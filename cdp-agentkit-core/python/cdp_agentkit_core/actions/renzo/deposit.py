from collections.abc import Callable
from decimal import Decimal
import time

from cdp import Wallet
from pydantic import BaseModel, Field

from cdp_agentkit_core.actions import CdpAction
from cdp_agentkit_core.actions.renzo.constants import RENZO_DEPOSIT_ABI


class RenzoDepositInput(BaseModel):
    """Input schema for Renzo deposit action."""

    amount: str = Field(..., description="The quantity of Ether to deposit")


DEPOSIT_PROMPT = """
This tool allows depositing Ether into Renzo.
It takes:

- amount: The amount of Ether to deposit

Important notes:
- Make sure to use the exact amount provided. Do not convert units for Ether for this action.
"""


def deposit_to_renzo(
    wallet: Wallet,
    amount: str,
) -> str:
    """Deposit Ether into Renzo.

    Args:
        wallet (Wallet): The wallet to execute the deposit from
        amount (str): The amount of Ether to deposit (e.g., 0.01 ETH)

    Returns:
        str: A success message with transaction hash or error message

    """
    if float(amount) <= 0:
        return "Error: Amount must be greater than 0"

    try:
        atomic_amount = str(int(Decimal(amount) * 1e18))
        min_amount_out = atomic_amount  # Change this according to amount
        deadline = str(int(time.time()) + (20 * 60))

        deposit_args = {
            "_minOut": min_amount_out,
            "_deadline": deadline,
        }

        invocation = wallet.invoke_contract(
            contract_address="0xf25484650484DE3d554fB0b7125e7696efA4ab99",
            method="depositETH",
            abi=RENZO_DEPOSIT_ABI,
            args=deposit_args,
            amount=amount,
            asset_id="eth",
        ).wait()

        return f"Deposited {amount} ETH to Renzo with transaction hash: {invocation.transaction_hash} and transaction link: {invocation.transaction_link}"

    except Exception as e:
        return f"Error depositing to Renzo: {e!s}"


class RenzoDepositAction(CdpAction):
    """Renzo deposit action."""

    name: str = "renzo_deposit"
    description: str = DEPOSIT_PROMPT
    args_schema: type[BaseModel] = RenzoDepositInput
    func: Callable[..., str] = deposit_to_renzo

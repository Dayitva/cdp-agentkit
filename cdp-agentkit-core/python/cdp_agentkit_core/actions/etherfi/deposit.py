from collections.abc import Callable
from decimal import Decimal

from cdp import Wallet
from pydantic import BaseModel, Field

from cdp_agentkit_core.actions import CdpAction
from cdp_agentkit_core.actions.etherfi.constants import ETHERFI_DEPOSIT_ABI


class EtherFiDepositInput(BaseModel):
    """Input schema for EtherFi deposit action."""

    amount: str = Field(..., description="The quantity of Ether to deposit")


DEPOSIT_PROMPT = """
This tool allows depositing Ether into EtherFi.
It takes:

- amount: The amount of Ether to deposit

Important notes:
- Make sure to use the exact amount provided. Do not convert units for Ether for this action.
"""


def deposit_to_etherfi(
    wallet: Wallet,
    amount: str,
) -> str:
    """Deposit Ether into EtherFi.

    Args:
        wallet (Wallet): The wallet to execute the deposit from
        amount (str): The amount of Ether to deposit (e.g., 0.01 ETH)

    Returns:
        str: A success message with transaction hash or error message

    """
    if Decimal(amount) <= 0:
        return "Error: Amount must be greater than 0"

    try:
        atomic_amount = str(int(Decimal(amount) * Decimal(1e18)))
        min_amount_out = str(int(Decimal(amount) * Decimal(1e18) * Decimal(0.9)))

        deposit_args = {
            "tokenIn": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
            "amountIn": atomic_amount,
            "minAmountOut": min_amount_out,
        }

        invocation = wallet.invoke_contract(
            contract_address="0xc38e046dFDAdf15f7F56853674242888301208a5",
            method="deposit",
            abi=ETHERFI_DEPOSIT_ABI,
            args=deposit_args,
            amount=amount,
            asset_id="eth",
        ).wait()

        return f"Deposited {amount} ETH to EtherFi with transaction hash: {invocation.transaction_hash} and transaction link: {invocation.transaction_link}"

    except Exception as e:
        return f"Error depositing to EtherFi: {e!s}"


class EtherFiDepositAction(CdpAction):
    """EtherFi deposit action."""

    name: str = "etherfi_deposit"
    description: str = DEPOSIT_PROMPT
    args_schema: type[BaseModel] = EtherFiDepositInput
    func: Callable[..., str] = deposit_to_etherfi

from collections.abc import Callable

from cdp import Wallet
from pydantic import BaseModel, Field

from cdp_agentkit_core.actions import CdpAction
from cdp_agentkit_core.actions.kelpdao.constants import KELPDAO_DEPOSIT_ABI

BASE_CA = "0x291088312150482826b3A37d5A69a4c54DAa9118"
ARBITRUM_CA = "0x376A7564AF88242D6B8598A5cfdD2E9759711B61"

class KelpdaoDepositInput(BaseModel):
    """Input schema for Kelpdao deposit action."""

    amount: str = Field(..., description="The quantity of Ether to deposit")


DEPOSIT_PROMPT = """
This tool allows depositing Ether into Kelpdao.
It takes:
- amount: The amount of Ether to deposit

Important notes:
- Make sure to use the exact amount provided. Do not convert units for Ether for this action.
- This is supported on the following networks:
  - Base Mainnet (ie, 'base', 'base-mainnet')
  - Ethereum Mainnet (ie, 'ethereum', 'ethereum-mainnet')
  - Polygon Mainnet (ie, 'polygon', 'polygon-mainnet')
  - Arbitrum Mainnet (ie, 'arbitrum', 'arbitrum-mainnet')
"""


def deposit_to_kelpdao(
    wallet: Wallet,
    amount: str,
) -> str:
    """Deposit Ether into Kelpdao.

    Args:
        wallet (Wallet): The wallet to execute the deposit from
        amount (str): The amount of Ether to deposit (e.g., 0.01 ETH)

    Returns:
        str: A success message with transaction hash or error message

    """
    if float(amount) <= 0:
        return "Error: Amount must be greater than 0"

    try:
        deposit_args = {
            "referralId": "0xd05723c7b17b4e4c722ca4fb95e64ffc54a70131c75e2b2548a456c51ed7cdaf"
        }

        invocation = wallet.invoke_contract(
            contract_address=ARBITRUM_CA,
            method="deposit",
            abi=KELPDAO_DEPOSIT_ABI,
            args=deposit_args,
            amount=amount,
            asset_id="eth",
        ).wait()

        return f"Deposited {amount} ETH to Kelpdao with transaction hash: {invocation.transaction_hash} and transaction link: {invocation.transaction_link}"

    except Exception as e:
        return f"Error depositing to Kelpdao: {e!s}"


class KelpdaoDepositAction(CdpAction):
    """Kelpdao deposit action."""

    name: str = "kelpdao_deposit"
    description: str = DEPOSIT_PROMPT
    args_schema: type[BaseModel] = KelpdaoDepositInput
    func: Callable[..., str] = deposit_to_kelpdao

from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS").lower()

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

ERC20_ABI = '[{"constant":true,"inputs":[{"name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]'

# Список популярных токенов, которые могут оставаться как пыль
TOKENS = {
    "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    "LINK": "0x514910771AF9Ca656af840dff83E8264EcF986CA"
}

DUST_THRESHOLD = 0.001  # В токенах, например 0.001 LINK

def get_token_balance(token_address):
    contract = w3.eth.contract(address=w3.to_checksum_address(token_address), abi=json.loads(ERC20_ABI))
    balance = contract.functions.balanceOf(WALLET_ADDRESS).call()
    return balance / (10 ** 18)

def check_dust():
    print(f"🔍 Scanning wallet {WALLET_ADDRESS} for token dust...")
    for name, address in TOKENS.items():
        balance = get_token_balance(address)
        if 0 < balance < DUST_THRESHOLD:
            print(f"⚠️ Dust detected: {name} = {balance:.8f}")
        else:
            print(f"✅ {name} balance is sufficient: {balance:.4f}")

if __name__ == "__main__":
    check_dust()

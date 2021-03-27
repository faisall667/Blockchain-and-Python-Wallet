import subprocess
import json
from constants import *
from dotenv import load_dotenv
import os
from bit import wif_to_key


load_dotenv()


mnemonic = os.getenv('mnemonic')

def derive_wallets (mnemonic, coin, numderive):
    command = f'./derive -g --mnemonic="{mnemonic}" --cols=path,address,privkey,pubkey --format=json --coin="{coin}" --numderive= 3 '
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return json.loads(output)
    



w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

coins = {ETH:derive_wallets(mnemonic,ETH,3),BTCTEST: derive_wallets(mnemonic,BTCTEST,3)}

ethprivatekey = coins[ETH][0]['privkey']
btcprivatekey = coins[BTCTEST][0]['privkey']
key = wif_to_key(btcprivatekey)


def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

def create_tx(coin, account, to, amount):
    if coin == ETH:
        gasEstimate = we3.eth.estimateGas({"recipient": to, "from":account.address, "gas": gasEstimate, "gasPrice": gasPrice, "nonce": nonce, "chainID": chainID})
        return {"recipient": to, "from":account.address, "gas": gasEstimate, "gasPrice": gasPrice, "nonce": nonce, "chainID": chainID}
    if coin == BTCTEST:
        return PrivateKetTestnet.prepare_transaction(account.address, [(to, amount,BTC)])

#def send_tx(coin, account, to, amount):
 #   raw_tx = create_tx(coin, amount, to, amount)
  #  sign = account.sign_transaction(raw_tx)
   # if coin == ETH:
    #    output = w3.eth.sendRawTransaction(sign.rawTransaction)
     #   return output.hex()
   # elif coin == BTCTEST:
    #    output2 = NetworkAPI.broadcast_tx_testnet(sign)
     #   return output2.hex()
        

def send_tx(coin,account, to, amount):
    raw_tx = create_tx(coin, account, to, amount)
    if coin == ETH:
        sign = account.sign_transaction(raw_tx)
        output = w3.eth.sendRawTransaction(sign.rawTransaction)
        print(output.hex())
        return output.hex()

    elif coin == BTCTEST:
        tx_btctest = create_tx(coin, account, to, amount)
        sign2 = account.sign_transaction(raw_tx)
        output2 = NetworkAPI.broadcast_tx_testnet(sign2) 
        print(output2.hex())
        return output.hex    
    
print(coins[BTCTEST][0]['privkey'])    
print(coins[BTCTEST][0]['address'])
print(key.get_balance("btc"))

priv_key_to_account("BTCTEST",key)

create_tx("BTCTEST", key, "muURH5chAcy3VyDXxYSDBpcLoqH42irr9c", 0.001)

send_tx("BTCTEST", key, "muURH5chAcy3VyDXxYSDBpcLoqH42irr9c", 0.001)

print(key.get_balance("btc"))


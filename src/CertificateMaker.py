"""
CertificateMaker.py

CertificateMaker.py implemnts core methods for creation, deletion and modification of Algorand certificates
It also allows possible transactions of certificates between two parties(useful for future implementation of trading of certificates).
"""

import json
import time
import base64
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
from Certificate import Certificate
import Algorand
from pprint import pprint

class CertificateMaker:
    def __init__(self):
        self.algod_address = "https://testnet-algorand.api.purestake.io/ps2"
        self.algod_token = "zLAOcinLq31BhPezSnHQL3NF7qBwHtku6XwN8igq"
        headers = {
            "X-Api-key": self.algod_token,
            # "X-Algo-API-Token": "asdf"
        }

        passphrase = "session lizard tide improve benefit have throw stove miss pave captain spread suffer appear barely provide cheese blade stock axis depart answer budget absorb axis"
        self.private_key = mnemonic.to_private_key(passphrase)
        self.my_address = mnemonic.to_public_key(passphrase)
        print("My address: {}".format(self.my_address))

        self.algod_client = algod.AlgodClient(self.algod_token, self.algod_address, headers)
        self.status = self.algod_client.status()
        # print(json.dumps(self.status, indent=4))

        self.account_info = self.algod_client.account_info(self.my_address)
        print("Account balance: {} microAlgos".format(self.account_info.get('amount')))

    def createCertificate(self,hash,asset_name, asset_url):
        c = Certificate("tmp", "tmp", "tmp", "tmp", "tmp", "tmp", "tmp", "tmp", "tmp", "tmp", "tmp", "tmp", "tmp",
                        "tmp", "tmp", "tmp")

        params = self.algod_client.suggested_params()
        # pprint(params.__dict__)
        first = params.first
        last = params.last
        gen = params.gen
        gh = params.gh
        min_fee = params.min_fee

        data = {
            "sender": self.my_address,
            "fee": min_fee,
            "first": first,
            "last": last,
            "gh": gh,
            "total": 1000,
            "decimals": 0,
            "default_frozen": False,
            "unit_name": "aa",
            "asset_name": asset_name,
            "metadata_hash": bytearray(hash.digest()),
            "manager": self.my_address,
            "reserve": self.my_address,
            "freeze": self.my_address,
            "clawback": self.my_address,
            "url": asset_url,
            "flat_fee": True
        }

        txn = transaction.AssetConfigTxn(**data)


        stxn = txn.sign(self.private_key)

        print("Asset Creation")

        txid = self.algod_client.send_transaction(stxn)

        txinfo = Algorand.wait_for_confirmation(self.algod_client, txid)
        #print(txinfo.keys())
        pprint(("txinfo", txinfo))
        # asset_id = txinfo.txn.
        account_info = self.algod_client.account_info(self.my_address)
        # pprint(account_info)
        print("The hash of certificate is: {}".format(hash.hexdigest()))
        
        print("Certificate recreated")
        return  txinfo['asset-index']


    # def revokeCertificate(self):
    #     data = {
    #         "sender": self.my_address,
    #         "fee": self.min_fee,
    #         "first": self.first,
    #         "last": self.last,
    #         "gh": self.gh,
    #         "receiver": self.my_address,
    #         "amt": 10,
    #         "index": self.asset_id,
    #         "revocation_target": self.my_address,
    #         "flat_fee": True
    #     }
    #     print("Asset Revoke")
    #     txn = transaction.AssetTransferTxn(**data)
    #     stxn = txn.sign(self.private_key)
    #     txid = self.algod_client.send_transaction(stxn, headers={'content-type': 'application/x-binary'})
    #     print(txid)
    #     Algorand.wait_for_confirmation(self.algod_client, txid)
    #     account_info = self.algod_client.account_info(self.my_address)
    #     print(json.dumps(account_info['assets'][str(self.asset_id)], indent=4))
    #     account_info = self.algod_client.account_info(self.my_address)
    #     print(json.dumps(account_info['assets'][str(self.asset_id)], indent=4))

    # def doTransaction(self):
    #     data = {
    #         "sender": self.my_address,
    #         "fee": self.min_fee,
    #         "first": self.first,
    #         "last": self.last,
    #         "gh": self.gh,
    #         "receiver": self.my_address,
    #         "amt": 10,
    #         "index": self.asset_id,
    #         "flat_fee": True
    #     }
    #     print("Asset Transfer")
    #     txn = transaction.AssetTransferTxn(**data)
    #     stxn = txn.sign(self.private_key)
    #     txid = self.algod_client.send_transaction(stxn, headers={'content-type': 'application/x-binary'})
    #     print(txid)

    #     Algorand.wait_for_confirmation(self.algod_client, txid)
    #     account_info = self.algod_client.account_info(self.my_address)
    #     print(json.dumps(account_info['assets'][str(self.asset_id)], indent=4))
        
if __name__ == "__main__":
    cm = CertificateMaker()
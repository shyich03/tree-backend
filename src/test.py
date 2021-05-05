# not used 
import json
import time
import base64
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
from Certificate import Certificate
import Algorand
from CertificateIndexer import CertificateIndexer
from CertificateMaker import CertificateMaker
import hashlib
import datetime
import numpy as np
from algosdk import account
# private_key, public_address = account.generate_account()
# print("Base64 Private Key: {}\nPublic Algorand Address: {}\n".format(private_key, public_address))
m=mnemonic.from_private_key('x3/x7jdaBWxJZN6IW7DtRw8T/mTMEim1Ca6yXrm1JXTCg+9kOU561gfgnml6qD3wj9cY1W3X4qzlzszEfDjRFw==')
print(m)
# x3/x7jdaBWxJZN6IW7DtRw8T/mTMEim1Ca6yXrm1JXTCg+9kOU561gfgnml6qD3wj9cY1W3X4qzlzszEfDjRFw==
# YKB66ZBZJZ5NMB7ATZUXVKB56CH5OGGVNXL6FLHFZ3GMI7BY2EL5EH3UZM
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "zLAOcinLq31BhPezSnHQL3NF7qBwHtku6XwN8igq"
purestake_token = {'X-Api-key': algod_token}

passphrase = "wedding shine wash pet apple force car taxi illegal scrap walnut virtual champion display glimpse barrel pioneer chat finish twenty increase hope patrol about stage"
private_key = mnemonic.to_private_key(passphrase)
my_address = mnemonic.to_public_key(passphrase)
print("My address: {}".format(my_address))

algod_client = algod.AlgodClient(algod_token, algod_address, headers=purestake_token)
params = algod_client.suggested_params()
cm = CertificateMaker()
ci = CertificateIndexer()
res = (np.array([[0,1],[1,0]]), 0, 5,6,datetime.datetime.now())

h=hashlib.sha256(str(res).encode())
# cm.createCertificate(h)
# print(h.hexdigest())
# print(my_address)
# print(private_key)
# res = (np.array([[0,0],[0,1]]), 0, 5,6,datetime.datetime.now())
ci.writeHashValue( res)
res = (np.array([[1,1],[0,1]]), 0, 5,6,datetime.datetime.now())
cm.createCertificate(h,"name","url")
cor = ci.checkMarkingCorrectness(res)
print(cor)



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


algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "zLAOcinLq31BhPezSnHQL3NF7qBwHtku6XwN8igq"
purestake_token = {'X-Api-key': algod_token}

passphrase = "session lizard tide improve benefit have throw stove miss pave captain spread suffer appear barely provide cheese blade stock axis depart answer budget absorb axis"
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
# cm.createCertificate(h)
cor = ci.checkMarkingCorrectness(res)
print(cor)


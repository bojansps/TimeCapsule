import contextlib
from datetime import datetime
import json
import uvicorn
from pydantic.class_validators import Any
from uvicorn.config import Config
from web3 import Web3
from fastapi import FastAPI, BackgroundTasks
from solcx import compile_standard, install_solc
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
import schedule
import subprocess
import time
import threading
import smtplib
import schedule
import time


class Item(BaseModel):
    message: Optional[str]
    reciever: Optional[str]
    email: Optional[str]
    password: Optional[str]
    title: Optional[str]
    date: Optional[str]


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# We add these two lines that we forgot from the video!
# print("Installing...")
# install_solc('0.7.0')
# Call
# solcx.get_installable_solc_versions()
# to
# view
# for available versions and

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    # solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

# w3 = Web3(Web3.HTTPProvider(os.getenv("RINKEBY_RPC_URL")))
# chain_id = 4
#
# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0xbb33feC643d41659686ea87675f55A2563B4d3E7"
private_key = "0xd7cdcd0cac316c4cc2bfd27ef0ce777e11155e5d0c1ebe84f177ae752c3b394b"


# -------------------------------------- CREATES THE SIMPLESTORAGE CONTRACT


@app.get("/")
async def helloWorld():
    # Create the contract in Python
    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
    # Get the latest transaction
    nonce = w3.eth.getTransactionCount(my_address)
    # Submit the transaction that deploys the contract
    transaction = SimpleStorage.constructor().buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce,
        }
    )
    # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    print("Deploying Contract!")
    print(signed_txn)
    # # Send it!
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

    # ----------------------- API CALLS

    # Create the contract in Python
    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
    # Get the latest transaction
    nonce = w3.eth.getTransactionCount(my_address)
    # Submit the transaction that deploys the contract
    transaction = SimpleStorage.constructor().buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce,
        }
    )
    # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    print("Deploying Contract!")
    print(signed_txn)
    # # Send it!
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

    simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    print(f"Initial Stored Value {simple_storage.functions.retrieveText().call()}")

    greeting_transaction = simple_storage.functions.storeText("Bojan").buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce + 1,
        }
    )

    signed_greeting_txn = w3.eth.account.sign_transaction(
        greeting_transaction, private_key=private_key
    )
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

    print(f"Updated Stored Value {simple_storage.functions.retrieveText().call()}")

    return simple_storage.functions.retrieveText().call()


@app.post("/message")
async def sendMessage(message: Item, backgroundTask: BackgroundTasks):
    # Create the contract in Python

    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
    # Get the latest transaction
    nonce = w3.eth.getTransactionCount(my_address)
    # Submit the transaction that deploys the contract
    transaction = SimpleStorage.constructor().buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce,
        }
    )
    # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    print("Deploying Contract!")
    print(signed_txn)
    # # Send it!
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

    # ----------------------- API CALLS

    # Create the contract in Python
    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
    # Get the latest transaction
    nonce = w3.eth.getTransactionCount(my_address)
    # Submit the transaction that deploys the contract
    transaction = SimpleStorage.constructor().buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce,
        }
    )
    # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    print("Deploying Contract!")
    print(signed_txn)
    # # Send it!
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

    simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    print(f"Initial Stored Value {simple_storage.functions.retrieveText().call()}")

    greeting_transaction = simple_storage.functions.storeText(message.message).buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce + 1,
        }
    )

    signed_greeting_txn = w3.eth.account.sign_transaction(
        greeting_transaction, private_key=private_key
    )
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

    print(f"Updated Stored Value {simple_storage.functions.retrieveText().call()}")
    print(message.date)

    x = datetime.strptime(message.date, '%d/%m/%y %H:%M:%S')

    seconds_to_send_post = datetime.timestamp(x) - datetime.timestamp(datetime.now())
    print(int(seconds_to_send_post))

    # backgroundTask.add_task(createSchedule, seconds_to_send_post,
    #                         message.email, message.reciever, message.password, message.message)

    backgroundTask.add_task(sendEmailScheduled, seconds_to_send_post, message.email, message.reciever, message.password, message.message)

    # backgroundTask.add_task(printSomething, "hello there ")

    return simple_storage.functions.retrieveText().call()


def printSomething(message):
    time.sleep(5)
    print(message + " sent")


@app.get('/text')
async def getText(backgroundTask: BackgroundTasks):
    backgroundTask.add_task(printSomething, "hello there ")
    return {'result': 'success'}


def createSchedule(second, email, reciever, password, message):
    schedule.every(second).seconds.do(sendEmailScheduled(email,
                                                         reciever,
                                                         password,
                                                         message))


class ScheduledEmail(threading.Thread):

    def run(self):
        print("In thread")
        # schedule.every(60).seconds.do(self.sendEmailScheduled)
        while True:
            schedule.run_pending()


def sendEmailScheduled(second_to_send, sender_email, rec_email, password, message):
    # sender_email = sender_email
    # rec_email = "kostadinovski.petar98@gmail.com"
    # password = "aicarambas.timecapsule123"
    # message = "Time capsule"
    time.sleep(second_to_send)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    print("Login success.")
    server.sendmail(sender_email, rec_email, message)
    print("Email has been sent to: ", rec_email)
    return schedule.CancelJob


if __name__ == '__main__':
    thread = ScheduledEmail()
    thread.start()
    # uvicorn.run('main:app', reload=True)
    # threading.Thread(target=uvicorn.run('main:app', reload=True)).start()

# threading.Thread(target=schedule.run_pending()).start()

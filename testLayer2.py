import unittest
import binascii
from binascii import b2a_hex, a2b_hex
from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams
from ontology.smart_contract.neo_contract.abi.abi_function import AbiFunction
from ontology.account.account import Account
from ontology.common.address import Address
from ontology.vm.params_builder import ParamsBuilder
from ontology.core.transaction import Transaction
from time import time
import time
import xlrd
import requests
from datetime import datetime
from ontology.smart_contract.neo_vm import NeoVm
from ontology.crypto.digest import Digest
from ontology.utils.util import bigint_to_neo_bytes

rpc_address = 'http://127.0.0.1:20336'
sdk = OntologySdk()
sdk.rpc.set_address(rpc_address)

wallet_path = "D:\\test-python-sdk\\wallet.dat"
sdk.wallet_manager.open_wallet(wallet_path)
admin_addr = "ASwaf8mj2E3X18MHvcJtXoDsMqUjJswRWS"
admin_pwd = "123123"
ownerAcct = sdk.wallet_manager.get_account(admin_addr, admin_pwd)
ownerAddress = Address.b58decode(admin_addr).to_array()

challengerAddress = "ARDskfQuvTa7TvbCVNX8MP5zjg7SUdDgSa"
challengerAccount = Address.b58decode(challengerAddress).to_array()
challengerAcct = sdk.wallet_manager.get_account(challengerAddress, admin_pwd)

challengerAddress1 = "ASJeGy7CPoa2EvTEAyQFd5uxD9mr8ejVxE"
challengerAccount1 = Address.b58decode(challengerAddress1).to_array()
challengerAcct1 = sdk.wallet_manager.get_account(challengerAddress1, admin_pwd)

tokenAddress = "3cf3cd1332a4c7eabcb3665d2b6e3388047bd6e4"
token_address = bytearray.fromhex(tokenAddress)
token_address.reverse()

PLCRAddress = "b7e54aa69c0c60a93104a8613e3935cf7db7294f"
PLCR_address = bytearray.fromhex(PLCRAddress)
PLCR_address.reverse()

ParameterizerAddress = "0808b3874e9d86c0638af8a03b13b7feea172305"
Parameterizer_address = bytearray.fromhex(ParameterizerAddress)
Parameterizer_address.reverse()

RegistryAddress = "6053d15e77a22aa06d37e39d3af00e72f22fdfaa"
Registry_address = bytearray.fromhex(RegistryAddress)
Registry_address.reverse()

ContractAddress = "b7e54aa69c0c60a93104a8613e3935cf7db7294f"
contract_address_str = ContractAddress
contract_address = bytearray.fromhex(contract_address_str)
contract_address.reverse()

listingHash = '11111211111111111111'
pollID = 9

secretHash = 'c15513d1fec76594f8d3eeb1f1af4fca8a938a669e8e575c15a115a60d98404a'
secretHash = bytearray.fromhex(secretHash)

class Test(unittest.TestCase):

    def test_PLCRVoting_init(self):

        payerAcct = ownerAcct

        param_list = []
        param_list1 = []  # args

        param_list.append("init".encode())  # operation

        param_list1.append(token_address)
        param_list.append(param_list1)
        print("params_invoke ----- ", param_list, "\n")
        hash2 = self.test_invoke_PLCRVoting(payerAcct, param_list)


        print("hash === ", hash2)
        return True

    def test_Parameterizer_init(self):

        payerAcct = ownerAcct

        param_list = []
        param_list1 = []  # args

        param_list.append("init".encode())  # operation

        param_list1.append(token_address)
        param_list1.append(PLCR_address)
        parametersList = [100, 100, 30, 30, 30, 30, 50, 30, 50, 50, 20, 20]
        param_list1.append(parametersList)
        param_list1.append(1112)

        param_list.append(param_list1)
        print("params_invoke ----- ", param_list, "\n")
        hash2 = self.test_invoke(payerAcct, param_list)


        print("hash === ", hash2)
        return True

    def test_Registry_init(self):
        payerAcct = ownerAcct

        param_list = []
        param_list1 = []  # args

        param_list.append("init".encode())  # operation

        param_list1.append(token_address)
        param_list1.append(PLCR_address)
        param_list1.append(Parameterizer_address)
        param_list1.append(1111)

        param_list.append(param_list1)
        print("params_invoke ----- ", param_list, "\n")
        hash2 = self.test_invoke_Registry(payerAcct, param_list)


        print("hash === ", hash2)
        return True

    def test_Registry_apply(self):

        payerAcct = ownerAcct

        param_list = []
        param_list1 = []  # args

        param_list.append("apply".encode())  # operation

        param_list1.append(ownerAddress)
        param_list1.append(listingHash)
        param_list1.append(200)
        param_list1.append(666)

        param_list.append(param_list1)
        print("params_invoke ----- ", param_list, "\n")
        hash2 = self.test_invoke_Registry(payerAcct, param_list)


        print("hash === ", hash2)
        return True

    def test_Registry_challenge(self):


        payerAcct = challengerAcct

        param_list = []
        param_list1 = []  # args

        param_list.append("challenge".encode())  # operation

        param_list1.append(challengerAccount)
        param_list1.append(listingHash)
        param_list1.append(66666)

        param_list.append(param_list1)
        print("params_invoke ----- ", param_list, "\n")
        hash2 = self.test_invoke_Registry(payerAcct, param_list)


        print("hash === ", hash2)
        return True

    def test_PLCR_reveal(self):

        self.test_PLCR_revealPeriodActive()

        payerAcct = ownerAcct

        param_list = []
        param_list1 = []  # args

        param_list.append("revealVote".encode())  # operation


        param_list1.append(ownerAddress)
        param_list1.append(pollID)
        param_list1.append(1)
        param_list1.append(pollID)

        param_list.append(param_list1)
        print("params_invoke ----- ", param_list, "\n")
        hash2 = self.test_invoke_PLCRVoting(payerAcct, param_list)


        print("hash === ", hash2)
        return True

    def test_Registry_updateStatus(self):

        payerAcct = challengerAcct

        param_list = []
        param_list1 = []  # args

        param_list.append("updateStatus".encode())  # operation

        param_list1.append(listingHash)

        param_list.append(param_list1)
        print("params_invoke ----- ", param_list, "\n")
        hash2 = self.test_invoke_Registry(payerAcct, param_list)


        print("hash === ", hash2)
        return True

    def test_Registry_withdraw(self):

        payerAcct = challengerAcct

        param_list = []
        param_list1 = []  # args

        param_list.append("withdraw".encode())  # operation

        param_list1.append(challengerAccount)
        param_list1.append(listingHash)
        param_list1.append(10000000000)

        param_list.append(param_list1)
        print("params_invoke ----- ", param_list, "\n")
        hash2 = self.test_invoke_Registry(payerAcct, param_list)


        print("hash === ", hash2)
        return True

    def test_PLCR_commitVoteC(self):

        payerAcct = challengerAcct

        param_list = []
        param_list1 = []  # args

        param_list.append("commitVote".encode())  # operation


        param_list1.append(challengerAccount)
        param_list1.append(1)
        param_list1.append('45c74115a686111bb11bf1968f424fc3b82268111a659a9ad44991778c5772d2')
        param_list1.append(100)
        param_list1.append(0)

        param_list.append(param_list1)
        print("params_invoke ----- ", param_list, "\n")
        hash2 = self.test_invoke_PLCRVoting(payerAcct, param_list)


        print("hash === ", hash2)
        return True

    def test_PLCR_commitVoteC1(self):

        payerAcct = challengerAcct1

        param_list = []
        param_list1 = []  # args

        param_list.append("commitVote".encode())  # operation


        param_list1.append(challengerAccount1)
        param_list1.append(1)
        param_list1.append('95c74115a626187bb22bf9968f494fc6182268011a659a9ad44991778c0772d2')
        param_list1.append(100)
        param_list1.append(0)

        param_list.append(param_list1)
        print("params_invoke ----- ", param_list, "\n")
        hash2 = self.test_invoke_PLCRVoting(payerAcct, param_list)


        print("hash === ", hash2)
        return True

    def test_PLCR_commitVoteO(self):

        payerAcct = ownerAcct

        param_list = []
        param_list1 = []  # args

        param_list.append("commitVote".encode())  # operation

        param_list1.append(ownerAddress)
        param_list1.append(pollID)
        param_list1.append(secretHash)
        param_list1.append(150)
        param_list1.append(0)

        param_list.append(param_list1)
        print("params_invoke ----- ", param_list, "\n")
        hash2 = self.test_invoke_PLCRVoting(payerAcct, param_list)

        print("hash === ", hash2)
        return True

    def test_getPollNounce(self):
        payerAcct = ownerAcct
        param_list = []
        param_list.append("getPollNounce".encode())
        param_list1 = []

        param_list.append(param_list1)
        print(param_list)

        res = self.test_invokeRead(payerAcct, param_list)
        print( res)
        return True

    def test_getVoteTokenBalance(self):
        payerAcct = ownerAcct

        param_list = []
        param_list.append("getVoteTokenBalance".encode())
        param_list1 = []
        param_list1.append(ownerAddress)

        param_list.append(param_list1)
        print(param_list)

        res = self.test_invokeRead(payerAcct, param_list)
        print( res)
        return True

    def test_getNumTokens(self):
        payerAcct = ownerAcct

        param_list = []
        param_list.append("getNumTokens".encode())
        param_list1 = []
        param_list1.append(ownerAddress)
        param_list1.append(1)

        param_list.append(param_list1)
        print(param_list)

        res = self.test_invokeRead(payerAcct, param_list)
        print( res)
        return True

    def test_PLCR_revealPeriodActive(self):
        payerAcct = ownerAcct

        param_list = []
        param_list.append("revealPeriodActive".encode())
        param_list1 = []

        param_list1.append(pollID)

        param_list.append(param_list1)
        print(param_list)
        times = 0
        while(1):
            time.sleep(1)
            res = self.test_invokeRead(payerAcct, param_list)
            times += 1
            print(times)
            if res[0] != "00":
                break
        print(res)
        return True

    def test_PLCR_getEndTimeList(self):
        payerAcct = ownerAcct

        param_list = []
        param_list.append("getEndTimeList".encode())
        param_list1 = []

        param_list1.append(pollID)

        param_list.append(param_list1)
        print(param_list)
        res = self.test_invokeRead(payerAcct, param_list)
        print(res)
        return True

    def test_commiStage(self):
        payerAcct = ownerAcct

        param_list = []
        param_list.append("get".encode())
        param_list1 = []
        param_list1.append("commitStageLen")
        param_list.append(param_list1)

        res = self.test_invokeRead(payerAcct, param_list)
        print(res)

        param_list = []
        param_list.append("get".encode())
        param_list1 = []
        param_list1.append("revealStageeLen")
        param_list.append(param_list1)

        res = self.test_invokeRead(payerAcct, param_list)
        print(res)
        return True

    def test_getListing(self):
        payerAcct = ownerAcct

        param_list = []
        param_list.append("getListing".encode())
        param_list1 = []
        param_list1.append(listingHash)

        param_list.append(param_list1)
        print(param_list)

        res = self.test_invokeRead(payerAcct, param_list)
        print( res)
        return True

    def test_getHash(self):
        payerAcct = ownerAcct

        param_list = []
        param_list.append("calculateSecretHashTest".encode())
        param_list1 = []
        param_list1.append(1)
        param_list1.append(pollID)

        param_list.append(param_list1)
        print(param_list)

        res = self.test_invokeRead(payerAcct, param_list)
        print( res)
        return True

    def test_validPosition(self):
        payerAcct = ownerAcct

        param_list = []
        param_list.append("validPosition".encode())
        param_list1 = []
        param_list1.append(0)
        param_list1.append(1)
        param_list1.append(ownerAddress)
        param_list1.append(300)
        param_list.append(param_list1)
        print(param_list)

        res = self.test_invokeRead(payerAcct, param_list)
        print( res)
        return True

    def test_get(self):
        payerAcct = ownerAcct
        param_list = []
        param_list.append("getParamRCH".encode())
        param_list1 = []
        param_list.append(param_list1)
        print(param_list)

        res = self.test_invokeRead(payerAcct, param_list)
        print( res)
        return True

    def test_invoke(self, payerAcct, param_list):
        params = BuildParams.create_code_params_script(param_list)

        # tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 20000, 500)
        # sdk.sign_transaction(tx, payerAcct)
        # nil, gaslimit = sdk.rpc.send_raw_transaction_pre_exec(tx)
        #
        params.append(0x67)
        for i in contract_address:
            params.append(i)
        gaslimit = 2000000000
        unix_time_now = int(time.time())
        tx = Transaction(0, 0xd1, unix_time_now, 500, gaslimit, payerAcct.get_address().to_array(), params, bytearray(),
                         [], bytearray())
        sdk.sign_transaction(tx, payerAcct)
        loopFlag = True
        hash = None
        while loopFlag:
            try:
                hash = sdk.rpc.send_raw_transaction(tx)
            except requests.exceptions.ConnectTimeout or requests.exceptions.ConnectionError:
                loopFlag = True
            if hash != None:
                loopFlag = False
        return hash

    def test_invoke_Registry(self, payerAcct, param_list):
        params = BuildParams.create_code_params_script(param_list)

        # tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 20000, 500)
        # sdk.sign_transaction(tx, payerAcct)
        # nil, gaslimit = sdk.rpc.send_raw_transaction_pre_exec(tx)
        #
        params.append(0x67)
        for i in Registry_address:
            params.append(i)
        gaslimit = 2000000000
        unix_time_now = int(time.time())
        tx = Transaction(0, 0xd1, unix_time_now, 500, gaslimit, payerAcct.get_address().to_array(), params, bytearray(),
                         [], bytearray())
        sdk.sign_transaction(tx, payerAcct)
        loopFlag = True
        hash = None
        while loopFlag:
            try:
                hash = sdk.rpc.send_raw_transaction(tx)
            except requests.exceptions.ConnectTimeout or requests.exceptions.ConnectionError:
                loopFlag = True
            if hash != None:
                loopFlag = False
        return hash

    def test_invoke_PLCRVoting(self, payerAcct, param_list):
        params = BuildParams.create_code_params_script(param_list)

        # tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 20000, 500)
        # sdk.sign_transaction(tx, payerAcct)
        # nil, gaslimit = sdk.rpc.send_raw_transaction_pre_exec(tx)
        #
        params.append(0x67)
        for i in PLCR_address:
            params.append(i)
        gaslimit = 2000000000
        unix_time_now = int(time.time())
        tx = Transaction(0, 0xd1, unix_time_now, 500, gaslimit, payerAcct.get_address().to_array(), params, bytearray(),
                         [], bytearray())
        sdk.sign_transaction(tx, payerAcct)
        loopFlag = True
        hash = None
        while loopFlag:
            try:
                hash = sdk.rpc.send_raw_transaction(tx)
            except requests.exceptions.ConnectTimeout or requests.exceptions.ConnectionError:
                loopFlag = True
            if hash != None:
                loopFlag = False
        return hash

    def test_handleEvent(self, action, hash):
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        if action == "setOddsTable":
            events = res["Notify"]
            # print("buyPaper-res-events is ", events)
            notifyContents = []
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == ContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    notifyContent.append(first)
                    notifyContents.append(notifyContent)
            print("setOddsTable-res-events is : ", notifyContents)
        elif action == "setLuckyToOngRate":
            events = res["Notify"]
            # print("buyPaper-res-events is ", events)
            notifyContents = []
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == ContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    notifyContent.append(first)
                    if first == "setRate":
                        num = event["States"][1]
                        if not num:
                            num = "0"
                        num = bytearray.fromhex(num)
                        num.reverse()
                        num = int(num.hex(), 16)
                        notifyContent.append(num)
                        num = event["States"][2]
                        if not num:
                            num = "0"
                        num = bytearray.fromhex(num)
                        num.reverse()
                        num = int(num.hex(), 16)
                        notifyContent.append(num)
                    notifyContents.append(notifyContent)
            print("setLuckyToOngRate-res-events is : ", notifyContents)
        elif action == "startNewRound":
            events = res["Notify"]
            notifyContents = []
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == ContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    notifyContent.append(first)
                    if first == "startNewRound":
                        roundNumber = event["States"][1]
                        if not roundNumber:
                            num = "0"
                        roundNumber = bytearray.fromhex(roundNumber)
                        roundNumber.reverse()
                        roundNumber = int(roundNumber.hex(), 16)
                        notifyContent.append(roundNumber)

                        timeStamp = str(event["States"][2])
                        if not timeStamp:
                            timeStamp = "0"
                        timeStamp = bytearray.fromhex(timeStamp)
                        timeStamp.reverse()
                        timeStamp = int(timeStamp.hex(), 16)
                        dateTime = datetime.utcfromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
                        notifyContent.append(dateTime)

                        hashHexString = str(event["States"][3])
                        notifyContent.append(hashHexString)
                    notifyContents.append(notifyContent)
            print("startNewRound-res-events is : ", notifyContents)
        elif action == "bet":
            events = res["Notify"]
            notifyContents = []
            i = 1
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == ContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    notifyContent.append(first)
                    if first == "bet":
                        roundNumber = event["States"][1]
                        if not roundNumber:
                            num = "0"
                        roundNumber = bytearray.fromhex(roundNumber)
                        roundNumber.reverse()
                        roundNumber = int(roundNumber.hex(), 16)
                        notifyContent.append(roundNumber)

                        account = Address(binascii.a2b_hex(event["States"][2]))
                        account = account.b58encode()
                        notifyContent.append(account)

                        num = event["States"][3]
                        if not num:
                            num = "0"
                        num = bytearray.fromhex(num)
                        num.reverse()
                        num = int(num.hex(), 16)
                        notifyContent.append(num)
                    notifyContents.append(notifyContent)
            print("bet-res-events is : ", notifyContents)
        elif action == "endCurrentRound":
            res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
            print("endCurrentRound-res is ", res)
            events = res["Notify"]
            notifyContents = []
            i = 1
            # print("events === ", events)
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == ContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    if first == "endCurrentRound":
                        notifyContent.append(first)
                        roundNumber = event["States"][1]
                        if not roundNumber:
                            num = "0"
                        roundNumber = bytearray.fromhex(roundNumber)
                        roundNumber.reverse()
                        roundNumber = int(roundNumber.hex(), 16)
                        notifyContent.append(roundNumber)

                        explodePoint = event["States"][2]
                        if not explodePoint:
                            explodePoint = "0"
                        explodePoint = bytearray.fromhex(explodePoint)
                        explodePoint.reverse()
                        explodePoint = int(explodePoint.hex(), 16)
                        notifyContent.append(explodePoint)

                        salt = event["States"][3]
                        if not salt:
                            salt = "0"
                        salt = bytearray.fromhex(salt)
                        salt.reverse()
                        salt = int(salt.hex(), 16)
                        notifyContent.append(salt)

                        effectiveEscapeAcctPointOddsProfitList = event["States"][4]
                        notify1 = []
                        for effectiveEscapeAcctPointOddsProfit in effectiveEscapeAcctPointOddsProfitList:
                            notify2 = []
                            account = Address(binascii.a2b_hex(effectiveEscapeAcctPointOddsProfit[0]))
                            account = account.b58encode()
                            notify2.append(account)

                            escapePoint = effectiveEscapeAcctPointOddsProfit[1]
                            if not escapePoint:
                                escapePoint = "0"
                            escapePoint = bytearray.fromhex(escapePoint)
                            escapePoint.reverse()
                            escapePoint = int(escapePoint.hex(), 16)
                            notify2.append(escapePoint)

                            # odds = effectiveEscapeAcctPointOddsProfit[2]
                            # if not odds:
                            #     odds = "0"
                            # odds = bytearray.fromhex(odds)
                            # odds.reverse()
                            # odds = int(odds.hex(), 16)
                            # notify2.append(odds)

                            profit = effectiveEscapeAcctPointOddsProfit[2]
                            if not profit:
                                profit = "0"
                            profit = bytearray.fromhex(profit)
                            profit.reverse()
                            profit = int(profit.hex(), 16)
                            notify2.append(profit)

                            notify1.append(notify2)

                        notifyContent.append(notify1)
                        # print("endCurrentRound-res-event is : ", notifyContent)
                    elif first == "Error":
                        errorCode = event["States"][1]
                        if not errorCode:
                            errorCode = "0"
                        errorCode = bytearray.fromhex(errorCode)
                        errorCode.reverse()
                        errorCode = int(errorCode.hex(), 16)
                        notifyContent.append(errorCode)
                    notifyContents.append(notifyContent)
            print("endCurrentRound-res-events is : ", notifyContents)

        return True

    def test_invokeRead(self, payerAcct, param_list):
        params = BuildParams.create_code_params_script(param_list)

        tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 2000000, 50000)
        sdk.sign_transaction(tx, payerAcct)
        res = sdk.rpc.send_raw_transaction_pre_exec(tx)
        return res


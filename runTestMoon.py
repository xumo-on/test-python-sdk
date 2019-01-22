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

wallet_path = "D:\\test-Moon\\wallet.dat"
sdk.wallet_manager.open_wallet(wallet_path)
admin_addr = "ASwaf8mj2E3X18MHvcJtXoDsMqUjJswRWS"
admin_pwd = "123123"
adminAcct = sdk.wallet_manager.get_account(admin_addr, admin_pwd)

luckyMoonContractAddress = "6bc94156ad2057cab6b159217d4e444fd2e17005"

contract_address_str = luckyMoonContractAddress
contract_address = bytearray.fromhex(contract_address_str)
contract_address.reverse()

explodePoint = 1000
salt = 89
betNum = 100
escapePoint = 100000


class Test(unittest.TestCase):

    def test_getNum1(self):

        param_list = []
        param_list.append("getExplodePoint".encode())

        abi_function = AbiFunction("getExplodePoint", "", param_list)
        res = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 20000000, 200000000, abi_function,
                                            True)

        num = bytearray.fromhex(res[0])
        num.reverse()
        num = int(num.hex(), 16)

        print(num)
        return num

    def test_init(self):
        param_list = []
        # when pre-execute, don't use 0x67
        abi_function = AbiFunction("init", "", param_list)
        hash = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 20000, 500, abi_function, False)
        # res = sdk.rpc.send_raw_transaction(tx)
        time.sleep(6)
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        print("init-res is ", res)
        events = res["Notify"]
        notifyContents = []
        for event in events:
            notifyContent = []
            if event["ContractAddress"] == luckyMoonContractAddress:
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
                elif first == "setReferralBonus":
                    num = event["States"][1]
                    if not num:
                        num = "0"
                    num = bytearray.fromhex(num)
                    num.reverse()
                    num = int(num.hex(), 16)
                    notifyContent.append(num)
                notifyContents.append(notifyContent)
        print("init-res-event is : ", notifyContents)
        return True

    def test_startNewRound(self):
        payerAcct = adminAcct
        hash11 = self.test_getHash(1000)
        hash22 = self.test_getHash(89)
        print(hash11, type(hash11))
        print(hash22)
        h1 = (bytearray.fromhex(hash11))
        h1.reverse()
        h2 = (bytearray.fromhex(hash22))
        h2.reverse()
        hash33 = int(h1.hex(), 16) ^ int(h2.hex(), 16)
        hashh = hex(hash33)
        hashh = hashh[2:]
        h3 = bytearray.fromhex(str(hashh))
        h3.reverse()

        param_list = []
        param_list.append("startNewRound".encode())
        param_list1 = []
        param_list1.append(h3)
        param_list.append(param_list1)
        hash1 = self.test_invoke(payerAcct, param_list)
        print("hash === setOddsTable", hash1)
        time.sleep(6)
        self.test_handleEvent("startNewRound", hash1)
        return True

    def test_bet(self):
        payerAcct = adminAcct
        param_list = []
        param_list.append("bet".encode())
        param_list1 = []
        param_list1.append(payerAcct.get_address().to_array())
        param_list1.append(betNum)
        param_list.append(param_list1)
        hash = self.test_invoke(payerAcct, param_list)
        print("hash === bet", hash)
        time.sleep(6)
        self.test_handleEvent("bet", hash)
        return True

    def test_end(self):
        param_list = []
        param_list.append("endCurrentRound".encode())
        param_list1 = []
        param_list1.append(explodePoint)
        param_list1.append(salt)
        param_list2 = []
        param_list3 = []
        param_list3.append(adminAcct.get_address().to_array())
        param_list3.append(escapePoint)
        param_list2.append(param_list3)
        param_list1.append(param_list2)
        param_list.append(param_list1)

        params = BuildParams.create_code_params_script(param_list)
        params.append(0x67)
        for i in contract_address:
            params.append(i)

        unix_time_now = int(time.time())

        tx = Transaction(0, 0xd1, unix_time_now, 500, 20000000, adminAcct.get_address().to_array(), params, bytearray(),
                         [], bytearray())

        sdk.sign_transaction(tx, adminAcct)
        res1 = sdk.rpc.send_raw_transaction(tx)

        print(res1)
        return res1

    def test_normal_bet(self):
        self.test_startNewRound()

        print("###########before bet###########")
        self.test_getCurrentRound()
        self.test_getRoundStatus()

        self.test_bet()
        time.sleep(20)

        print("###########after bet###########")
        self.test_getRoundStatus()

        self.test_end()

        print("###########after end###########")
        time.sleep(6)
        self.test_getRoundStatus()
        self.test_getLuckyBalance()

    def test_getCurrentRound(self):
        payerAcct = adminAcct
        param_list = []
        param_list.append("getCurrentRound".encode())
        param_list1 = []
        param_list.append(param_list1)
        currentRound = self.test_invokeRead(payerAcct, param_list)
        currentRound = int(currentRound[0], 16)
        print("currentRound is:", currentRound)
        return currentRound

    def test_getRoundStatus(self):
        payerAcct = adminAcct
        currentRound = self.test_getCurrentRound()
        param_list = []
        param_list.append("getRoundStatus".encode())
        param_list1 = []
        param_list1.append(currentRound)
        param_list.append(param_list1)

        roundStatus = self.test_invokeRead(payerAcct, param_list)
        roundStatus = bytearray.fromhex(roundStatus[0])
        roundStatus = str(roundStatus)
        print("currentRoundStatus is:",  roundStatus)
        return roundStatus

    def test_getLuckyBalance(self):
        payerAcct = adminAcct
        param_list = []
        param_list.append("getLuckyBalanceOf".encode())
        param_list1 = []
        param_list1.append(adminAcct.get_address().to_array())
        param_list.append(param_list1)
        luckyNum = self.test_invokeRead(payerAcct, param_list)
        luckyNum = luckyNum[0]
        Len = len(luckyNum)
        luckNumList = []
        i = Len
        while i > 0:
            luckNumList.append(luckyNum[i - 2:i])
            i -= 2
        luckyNum = ''.join(luckNumList)
        luckyNum = int(luckyNum, 16)

        print("LuckyNum is:", luckyNum)
        return luckyNum

    def test_invoke(self, payerAcct, param_list):
        params = BuildParams.create_code_params_script(param_list)
        #
        # tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 20000, 500)
        # sdk.sign_transaction(tx, payerAcct)
        # nil, gaslimit = sdk.rpc.send_raw_transaction_pre_exec(tx)
        #
        params.append(0x67)
        for i in contract_address:
            params.append(i)
        gaslimit = 20000
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
                if event["ContractAddress"] == luckyMoonContractAddress:
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
                if event["ContractAddress"] == luckyMoonContractAddress:
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
                if event["ContractAddress"] == luckyMoonContractAddress:
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
                if event["ContractAddress"] == luckyMoonContractAddress:
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
                if event["ContractAddress"] == luckyMoonContractAddress:
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

    def test_getHash(self, value):
        hash1 = Digest.sha256(bigint_to_neo_bytes(value), 0).hex()
        return hash1

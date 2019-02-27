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
adminAcct = sdk.wallet_manager.get_account(admin_addr, admin_pwd)
ad = Address.b58decode(admin_addr).to_array()

toAccount = "ARDskfQuvTa7TvbCVNX8MP5zjg7SUdDgSa"
toAcct = Address.b58decode(toAccount).to_array()

ContractAddress = "ade81ea47dc5babac9ec00f02292e7b8c39ab5d4"

contract_address_str = ContractAddress
contract_address = bytearray.fromhex(contract_address_str)
contract_address.reverse()

DNA1 = 111101666666104

pokeHashList = []

class Test(unittest.TestCase):

    def test_startGame(self):
        payerAcct = adminAcct

        param_list = []  # args
        param_list1 = []  # args[0]

        param_list.append("startGame".encode())  # operation
        i = 0
        num = 52
        pokeList = []
        while i < num:
            pokeList.append("bd15b3cd9804c09fa179d1310678bb08104a311aa9d9173f020363367e8b5434")
            i += 1
        param_list1.append(pokeList)
        param_list1.append([admin_addr, admin_addr, admin_addr, admin_addr, admin_addr, admin_addr, admin_addr, admin_addr, admin_addr, admin_addr])
        param_list1.append(22)
        param_list.append(param_list1)
        print("params_invoke ----- ", param_list, "\n")
        hash2 = self.test_invoke(payerAcct, param_list)


        print("hash === ", hash2)
        return True

    def test_transferProperty(self):
        payerAcct = adminAcct
        param_list = []
        param_list.append("transferProperty".encode())
        param_list1 = []
        param_list2 = [toAcct, DNA1]
        print(DNA1)
        param_list1.append([param_list2])
        param_list.append(param_list1)
        print(param_list)
        hash = self.test_invoke(payerAcct, param_list)
        print("hash === transferProperty", hash)
        return True

    def test_removeProperty(self):
        payerAcct = adminAcct
        param_list = []
        param_list.append("removeProperty".encode())
        param_list1 = []
        param_list2 = [DNA1 + 1, DNA1 + 2]
        param_list1.append(param_list2)
        param_list.append(param_list1)
        print(param_list)
        hash = self.test_invoke(payerAcct, param_list)
        print("hash === removeProperty", hash)
        return True

    def test_get(self):
        payerAcct = adminAcct
        param_list = []
        param_list.append("getPlayerAllDNA".encode())
        param_list1 = []
        param_list1.append(toAcct)
        param_list.append(param_list1)
        print(param_list)

        res = self.test_invokeRead(payerAcct, param_list)
        print( res)
        return True

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


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import unittest

from ontology.ont_sdk import OntologySdk
from ontology.common.address import Address
from ontology.account.account import Account
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo

rpc_address = 'http://polaris3.ont.io:20336'
# rpc_address = 'http://127.0.0.1:20336'
sdk = OntologySdk()

private_key = '523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f'
private_key2 = '75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf'
private_key3 = '1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114'
private_key4 = 'f9d2d30ffb22dffdf4f14ad6f1303460efc633ea8a3014f638eaa19c259bada1'
acct1 = Account(private_key, SignatureScheme.SHA256withECDSA)
acct2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
acct3 = Account(private_key3, SignatureScheme.SHA256withECDSA)
acct4 = Account(private_key4, SignatureScheme.SHA256withECDSA)


class TestNeoVm(unittest.TestCase):

    def test_big_int(self):
        num_dec = 135241956301000000
        bit_length = 57
        self.assertEqual(num_dec.bit_length(), bit_length)
        num_hex_str_little = '40cd0cbcd779e001'
        num_hex_str_big = '01e079d7bc0ccd40'
        self.assertEqual(num_hex_str_little, num_dec.to_bytes(8, 'little').hex())
        self.assertEqual(num_hex_str_big, num_dec.to_bytes(8, 'big').hex())

    def test_get_balance(self):
        sdk.set_rpc(rpc_address)
        acct_balance = sdk.rpc.get_balance(acct1.get_address_base58())
        try:
            acct_balance['ont']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
        try:
            acct_balance['ong']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')

        acct_balance_2 = sdk.rpc.get_balance(acct1.get_address_base58())
        try:
            acct_balance_2['ont']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
        try:
            acct_balance_2['ong']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')

        acct_balance_3 = sdk.rpc.get_balance(acct1.get_address_base58())
        try:
            acct_balance_3['ont']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
        try:
            acct_balance_3['ong']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')

        acct_balance_4 = sdk.rpc.get_balance(acct1.get_address_base58())
        try:
            acct_balance_4['ont']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')
        try:
            acct_balance_4['ong']
        except KeyError:
            raised = True
            self.assertFalse(raised, 'Exception raised')

    def test_unbound_ong(self):
        sdk.set_rpc(rpc_address)
        acct1_unbound_ong = sdk.native_vm().asset().query_unbound_ong(acct1.get_address_base58())
        self.assertGreaterEqual(int(acct1_unbound_ong), 0)
        acct2_unbound_ong = sdk.native_vm().asset().query_unbound_ong(acct4.get_address_base58())
        self.assertGreaterEqual(int(acct2_unbound_ong), 0)
        acct3_unbound_ong = sdk.native_vm().asset().query_unbound_ong(acct4.get_address_base58())
        self.assertGreaterEqual(int(acct3_unbound_ong), 0)
        acct4_unbound_ong = sdk.native_vm().asset().query_unbound_ong(acct4.get_address_base58())
        self.assertGreaterEqual(int(acct4_unbound_ong), 0)

    def test_address_from_vm_code(self):
        sdk.set_rpc(rpc_address)
        code = '54c56b6c766b00527ac46c766b51527ac4616c766b00c36c766b52527ac46c766b52c30548656c6c6f87630600621a' \
               '006c766b51c300c36165230061516c766b53527ac4620e00006c766b53527ac46203006c766b53c3616c756651c56b' \
               '6c766b00527ac46151c576006c766b00c3c461681553797374656d2e52756e74696d652e4e6f7469667961616c7566'
        code_hex_address = '362cb5608b3eca61d4846591ebb49688900fedd0'
        code_address = Address.address_from_vm_code(code)
        self.assertEqual(code_address.to_reverse_hex_str(), code_hex_address)

    def test_make_deploy_transaction(self):
        sdk.set_rpc(rpc_address)
        code = '54c56b6c766b00527ac46c766b51527ac4616c766b00c36c766b52527ac46c766b52c30548656c6c6f87630600621a' \
               '006c766b51c300c36165230061516c766b53527ac4620e00006c766b53527ac46203006c766b53c3616c756651c56b' \
               '6c766b00527ac46151c576006c766b00c3c461681553797374656d2e52756e74696d652e4e6f7469667961616c7566'
        payer = acct2
        b58_payer = payer.get_address_base58()
        gas_limit = 20000000
        gas_price = 500
        tx = sdk.neo_vm().make_deploy_transaction(code, True, 'name', 'v1.0', 'author', 'email', 'desp', b58_payer,
                                                  gas_limit, gas_price)
        sdk.sign_transaction(tx, payer)
        res = sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(len(res), 64)

    def test_invoke_transaction(self):
        sdk.set_rpc(rpc_address)
        code = '54c56b6c766b00527ac46c766b51527ac4616c766b00c36c766b52527ac46c766b52c30548656c6c6f87630600621a' \
               '006c766b51c300c36165230061516c766b53527ac4620e00006c766b53527ac46203006c766b53c3616c756651c56b' \
               '6c766b00527ac46151c576006c766b00c3c461681553797374656d2e52756e74696d652e4e6f7469667961616c7566'
        abi_str = '{"hash":"0x362cb5608b3eca61d4846591ebb49688900fedd0","entrypoint":"Main","functions":[{' \
                  '"name":"Main","parameters":[{"name":"operation","type":"String"},{"name":"args","type":"Array"}],' \
                  '"returntype":"Any"},{"name":"Hello","parameters":[{"name":"msg","type":"String"}],' \
                  '"returntype":"Void"}],"events":[]} '
        abi = json.loads(abi_str)
        abi_info = AbiInfo(abi['hash'], abi['entrypoint'], abi['functions'], abi['events'])
        func = abi_info.get_function("Main")
        func.set_params_value(("Hello", "args"))
        contract_address = Address.address_from_vm_code(code).to_array()
        res = sdk.neo_vm().send_transaction(contract_address, None, None, 0, 0, func, True)
        self.assertEqual(res, '00')
        func = abi_info.get_function("Hello")
        func.set_params_value(("value",))
        res = sdk.neo_vm().send_transaction(contract_address, None, None, 0, 0, func, True)
        self.assertEqual(res, '01')


if __name__ == '__main__':
    unittest.main()

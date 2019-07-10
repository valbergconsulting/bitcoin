#!/usr/bin/env python3
# Copyright (c) 2014-2018 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test the listtransactionsfrom API."""
from decimal import Decimal
from io import BytesIO

from test_framework.messages import COIN, CTransaction
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import (
    assert_array_result,
    assert_equal,
    bytes_to_hex_str,
    hex_str_to_bytes,
    sync_mempools,
)

def tx_from_hex(hexstring):
    tx = CTransaction()
    f = BytesIO(hex_str_to_bytes(hexstring))
    tx.deserialize(f)
    return tx

class ListTransactionsFromTest(BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 2
        self.setup_clean_chain = True

    def skip_test_if_missing_module(self):
        self.skip_if_no_wallet()

    def run_test(self):
        self.nodes[0].generate(201)
        txid = self.nodes[0].sendtoaddress(self.nodes[1].getnewaddress(), 0.1)

        # First transaction should be the oldest, the first coinbase
        oldest = self.nodes[0].listtransactionsfrom()[0]
        assert(oldest['confirmations'] == 201)
        assert(oldest['category'] == 'generate')

        # If we skip the first, next oldest coinbase
        next_oldest = self.nodes[0].listtransactionsfrom("*", 100, 1)[0]
        assert(next_oldest['confirmations'] == 200)

        # If we list all, the last one should be the one we sent
        newest = self.nodes[0].listtransactionsfrom("*", 1000)[-1]
        assert(newest['txid'] == txid)
        assert(newest['category'] == "send")

if __name__ == '__main__':
    ListTransactionsFromTest().main()

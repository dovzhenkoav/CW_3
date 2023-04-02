from unittest import TestCase, main

from utils.classes import Transactions, Transaction
from utils.functions import read_json


class TransactionsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = read_json()

    def setUp(self):
        self.transactions = Transactions(self.data)

    def test_is_transactions(self):
        self.assertIsInstance(Transactions(self.data), Transactions)

    def test_check_atributes(self):
        self.assertIsInstance(self.transactions._data, list)
        self.assertIsInstance(self.transactions._sorted_data, list)

    def test_make_data(self):
        data: list = self.transactions._make_data(self.data)
        self.assertIsInstance(data, list)
        for element in data:
            self.assertIsInstance(element, Transaction)

    def test_sort_data(self):
        self.assertIsInstance(self.transactions._sort_data(self.transactions._data), list)

    def test_get_all_transactions_info(self):
        self.assertIsInstance(self.transactions.get_all_transactions_info(), str)

    def test_get_last_executed_transactions(self):
        self.assertIsInstance(self.transactions.get_last_executed_transactions(), str)

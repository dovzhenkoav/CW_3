from unittest import TestCase, main

from utils.classes import Transactions
from settings import PATH_TO_JSON


class TransactionsTest(TestCase):

    def setUp(self):
        self.transactions = Transactions(PATH_TO_JSON)

    def test_is_transactions(self):
        self.assertIsInstance(Transactions(PATH_TO_JSON), Transactions)

    def test_check_attributes(self):
        self.assertIsInstance(self.transactions._data, list)
        self.assertIsInstance(self.transactions._sorted_data, list)

    def test_sort_data(self):
        self.assertIsInstance(self.transactions._sort_data(self.transactions._data), list)

    def test_get_all_transactions_info(self):
        self.assertIsInstance(self.transactions.get_all_transactions_info(), str)

    def test_get_last_executed_transactions(self):
        self.assertIsInstance(self.transactions.get_last_executed_transactions(), str)


if __name__ == '__main__':
    main()

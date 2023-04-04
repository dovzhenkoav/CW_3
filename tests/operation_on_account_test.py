from unittest import TestCase, main

from operations_on_account import get_operations_on_account


class GetOperationsOnAccountTest(TestCase):
    def test_no_errors_on_start(self):
        self.assertEqual(get_operations_on_account(), None)


if __name__ == '__main__':
    main()

from unittest import TestCase, main

from utils.classes import Transaction


class TransactionTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.id_: int = 1234134563
        cls.state1: str = "EXECUTED"
        cls.state2: str = "CANCELLED"
        cls.date: str = '2019-08-26T10:50:58.294041'
        cls.operation_amount: dict = {"amount": "31957.58",
                                      "currency": {
                                          "name": "руб.",
                                          "code": "RUB"
                                      }}
        cls.description: str = "Перевод организации"

        cls.from1: str = "Maestro 1596837868705199"
        cls.from2: str = "Visa Classic 6831982476737658"
        cls.from3: str = ""

        cls.to1: str = "Maestro 1596837868705199"
        cls.to2: str = "Visa Classic 6831982476737658"
        cls.to3: str = "Счет 27248529432547658655"

    def setUp(self):
        self.transaction1 = Transaction(
            self.id_,
            self.state1,
            self.date,
            self.operation_amount,
            self.description,
            self.from1,
            self.to1
        )
        self.transaction2 = Transaction(
            self.id_,
            self.state2,
            self.date,
            self.operation_amount,
            self.description,
            self.from2,
            self.to2
        )
        self.transaction3 = Transaction(
            self.id_,
            self.state2,
            self.date,
            self.operation_amount,
            self.description,
            self.from3,
            self.to3
        )

    def test_is_transaction(self):
        self.assertIsInstance(self.transaction1, Transaction)

    def test_get_state(self):
        self.assertEqual(self.transaction1.get_state(), "EXECUTED")
        self.assertEqual(self.transaction2.get_state(), "CANCELLED")
        self.assertEqual(self.transaction3.get_state(), "CANCELLED")

    def test_parse_date(self):
        self.assertEqual(self.transaction1._parse_date(), "26:08:2019")
        self.assertEqual(self.transaction2._parse_date(), "26:08:2019")
        self.assertEqual(self.transaction3._parse_date(), "26:08:2019")

    def test_parse_from(self):
        self.assertEqual(self.transaction1._parse_from(self.from1), 'Maestro 1596 83** **** 5199')
        self.assertEqual(self.transaction2._parse_from(self.from2), 'Visa Classic 6831 98** **** 7658')
        with self.assertRaises(ValueError) as err:
            self.transaction3._parse_from(self.from3)
        self.assertEqual('В транзакции нет номера счета', err.exception.args[0])

    def test_hide_from_card_number(self):
        self.assertEqual(self.transaction1._hide_from_card_number(self.from1), 'Maestro 1596 83** **** 5199 -> ')
        self.assertEqual(self.transaction2._hide_from_card_number(self.from2), 'Visa Classic 6831 98** **** 7658 -> ')
        self.assertEqual(self.transaction3._hide_from_card_number(self.from3), "")

    def test_parse_to(self):
        self.assertEqual(self.transaction1._parse_to(self.to1), ('Maestro', '1596837868705199'))
        self.assertEqual(self.transaction2._parse_to(self.to2), ('Visa Classic', '6831982476737658'))
        self.assertEqual(self.transaction3._parse_to(self.to3), ('Счет', '27248529432547658655'))

    def test_hide_to_card_info(self):
        self.assertEqual(self.transaction1._hide_to_card_info(self.to1), 'Maestro **5199')
        self.assertEqual(self.transaction2._hide_to_card_info(self.to2), 'Visa Classic **7658')
        self.assertEqual(self.transaction3._hide_to_card_info(self.to3), 'Счет **8655')

    def test_show_transaction(self):
        self.assertEqual(self.transaction1.show_transaction(),
                         "26:08:2019 Перевод организации\nMaestro 1596 83** **** 5199 -> Maestro **5199\n31957.58 руб.\n\n")
        self.assertEqual(self.transaction2.show_transaction(),
                         "26:08:2019 Перевод организации\nVisa Classic 6831 98** **** 7658 -> Visa Classic **7658\n31957.58 руб.\n\n")
        self.assertEqual(self.transaction3.show_transaction(),
                         "26:08:2019 Перевод организации\nСчет **8655\n31957.58 руб.\n\n")


if __name__ == '__main__':
    main()

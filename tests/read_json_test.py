from unittest import TestCase, main
from utils.functions import read_json


class ReadJsonTest(TestCase):
    def test_has_file(self):
        self.assertIsInstance(read_json(), list)

    def test_is_json(self):
        output: list[dict] = read_json()
        for element in output:
            self.assertIsInstance(element, dict)


if __name__ == '__main__':
    main()

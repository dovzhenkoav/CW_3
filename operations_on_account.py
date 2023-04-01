from utils.functions import read_json
from utils.classes import Transactions


def get_operations_on_account():
    data = read_json()
    transactions = Transactions(data)
    print(transactions.get_last_executed_transactions(), end='')


if __name__ == '__main__':
    get_operations_on_account()

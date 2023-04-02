from utils.classes import Transactions
from settings import PATH_TO_JSON


def get_operations_on_account():
    transactions = Transactions(PATH_TO_JSON)
    print(transactions.get_last_executed_transactions(), end='')


if __name__ == '__main__':
    get_operations_on_account()

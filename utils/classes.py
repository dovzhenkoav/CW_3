from datetime import datetime


class Transaction:
    def __init__(self, id: int, state: str, date: str,
                 operation_amount: dict, description: str,
                 from_: str, to: str):
        self._id: int = id
        self._state: str = state
        self._date: str = self._parse_date(date)
        self._operation_amount: dict = operation_amount
        self._description: str = description

        self._from: str = from_
        self._to: str = to
        self._hidden_from_card_number = self._hide_from_card_number(self._from)
        self._hidden_to_card_info = self._hide_to_card_info(self._to)

    def _parse_date(self, date: str) -> str:
        datetime_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
        return datetime_date.strftime('%d:%m:%Y')


    def _parse_from(self, info: str) -> str:

        splitted_from = info.split()
        for i in splitted_from:
            if i.isdigit():
                operation_number = i
                splitted_from.remove(operation_number)
                operation_cardname = " ".join(splitted_from)

                return f'{operation_cardname} {operation_number[:4]} {operation_number[4:6]}** **** {operation_number[-4:]}'
        raise ValueError('В транзакции нет номера счета')


    def _hide_from_card_number(self, number: str) -> str:
        if number:
            info = self._parse_from(number)
            return f'{info} -> '
        else:
            return ''

    def _parse_to(self, to: str) -> tuple[str, str]:
        splitted_to = to.split()
        for i in splitted_to:
            if i.isdigit():
                operation_number = i
                splitted_to.remove(operation_number)
                operation_cardname = " ".join(splitted_to)

                return operation_cardname, operation_number

    def _hide_to_card_info(self, card_info: str) -> str:
        card_desc, card_num = self._parse_to(card_info)
        # return f'{self._to[0]} **{self._to[1][-4:]}'
        return f'{card_desc} **{card_num[-4:]}'

    def show_transaction(self):
        return f'{self._date} {self._description}\n' \
               f'{self._hidden_from_card_number}{self._hidden_to_card_info}\n' \
               f'{self._operation_amount["amount"]} {self._operation_amount["currency"]["name"]}\n\n'

class Transactions:
    def __init__(self, data: list[dict]):
        self._data: list[Transaction] = self._make_data(data)

    def _make_data(self, data: list[dict]) -> list[Transaction]:
        all_entries = []

        for entry in data:
            if entry:
                try:
                    entry['from']
                except KeyError:
                    entry['from'] = ''

                all_entries.append(Transaction(
                    id=entry['id'],
                    state=entry['state'],
                    date=entry['date'],
                    operation_amount=entry['operationAmount'],
                    description=entry['description'],
                    from_=entry['from'],
                    to=entry['to'],
                    ))
        return all_entries

    def get_transactions_info(self):
        transactions_log = ''
        for transaction in self._data:
            transactions_log += transaction.show_transaction()
        return transactions_log

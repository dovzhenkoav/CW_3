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

        self._from: tuple[str] = self._parse_from(from_)
        self._to: tuple[str] = self._parse_to(to)
        self._formated_from_card_number = self._format_from_card_number(self._from[1])
        self._formated_to_card_number = self._format_to_card_number(self._to[1])

    def _parse_date(self, date: str) -> str:
        datetime_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
        return datetime_date.strftime('%d:%m:%Y')

    def _parse_from(self, from_: str) -> tuple[str]:
        splitted_from = from_.split()
        for i in splitted_from:
            if i.isdigit():
                operation_number = i
                splitted_from.remove(operation_number)
                operation_cardname = " ".join(splitted_from)

        return tuple([operation_cardname, operation_number])

    def _parse_to(self, to: str) -> tuple[str]:
        operation_cardname = ''
        operation_number = ''
        splitted_to = to.split()
        for i in splitted_to:
            if i.isdigit():
                operation_number = i
                splitted_to.remove(operation_number)
                operation_cardname = " ".join(splitted_to)

        return tuple([operation_cardname, operation_number])


    def _format_from_card_number(self, number: str) -> str:
        return f'{number[:4]} {number[4:6]}** **** {number[-4:]}'

    def _format_to_card_number(self, number: str) -> str:
        return f'{self._to[0]} **{self._to[1][-4:]}'

    def show_transaction(self):
        return f'{self._date} {self._description}\n' \
               f'{self._from[0]} {self._formated_from_card_number} -> {self._formated_to_card_number}\n' \
               f'{self._operation_amount["amount"]} {self._operation_amount["currency"]["name"]}\n'



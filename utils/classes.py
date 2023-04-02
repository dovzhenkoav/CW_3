from datetime import datetime
import json


class Transaction:
    """Класс, описывающий представление каждой транзакции"""
    def __init__(self, id: int, state: str, date: str,
                 operation_amount: dict, description: str,
                 from_: str, to: str):
        self._id: int = id
        self._state: str = state
        self._date: str = date
        self._operation_amount: dict = operation_amount
        self._description: str = description

        self._from: str = from_
        self._to: str = to
        self._hidden_from_card_number = self._hide_from_card_number(self._from)
        self._hidden_to_card_info = self._hide_to_card_info(self._to)

    def get_state(self):
        """Геттер для получения статуса операции"""
        return self._state

    def _parse_date(self) -> str:
        """Парсим дату транзакции из длинного представления в короткое под формат %d:%m:%Y"""
        datetime_date = datetime.strptime(self._date, '%Y-%m-%dT%H:%M:%S.%f')
        return datetime_date.strftime('%d:%m:%Y')

    def _parse_from(self, info: str) -> str:
        """Вспомогательная функция для _hide_from_card_number()"""
        splitted_from = info.split()
        for i in splitted_from:
            if i.isdigit():
                operation_number = i
                splitted_from.remove(operation_number)
                operation_cardname = " ".join(splitted_from)

                return f'{operation_cardname} {operation_number[:4]} {operation_number[4:6]}** **** {operation_number[-4:]}'
        raise ValueError('В транзакции нет номера счета')

    def _hide_from_card_number(self, number: str) -> str:
        """Скрываем номер карты/счета отправителя или убираем информацию, если его нет"""
        if number:
            info = self._parse_from(number)
            return f'{info} -> '
        else:
            return ''

    def _parse_to(self, to: str) -> tuple[str, str]:
        """Вспомогательная функция для метода _hide_to_card_info()"""
        splitted_to = to.split()
        for i in splitted_to:
            if i.isdigit():
                operation_number = i
                splitted_to.remove(operation_number)
                operation_cardname = " ".join(splitted_to)

                return operation_cardname, operation_number

    def _hide_to_card_info(self, card_info: str) -> str:
        """Скрываем номер счета/карты получателя"""
        card_desc, card_num = self._parse_to(card_info)
        return f'{card_desc} **{card_num[-4:]}'

    def show_transaction(self):
        """Вывод строки, описывающий всю информацию о транзакции"""
        return f'{self._parse_date()} {self._description}\n' \
               f'{self._hidden_from_card_number}{self._hidden_to_card_info}\n' \
               f'{self._operation_amount["amount"]} {self._operation_amount["currency"]["name"]}\n\n'


class Transactions:
    """Класс, реализующий функциональность взаимодействия с транзакциями"""
    def __init__(self, path: str):
        self._json: list[dict] = self._load_json(path)
        self._data: list[Transaction] = self._make_data(self._json)
        self._sorted_data = self._sort_data(self._data)
        self.number_of_recent_transaction = 5

    def _load_json(self, path: str):
        """Преобразовываем файл JSON в привычный для питона формат(list[dict]) и загоняем в атрибут self._json"""
        with open(path, mode='r', encoding='utf-8') as file:
            return json.load(file)

    def _make_data(self, data: list[dict]) -> list[Transaction]:
        """Каждую транзакцию в self._json описываем в представлении типа Transaction. Все транзакции собираются в список"""
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

    def _sort_data(self, data):
        """Транзакции сортируются по дате от новых к старым"""
        return sorted(data, key=lambda entry: entry._date, reverse=True)

    def get_all_transactions_info(self):
        """Метод для показа вообще всех транзакций пользователя"""
        transactions_log = ''
        for transaction in self._sorted_data:
            transactions_log += transaction.show_transaction()
        return transactions_log

    def get_last_executed_transactions(self):
        """Метод для показа конкретного числа последних транзакций"""
        recent_log = [transaction for transaction in self._sorted_data if transaction.get_state() == 'EXECUTED'][
                     :self.number_of_recent_transaction]
        transactions_log = ''
        for transaction in recent_log:
            transactions_log += transaction.show_transaction()
        return transactions_log

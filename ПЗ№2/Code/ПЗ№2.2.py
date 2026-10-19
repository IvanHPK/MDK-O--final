class Deposit:
    def __init__(self, first=1, second=1, years=1):
        self.first = first
        self.second = second
        self.years = years

    @property
    def first(self):
        return self.__first

    @first.setter
    def first(self, value):
        if value <= 0:
            raise ValueError("Сумма вклада должна быть положительной")
        self.__first = value

    @property
    def second(self):
        return self.__second

    @second.setter
    def second(self, value):
        if value <= 0:
            raise ValueError("Процентная ставка должна быть положительной")
        self.__second = value

    @property
    def years(self):
        return self.__years

    @years.setter
    def years(self, value):
        if value <= 0:
            raise ValueError("Срок вклада должен быть положительным")
        self.__years = value

    def read(self):
        try:
            self.first = float(input("Введите сумму вклада: "))
            self.second = float(input("Введите процентную ставку: "))
            self.years = float(input("Введите срок вклада в годах: "))
        except ValueError as e:
            print("Ошибка:", e)

    def final_amount(self):
        return self.first * (1 + self.second / 100) ** self.years

    def profit(self):
        return self.final_amount() - self.first

    def display(self):
        print("Начальная сумма:", self.first)
        print("Процентная ставка:", self.second)
        print("Срок вклада:", self.years)
        print("Итоговая сумма:", self.final_amount())
        print("Чистая прибыль:", self.profit())


deposit = Deposit()
deposit.read()
deposit.display()

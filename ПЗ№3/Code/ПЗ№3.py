# Собственные исключения
class InvalidSystemsCountError(ValueError):
    pass


class InvalidHoursError(ValueError):
    pass


# Обычный базовый класс
class SecurityIncident:
    base_severity = 0
    title = "Инцидент ИБ"

    def __init__(self, incident_id, affected_systems, hours_since_detected):
        self.incident_id = incident_id
        self.affected_systems = affected_systems
        self.hours_since_detected = hours_since_detected
        self.weight = self.calculate_weight(
            affected_systems, hours_since_detected
        )

    def check_data(self, affected_systems, hours_since_detected):
        if type(affected_systems) != int or affected_systems < 1:
            raise InvalidSystemsCountError(
                "Количество систем должно быть целым числом не меньше 1."
            )

        if hours_since_detected < 0:
            raise InvalidHoursError(
                "Количество часов не может быть отрицательным."
            )

    def calculate_weight(self, affected_systems, hours_since_detected):
        self.check_data(affected_systems, hours_since_detected)
        return 0

    def get_criticality(self):
        if self.weight >= 50:
            return "CRITICAL"
        elif self.weight >= 20:
            return "HIGH"
        elif self.weight >= 5:
            return "MEDIUM"
        else:
            return "LOW"

    def __str__(self):
        return (
            f"{self.title} №{self.incident_id}: вес = {self.weight}, "
            f"критичность = {self.get_criticality()}"
        )

    def __repr__(self):
        return f"{self.title}(id={self.incident_id}, weight={self.weight})"

    def __eq__(self, other):
        return self.incident_id == other.incident_id

    def __lt__(self, other):
        return self.weight < other.weight

    def __add__(self, other):
        return self.weight + other.weight


# Классы-наследники переопределяют calculate_weight
class DDoSAttack(SecurityIncident):
    base_severity = 10
    title = "DDoS-атака"

    def calculate_weight(self, affected_systems, hours_since_detected):
        self.check_data(affected_systems, hours_since_detected)
        return self.base_severity * affected_systems * (1 + hours_since_detected / 24)


class Phishing(SecurityIncident):
    base_severity = 3
    title = "Фишинг"

    def calculate_weight(self, affected_systems, hours_since_detected):
        self.check_data(affected_systems, hours_since_detected)
        return self.base_severity * affected_systems * (1 + hours_since_detected / 24)


class DataLeak(SecurityIncident):
    base_severity = 8
    title = "Утечка данных"

    def calculate_weight(self, affected_systems, hours_since_detected):
        self.check_data(affected_systems, hours_since_detected)
        return self.base_severity * affected_systems * (1 + hours_since_detected / 24)


# Класс-контейнер
class IncidentQueue:
    def __init__(self):
        self.incidents = []

    def add(self, incident):
        self.incidents.append(incident)

    def __len__(self):
        return len(self.incidents)

    def __getitem__(self, index):
        return self.incidents[index]


# Демонстрация работы
if __name__ == "__main__":
    ddos = DDoSAttack(1, 3, 12)
    phishing = Phishing(2, 1, 0)
    leak = DataLeak(3, 5, 48)

    queue = IncidentQueue()
    queue.add(ddos)
    queue.add(phishing)
    queue.add(leak)

    print("Исходная очередь:")
    for incident in queue:
        print(incident)

    print("\nПо убыванию веса:")
    for incident in sorted(queue, reverse=True):
        print(incident)

    print("\nПолиморфизм — вызов одного метода у разных объектов:")
    for incident in queue:
        weight = incident.calculate_weight(
            incident.affected_systems, incident.hours_since_detected
        )
        print(incident.title, "— вес:", weight)

    print("\nОтладочный вывод:", repr(ddos))
    print("Сравнение разных ID:", ddos == phishing)
    print("Сравнение одинаковых ID:", ddos == DDoSAttack(1, 3, 12))
    print("Сумма весов:", ddos + phishing)
    print("Количество инцидентов:", len(queue))
    print("Первый инцидент:", queue[0])

    print("\nПроверка исключений:")
    try:
        DDoSAttack(4, 0, 5)
    except InvalidSystemsCountError as error:
        print("Ошибка:", error)

    try:
        Phishing(5, 1, -2)
    except InvalidHoursError as error:
        print("Ошибка:", error)
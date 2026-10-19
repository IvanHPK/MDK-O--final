class StorageMonitor:
    """Singleton: единый монитор свободного места на дисках."""

    _instance = None  # здесь хранится единственный экземпляр

    def __new__(cls):
        # Создаём объект только при первом обращении
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.disks = {}  # словарь дисков: имя -> данные
        return cls._instance

    def add_disk(self, disk_name, free_gb, total_gb):
        """Добавить или обновить данные о диске."""
        # Проверка корректности входных данных
        if not disk_name:
            raise ValueError("Название диска не может быть пустым.")
        if total_gb <= 0:
            raise ValueError("Общий объём должен быть больше нуля.")
        if free_gb < 0 or free_gb > total_gb:
            raise ValueError("Свободное место должно быть от 0 до общего объёма.")

        self.disks[disk_name] = {
            "free_gb": free_gb,
            "total_gb": total_gb,
        }

    def free_percent(self, disk_name):
        """Вернуть процент свободного места на диске."""
        disk = self.disks[disk_name]
        return round(disk["free_gb"] / disk["total_gb"] * 100, 1)

    def get_all_disks(self):
        """Вернуть словарь всех дисков."""
        return self.disks
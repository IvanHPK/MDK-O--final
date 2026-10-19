from django.test import SimpleTestCase
from .singleton import StorageMonitor


class SingletonTest(SimpleTestCase):
    """Тесты паттерна Singleton."""

    def test_only_one_instance(self):
        """Проверяем, что два вызова возвращают один и тот же объект."""
        m1 = StorageMonitor()
        m2 = StorageMonitor()
        self.assertIs(m1, m2)

    def test_disks_are_shared(self):
        """Проверяем, что данные общие для всех экземпляров."""
        m1 = StorageMonitor()
        m1.add_disk("Z:", 50, 100)
        m2 = StorageMonitor()
        self.assertIn("Z:", m2.get_all_disks())

    def test_validation_rejects_empty_name(self):
        """Проверяем, что пустое имя диска отклоняется."""
        monitor = StorageMonitor()
        with self.assertRaises(ValueError):
            monitor.add_disk("", 10, 100)

    def test_validation_rejects_bad_total(self):
        """Проверяем, что нулевой общий объём отклоняется."""
        monitor = StorageMonitor()
        with self.assertRaises(ValueError):
            monitor.add_disk("X:", 10, 0)
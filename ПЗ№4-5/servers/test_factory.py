from django.test import SimpleTestCase
from .models import (
    AlertFactory,
    WarningAlert,
    CriticalAlert,
    EmergencyAlert,
)


class FactoryTest(SimpleTestCase):
    """Тесты паттерна Factory."""

    def test_creates_warning_by_name(self):
        a = AlertFactory.create("warning", "C:", 30)
        self.assertIsInstance(a, WarningAlert)

    def test_creates_critical_by_name(self):
        a = AlertFactory.create("critical", "C:", 15)
        self.assertIsInstance(a, CriticalAlert)

    def test_creates_emergency_by_name(self):
        a = AlertFactory.create("emergency", "C:", 3)
        self.assertIsInstance(a, EmergencyAlert)

    def test_unknown_type_raises(self):
        """Фабрика должна выбрасывать ValueError на неизвестный тип."""
        with self.assertRaises(ValueError):
            AlertFactory.create("unknown", "C:", 50)

    def test_auto_warning(self):
        a = AlertFactory.create_by_free_space("C:", 30)
        self.assertIsInstance(a, WarningAlert)

    def test_auto_critical(self):
        a = AlertFactory.create_by_free_space("C:", 15)
        self.assertIsInstance(a, CriticalAlert)

    def test_auto_emergency(self):
        a = AlertFactory.create_by_free_space("C:", 7)
        self.assertIsInstance(a, EmergencyAlert)
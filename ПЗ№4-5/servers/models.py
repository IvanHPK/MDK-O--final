from django.db import models

class Alert:
    """Базовый класс алерта. Все алерты умеют get_info()."""

    level = "UNKNOWN"

    def __init__(self, disk_name, free_percent):
        self.disk_name = disk_name
        self.free_percent = free_percent

    def get_info(self):
        raise NotImplementedError("Переопредели метод в наследнике")


class WarningAlert(Alert):
    level = "WARNING"

    def get_info(self):
        return f"[{self.level}] Диск {self.disk_name}: свободно {self.free_percent}% — следите за местом"


class CriticalAlert(Alert):
    level = "CRITICAL"

    def get_info(self):
        return f"[{self.level}] Диск {self.disk_name}: свободно {self.free_percent}% — срочно нужно место!"


class EmergencyAlert(Alert):
    level = "EMERGENCY"

    def get_info(self):
        return f"[{self.level}] Диск {self.disk_name}: свободно {self.free_percent}% — КРИТИЧНО!"


class AlertFactory:
    """Factory: создаёт алерт по типу или по проценту свободного места."""

    _registry = {
        "warning": WarningAlert,
        "critical": CriticalAlert,
        "emergency": EmergencyAlert,
    }

    @classmethod
    def create(cls, alert_type, disk_name, free_percent):
        if alert_type not in cls._registry:
            raise ValueError(f"Неизвестный тип алерта: {alert_type}")
        return cls._registry[alert_type](disk_name, free_percent)

    @classmethod
    def create_by_free_space(cls, disk_name, free_percent):
        if free_percent >= 20:
            alert_type = "warning"
        elif free_percent >= 10:
            alert_type = "critical"
        else:
            alert_type = "emergency"
        return cls.create(alert_type, disk_name, free_percent)
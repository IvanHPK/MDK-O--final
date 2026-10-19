from django.http import HttpResponse
from .singleton import StorageMonitor
from .models import AlertFactory


def index(request):
    """Главная страница: демонстрация Singleton и Factory."""
    monitor = StorageMonitor()

    lines = ["<h1>Мониторинг свободного места</h1>"]

    try:
        # Заполняем дисками только при первом заходе,
        # чтобы не перезаписывать существующие данные
        if not monitor.get_all_disks():
            monitor.add_disk("C:", 15, 100)
            monitor.add_disk("D:", 300, 1000)
            monitor.add_disk("E:", 2, 500)

        # Singleton: список дисков с процентом свободного места
        lines.append("<h2>Диски</h2><ul>")
        for name, info in monitor.get_all_disks().items():
            pct = monitor.free_percent(name)
            lines.append(
                f"<li>{name}: {info['free_gb']} ГБ из {info['total_gb']} ГБ ({pct}%)</li>"
            )
        lines.append("</ul>")

        # Singleton: доказательство того, что объект один и тот же
        monitor2 = StorageMonitor()
        lines.append(f"<p>Один и тот же объект? <b>{monitor is monitor2}</b></p>")

        # Factory: алерты для каждого диска
        lines.append("<h2>Алерты</h2><ul>")
        for name in monitor.get_all_disks():
            pct = monitor.free_percent(name)
            alert = AlertFactory.create_by_free_space(name, pct)
            lines.append(f"<li>{alert.get_info()}</li>")
        lines.append("</ul>")

    except ValueError as e:
        # Ошибка в данных — показываем сообщение пользователю
        lines.append(f"<p style='color:red'>Ошибка: {e}</p>")

    except Exception as e:
        # Любая другая непредвиденная ошибка
        lines.append(f"<p style='color:red'>Непредвиденная ошибка: {e}</p>")

    return HttpResponse("".join(lines))


def alerts(request):
    """Вторая страница: только список алертов."""
    monitor = StorageMonitor()

    lines = ["<h1>Текущие алерты</h1><ul>"]

    try:
        for name in monitor.get_all_disks():
            pct = monitor.free_percent(name)
            alert = AlertFactory.create_by_free_space(name, pct)
            lines.append(f"<li>{alert.get_info()}</li>")

    except ValueError as e:
        lines.append(f"<li style='color:red'>Ошибка: {e}</li>")

    except Exception as e:
        lines.append(f"<li style='color:red'>Непредвиденная ошибка: {e}</li>")

    lines.append("</ul>")

    return HttpResponse("".join(lines))
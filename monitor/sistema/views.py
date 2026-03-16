import os
import platform
from typing import Any, Dict

from django.shortcuts import render
from django.utils import timezone

try:
    import psutil
except ImportError:
    psutil = None

GB_DIVISOR = 1024 ** 3
AUTO_REFRESH_SECONDS = 15
DISK_PATH = os.path.abspath(os.sep)


DataPoint = Dict[str, Any]


def _bytes_to_gb(value: int) -> float:
    return round(value / GB_DIVISOR, 2)


def dashboard(request):
    context_errors: list[str] = []
    cpu_data: DataPoint = {'usage': None, 'error': None}
    memory_data: DataPoint = {'total': None, 'used': None, 'available': None, 'percent': None, 'error': None}
    disk_data: DataPoint = {'mountpoint': DISK_PATH, 'total': None, 'used': None, 'free': None, 'percent': None, 'error': None}
    core_data: DataPoint = {'logical': None, 'physical': None, 'error': None}

    if not psutil:
        context_errors.append('La librería psutil no está disponible en este entorno. Instala las dependencias para mostrar métricas reales.')
        mapped_error = 'psutil no disponible'
        cpu_data['error'] = mapped_error
        memory_data['error'] = mapped_error
        disk_data['error'] = mapped_error
        core_data['error'] = mapped_error
    else:
        try:
            cpu_data['usage'] = psutil.cpu_percent(interval=0.4)
        except Exception as exc:  # pragma: no cover
            cpu_data['error'] = str(exc)
            context_errors.append(f'No se pudo obtener el uso de CPU: {exc}')
        try:
            mem = psutil.virtual_memory()
            memory_data.update(
                total=_bytes_to_gb(mem.total),
                used=_bytes_to_gb(mem.used),
                available=_bytes_to_gb(mem.available),
                percent=round(mem.percent, 1),
            )
        except Exception as exc:  # pragma: no cover
            memory_data['error'] = str(exc)
            context_errors.append(f'No se pudo obtener la memoria RAM: {exc}')
        try:
            disk = psutil.disk_usage(DISK_PATH)
            disk_data.update(
                total=_bytes_to_gb(disk.total),
                used=_bytes_to_gb(disk.used),
                free=_bytes_to_gb(disk.free),
                percent=round(disk.percent, 1),
            )
        except Exception as exc:  # pragma: no cover
            disk_data['error'] = str(exc)
            context_errors.append(f'No se pudo obtener el disco ({DISK_PATH}): {exc}')
        try:
            core_data['logical'] = psutil.cpu_count(logical=True)
            core_data['physical'] = psutil.cpu_count(logical=False)
        except Exception as exc:  # pragma: no cover
            core_data['error'] = str(exc)
            context_errors.append(f'No se pudo determinar el conteo de núcleos: {exc}')

    platform_data = platform.uname()
    system_info = {
        'os': platform_data.system,
        'node': platform_data.node,
        'release': platform_data.release,
        'version': platform_data.version,
        'architecture': platform_data.machine,
        'processor': platform_data.processor or 'No disponible',
    }

    context = {
        'cpu': cpu_data,
        'memory': memory_data,
        'disk': disk_data,
        'system': system_info,
        'cores': core_data,
        'psutil_available': psutil is not None,
        'timestamp': timezone.now(),
        'errors': context_errors,
        'auto_refresh_seconds': AUTO_REFRESH_SECONDS,
    }
    return render(request, 'sistema/dashboard.html', context)

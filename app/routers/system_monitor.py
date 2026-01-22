from fastapi import APIRouter, HTTPException
import psutil
import time
from datetime import timedelta
import platform
import os

router = APIRouter(
    prefix="/system",
    tags=["System Monitoring"]
)

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

@router.get("/status")
async def get_system_status():
    try:
        # CPU
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_freq = psutil.cpu_freq()
        cpu_count = psutil.cpu_count(logical=True)
        
        # Memory
        svmem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        # Disk
        disk_partitions = psutil.disk_partitions()
        disk_usage = psutil.disk_usage('/')
        
        # Uptime
        boot_time_timestamp = psutil.boot_time()
        bt = time.time() - boot_time_timestamp
        uptime = str(timedelta(seconds=bt))
        
        # Service Checks (Basic process check)
        services = {
            "nginx": "stopped",
            "postgres": "stopped",
            "fastapi": "running" # Self check
        }
        
        for proc in psutil.process_iter(['name']):
            try:
                if 'nginx' in proc.info['name']:
                    services['nginx'] = 'active'
                if 'postgres' in proc.info['name']:
                    services['postgres'] = 'active'
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return {
            "system": {
                "os": f"{platform.system()} {platform.release()}",
                "cpu": {
                    "usage_percent": cpu_usage,
                    "count_logical": cpu_count,
                    "frequency_current": f"{cpu_freq.current:.2f}Mhz" if cpu_freq else "N/A"
                },
                "memory": {
                    "total": get_size(svmem.total),
                    "available": get_size(svmem.available),
                    "used": get_size(svmem.used),
                    "percent": svmem.percent,
                    "used_gb": round(svmem.used / (1024**3), 2),
                    "total_gb": round(svmem.total / (1024**3), 2)
                },
                "disk_root": {
                    "total": get_size(disk_usage.total),
                    "used": get_size(disk_usage.used),
                    "free": get_size(disk_usage.free),
                    "percent": disk_usage.percent,
                    "free_gb": round(disk_usage.free / (1024**3), 2)
                },
                "uptime": uptime
            },
            "services": services
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

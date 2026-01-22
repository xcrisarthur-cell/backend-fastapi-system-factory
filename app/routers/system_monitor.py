from fastapi import APIRouter, HTTPException
import psutil
import shutil
import time
import subprocess
from datetime import timedelta

router = APIRouter(
    prefix="/system",
    tags=["System Monitor"]
)

def get_service_status(service_name: str) -> str:
    """Check if a systemd service is active."""
    try:
        # Run systemctl is-active [service_name]
        result = subprocess.run(
            ["systemctl", "is-active", service_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"

def bytes_to_gb(bytes_value):
    """Convert bytes to GB with 2 decimal places."""
    return round(bytes_value / (1024 ** 3), 2)

@router.get("/status")
async def get_system_status():
    try:
        # 1. CPU Usage
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # 2. Memory (RAM)
        memory = psutil.virtual_memory()
        ram_total_gb = bytes_to_gb(memory.total)
        ram_used_gb = bytes_to_gb(memory.used)
        ram_available_gb = bytes_to_gb(memory.available)
        ram_percent = memory.percent

        # 3. Disk Usage (Root Partition)
        disk = shutil.disk_usage("/")
        disk_total_gb = bytes_to_gb(disk.total)
        disk_used_gb = bytes_to_gb(disk.used)
        disk_free_gb = bytes_to_gb(disk.free)
        disk_percent = round((disk.used / disk.total) * 100, 1)

        # 4. System Uptime
        uptime_seconds = time.time() - psutil.boot_time()
        uptime_string = str(timedelta(seconds=int(uptime_seconds)))

        # 5. Services Status (Only works on Linux with systemd)
        services = {
            "nginx": get_service_status("nginx"),
            "postgresql": get_service_status("postgresql"),
            "fastapi_app": get_service_status("fastapi_app")
        }

        return {
            "status": "success",
            "timestamp": int(time.time()),
            "system": {
                "cpu": {
                    "usage_percent": cpu_percent,
                    "count_logical": psutil.cpu_count(),
                    "count_physical": psutil.cpu_count(logical=False)
                },
                "memory": {
                    "total_gb": ram_total_gb,
                    "used_gb": ram_used_gb,
                    "available_gb": ram_available_gb,
                    "percent": ram_percent
                },
                "disk_root": {
                    "total_gb": disk_total_gb,
                    "used_gb": disk_used_gb,
                    "free_gb": disk_free_gb,
                    "percent": disk_percent
                },
                "uptime": uptime_string
            },
            "services": services
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

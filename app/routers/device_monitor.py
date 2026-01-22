from fastapi import APIRouter
import socket
import asyncio
from concurrent.futures import ThreadPoolExecutor

router = APIRouter(
    prefix="/devices",
    tags=["Device Monitor"]
)

# Daftar perangkat dari file listFp&DVR.txt
DEVICES = [
    # Fingerprints
    {"name": "FP OFFICE (Local)", "host": "172.16.0.18", "port": 4370, "group": "Fingerprint"},
    {"name": "FP OFFICE (Public)", "host": "103.164.99.2", "port": 4, "group": "Fingerprint"},
    
    {"name": "FP KAWAT (Local)", "host": "172.16.0.17", "port": 4370, "group": "Fingerprint"},
    {"name": "FP KAWAT (Public)", "host": "103.164.99.2", "port": 3, "group": "Fingerprint"},
    
    {"name": "FP ACS/QCR (Local)", "host": "172.16.0.16", "port": 4370, "group": "Fingerprint"},
    {"name": "FP ACS/QCR (Public)", "host": "103.164.99.2", "port": 2, "group": "Fingerprint"},
    
    {"name": "FP PRINTSEWING/QC (Local)", "host": "172.16.0.15", "port": 4370, "group": "Fingerprint"},
    {"name": "FP PRINTSEWING/QC (Public)", "host": "103.164.99.2", "port": 1, "group": "Fingerprint"},
    
    {"name": "FP PEKANBARU", "host": "103.183.14.82", "port": 11043, "group": "Fingerprint"},

    # DVRs
    {"name": "DVR HRD BEKASI", "host": "103.164.99.2", "port": 11011, "group": "DVR"},
    {"name": "DVR PPIC BEKASI", "host": "103.164.99.2", "port": 11012, "group": "DVR"},
    {"name": "DVR SECURITY BEKASI", "host": "103.164.99.2", "port": 11013, "group": "DVR"},
    {"name": "DVR PRODUKSI 1 BEKASI", "host": "103.164.99.2", "port": 11014, "group": "DVR"},
    {"name": "DVR GUDANG JADI BEKASI", "host": "103.164.99.2", "port": 11015, "group": "DVR"},
    {"name": "DVR PRODUKSI 2 BEKASI", "host": "103.164.99.2", "port": 11016, "group": "DVR"}, # Asumsi baris 35 adalah unit ke-2
    {"name": "DVR KAWAT BEKASI", "host": "103.164.99.2", "port": 11017, "group": "DVR"},
    {"name": "DVR ICU + BANTAL BEKASI", "host": "103.164.99.2", "port": 11018, "group": "DVR"},
    
    {"name": "DVR PRODUKSI BANDUNG", "host": "36.93.215.10", "port": 11021, "group": "DVR"},
    {"name": "DVR OFFICE BANDUNG", "host": "36.93.215.10", "port": 11022, "group": "DVR"},
    
    {"name": "DVR OFFICE PEKANBARU", "host": "103.183.14.82", "port": 11042, "group": "DVR"},
    {"name": "DVR PRODUKSI PEKANBARU", "host": "103.183.14.82", "port": 11041, "group": "DVR"},
]

def check_connection(host: str, port: int, timeout: int = 2) -> bool:
    """Check if a TCP port is open"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except Exception:
        return False

@router.get("/status")
async def get_devices_status():
    loop = asyncio.get_running_loop()
    
    # Gunakan ThreadPoolExecutor untuk menjalankan socket blocking secara paralel
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for device in DEVICES:
            futures.append(
                loop.run_in_executor(
                    executor, 
                    check_connection, 
                    device["host"], 
                    device["port"]
                )
            )
        
        results = await asyncio.gather(*futures)
    
    # Gabungkan hasil dengan data device
    response_data = []
    for i, device in enumerate(DEVICES):
        response_data.append({
            "name": device["name"],
            "host": device["host"],
            "port": device["port"],
            "group": device["group"],
            "status": "online" if results[i] else "offline"
        })
        
    return response_data

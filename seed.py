
import os
import sys
import csv
import re
import argparse
from decimal import Decimal
from datetime import datetime, timedelta
import random
from faker import Faker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal, engine, Base
from app.models import (
    Division, Department, Position, SubPosition,
    Worker, Shift, Supplier, Item, ProblemComment,
    ProductionLog, ProductionLogProblemComment,
    ProductionTarget, Attendance, AttendanceStatus
)
from app.security import hash_password

fake = Faker('id_ID')  # Indonesian locale
Faker.seed(42)  # Set seed for reproducibility
random.seed(42)


def get_priority_data():
    """Get priority data directly embedded"""
    return {
        'divisions': [
            'Kawat',
            'Rangka',
            'Bantal',
            'IT'
        ],
        'departments': [
            'Operator',
            'Koordinator',
            'Supervisor',
            'Admin Produksi',
            'Superadmin'
        ],
        'positions': [
            {'code': 'PER', 'unit': 'pcs', 'name': 'Per'},
            {'code': 'RAM', 'unit': 'lmbr', 'name': 'Ram'},
            {'code': 'TEMBAK_KAWAT', 'unit': 'lmbr', 'name': 'Tembak(Kawat)'},
            {'code': 'POCKET', 'unit': 'pcs', 'name': 'Pocket'},
            {'code': 'ASSEMBLY', 'unit': 'lmbr', 'name': 'Assembly'},
            {'code': 'FRAME', 'unit': 'pcs', 'name': 'Frame'},
            {'code': 'SUPPLY', 'unit': 'lmbr', 'name': 'Supply'},
            {'code': 'POTONG', 'unit': 'pcs', 'name': 'Potong'},
            {'code': 'TEMBAK_RANGKA', 'unit': 'lmbr', 'name': 'Tembak(Rangka)'},
            {'code': 'FG', 'unit': 'pcs', 'name': 'Finish Good(FG)'},
            {'code': 'PRP', 'unit': 'pcs', 'name': 'PRP'},
            {'code': 'ISI', 'unit': 'pcs', 'name': 'ISI'},
            {'code': 'JAHIT', 'unit': 'pcs', 'name': 'Jahit'},
            {'code': 'PACKING', 'unit': 'pcs', 'name': 'Packing'},
        ],
        'sub_positions': [
            {'code': 'FC60', 'position_code': 'PER'},
            {'code': 'SX80', 'position_code': 'PER'},
            {'code': 'SX80i', 'position_code': 'PER'},
            {'code': 'SX80iS', 'position_code': 'PER'},
            {'code': 'SX200', 'position_code': 'RAM'},
            {'code': 'AS3-NEW', 'position_code': 'RAM'},
            {'code': 'AS3-OLD', 'position_code': 'RAM'},
            {'code': 'MEJA-1', 'position_code': 'TEMBAK_KAWAT'},
            {'code': 'MEJA-2', 'position_code': 'TEMBAK_KAWAT'},
            {'code': 'MEJA-3', 'position_code': 'TEMBAK_KAWAT'},
            {'code': 'LSPR180', 'position_code': 'POCKET'},
            {'code': 'LSPR-NEW', 'position_code': 'POCKET'},
            {'code': 'LSPR-OLD', 'position_code': 'POCKET'},
        ],
        'shifts': [
            'Shift 1',
            'Shift 2',
            'Shift 3'
        ],
        'suppliers': [
            'Intiroda',
            'Mega',
            'Kingdom'
        ],
        'workers': [
            # Existing workers updated with new codes if needed
            {'name': 'Slamet Purnomo', 'position_code': 'PER', 'department_name': 'Operator'},
            {'name': 'M Husen Ali', 'position_code': 'PER', 'department_name': 'Operator'},
            {'name': 'Edi Suhardi', 'position_code': 'PER', 'department_name': 'Operator'},
            {'name': 'Mahmud', 'position_code': 'PER', 'department_name': 'Operator'},
            {'name': 'Fiki Ariyanto', 'position_code': 'PER', 'department_name': 'Operator'},
            {'name': 'Rahmat Suryadi', 'position_code': 'PER', 'department_name': 'Operator'},
            {'name': 'Arif Hidayat', 'position_code': 'RAM', 'department_name': 'Operator'},
            {'name': 'M Thamrin', 'position_code': 'RAM', 'department_name': 'Operator'},
            {'name': 'Jaka Swara', 'position_code': 'RAM', 'department_name': 'Operator'},
            {'name': 'Bangkit Prayoga', 'position_code': 'RAM', 'department_name': 'Operator'},
            {'name': 'Fajar Aditya', 'position_code': 'RAM', 'department_name': 'Operator'},
            {'name': 'Khafit', 'position_code': 'RAM', 'department_name': 'Operator'},
            {'name': 'Albert Ikhbal', 'position_code': 'TEMBAK_KAWAT', 'department_name': 'Operator'},
            {'name': 'Suyanto', 'position_code': 'TEMBAK_KAWAT', 'department_name': 'Operator'},
            {'name': 'Ryandi', 'position_code': 'TEMBAK_KAWAT', 'department_name': 'Operator'},
            {'name': 'Radika', 'position_code': 'TEMBAK_KAWAT', 'department_name': 'Operator'},
            {'name': 'Dedi', 'position_code': 'TEMBAK_KAWAT', 'department_name': 'Operator'},
            {'name': 'M Iqhbal', 'position_code': 'TEMBAK_KAWAT', 'department_name': 'Operator'},
            {'name': 'Jiman', 'position_code': 'POCKET', 'department_name': 'Operator'},
            {'name': 'Firmansyah', 'position_code': 'POCKET', 'department_name': 'Operator'},
            {'name': 'Cahdiana', 'position_code': 'POCKET', 'department_name': 'Operator'},
            {'name': 'M Teguh', 'position_code': 'POCKET', 'department_name': 'Operator'},
            {'name': 'Dedi Setiawan', 'position_code': 'ASSEMBLY', 'department_name': 'Operator'},
            {'name': 'Amit', 'position_code': 'ASSEMBLY', 'department_name': 'Operator'},
            {'name': 'Sugino', 'position_code': 'FRAME', 'department_name': 'Operator'},
            {'name': 'Sugianto', 'position_code': 'FRAME', 'department_name': 'Operator'},
            {'name': 'Ali', 'position_code': 'FRAME', 'department_name': 'Operator'},
            {'name': 'Afian Nurcahyo', 'position_code': 'FRAME', 'department_name': 'Operator'},
            {'name': 'Karnila', 'position_code': 'SUPPLY', 'department_name': 'Operator'},
            {'name': 'Faiz Fadrul', 'position_code': 'SUPPLY', 'department_name': 'Operator'},
            # New workers requested by user
            {'name': 'Zuriana', 'position_code': 'POTONG', 'department_name': 'Operator'},
            {'name': 'Ardi Kurniawan', 'position_code': 'POTONG', 'department_name': 'Operator'},
            {'name': 'Andika Yogastira', 'position_code': 'TEMBAK_RANGKA', 'department_name': 'Operator'},
            {'name': 'Reka Dara S', 'position_code': 'TEMBAK_RANGKA', 'department_name': 'Operator'},
            {'name': 'Dani Setiawan', 'position_code': 'TEMBAK_RANGKA', 'department_name': 'Operator'},
            {'name': 'Tarsius', 'position_code': 'FG', 'department_name': 'Operator'},
            {'name': 'Ngaliman', 'position_code': 'PRP', 'department_name': 'Operator'},
            {'name': 'Yogi', 'position_code': 'ISI', 'department_name': 'Operator'},
            {'name': 'Andreas', 'position_code': 'ISI', 'department_name': 'Operator'},
            {'name': 'Tandi', 'position_code': 'JAHIT', 'department_name': 'Operator'},
            {'name': 'Adman Husen', 'position_code': 'PACKING', 'department_name': 'Operator'},
            # Admin/Management
            {'name': 'Zaenal Arifin', 'position_code': None, 'department_name': 'Koordinator', 'password': 'zaenal1'},
            {'name': 'Prido Sagala', 'position_code': None, 'department_name': 'Supervisor', 'password': 'prido1'},
            {'name': 'Kiky', 'position_code': None, 'department_name': 'Admin Produksi', 'password': 'kiky1'},
            {'name': 'Rino Alyuwa', 'position_code': None, 'department_name': 'Admin Produksi', 'password': 'rino1'},
            {'name': 'Super Admin', 'position_code': None, 'department_name': 'Superadmin', 'password': 'mas5indo'},
        ],
        'items': [
            {'item_number': 'W1090001581224', 'item_name': 'PER T15 D8,1 K2,24', 'spec': ''},
            {'item_number': 'W1090001585224', 'item_name': 'PER T15 D8,5 K2,24', 'spec': ''},
            {'item_number': 'W1090001881224', 'item_name': 'PER T18 D8.1 K2.24', 'spec': ''},
            {'item_number': 'W1090001885224', 'item_name': 'PER T18 D8.5 K2.24', 'spec': ''},
            {'item_number': 'W1090001885240', 'item_name': 'PER T18 D8.5 K2.40 6 ULIR', 'spec': ''},
            {'item_number': 'W8320015073176', 'item_name': 'SPRING POCKET 15X073X176', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320015083176', 'item_name': 'SPRING POCKET 15X083X176', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320015103176', 'item_name': 'SPRING POCKET 15X103X176', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8300015074177', 'item_name': 'SPRING POCKET 15X071X176', 'spec': 'KAWAT 2 MM + BW TANPA M-GUARD'},
            {'item_number': 'W8300015084177', 'item_name': 'SPRING POCKET 15X081X176', 'spec': 'KAWAT 2 MM + BW TANPA M-GUARD'},
            {'item_number': 'W8300015104177', 'item_name': 'SPRING POCKET 15X101X176', 'spec': 'KAWAT 2 MM + BW TANPA M-GUARD'},
            {'item_number': 'W8300015074184', 'item_name': 'SPRG POCKET 15X073X183/071X181', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8300015084184', 'item_name': 'SPRG POCKET 15X083X183/081X181', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8300015104184', 'item_name': 'SPRG POCKET 15X103X183/101X181', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8320018075185', 'item_name': 'SPRING POCKET 18X073X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320018085185', 'item_name': 'SPRING POCKET 18X083X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320018105185', 'item_name': 'SPRING POCKET 18X103X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320018145185', 'item_name': 'SPRING POCKET 18X143X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320018165185', 'item_name': 'SPRING POCKET 18X163X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320018185185', 'item_name': 'SPRING POCKET 18X183X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320118073183', 'item_name': 'SPRG POCKET 18X073X183/071X181', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8320118083183', 'item_name': 'SPRG POCKET 18X083X183/081X181', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8320118103183', 'item_name': 'SPRG POCKET 18X103X183/101X181', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8320118143183', 'item_name': 'SPRG POCKET 18X143X183/141X181', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8320118163183', 'item_name': 'SPRG POCKET 18X163X183/161X181', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8320118183183', 'item_name': 'SPRG POCKET 18X183X183/181X181', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8320021075185', 'item_name': 'SPRING POCKET 21X073X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320021085185', 'item_name': 'SPRING POCKET 21X083X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320021105185', 'item_name': 'SPRING POCKET 21X103X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320021145185', 'item_name': 'SPRING POCKET 21X143X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320021165185', 'item_name': 'SPRING POCKET 21X163X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320021185185', 'item_name': 'SPRING POCKET 21X183X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8300021073183', 'item_name': 'SPRG POCKET 21X073X183/071X181', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8300021083183', 'item_name': 'SPRG POCKET 21X083X183/081X181', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8300021103183', 'item_name': 'SPRG POCKET 21X103X183/101X181', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8300021143183', 'item_name': 'SPRG POCKET 21X143X183/141X181', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8300021163183', 'item_name': 'SPRG POCKET 21X163X183/161X181', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8300021183183', 'item_name': 'SPRG POCKET 21X183X183/181X181', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8320028073183', 'item_name': 'SPRING POCKET 28X073X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320028083183', 'item_name': 'SPRING POCKET 28X083X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320028103183', 'item_name': 'SPRING POCKET 28X103X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320028143183', 'item_name': 'SPRING POCKET 28X143X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320028163183', 'item_name': 'SPRING POCKET 28X163X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320028183183', 'item_name': 'SPRING POCKET 28X183X183', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320018061071', 'item_name': 'SPRING POCKET 18X061X071 HYBRD', 'spec': 'KAWAT 2 MM'},
            {'item_number': 'W8320018061081', 'item_name': 'SPRING POCKET 18X061X081 HYBRD', 'spec': 'KAWAT 2 MM'},
            {'item_number': 'W8320018061101', 'item_name': 'SPRING POCKET 18X061X101 HYBRD', 'spec': 'KAWAT 2 MM'},
            {'item_number': 'W8320018061141', 'item_name': 'SPRING POCKET 18X061X141 HYBRD', 'spec': 'KAWAT 2 MM'},
            {'item_number': 'W8320018061161', 'item_name': 'SPRING POCKET 18X061X161 HYBRD', 'spec': 'KAWAT 2 MM'},
            {'item_number': 'W8320018061181', 'item_name': 'SPRING POCKET 18X061X181 HYBRD', 'spec': 'KAWAT 2 MM'},
            {'item_number': 'W8320018071181', 'item_name': 'SPRING POCKET 18X071X181 HYBRD', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8320018081181', 'item_name': 'SPRING POCKET 18X081X181 HYBRD', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8320018101181', 'item_name': 'SPRING POCKET 18X101X181 HYBRD', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8320018141181', 'item_name': 'SPRING POCKET 18X141X181 HYBRD', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8320018161181', 'item_name': 'SPRING POCKET 18X161X181 HYBRD', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8320018181181', 'item_name': 'SPRING POCKET 18X181X181 HYBRD', 'spec': 'KAWAT 2 MM BW + M + C-GUARD'},
            {'item_number': 'W8320018089199', 'item_name': 'SPRING POCKET 18X089X199 SLEEP', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320018099199', 'item_name': 'SPRING POCKET 18X099X199 SLEEP', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320018119199', 'item_name': 'SPRING POCKET 18X119X199 SLEEP', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320018159199', 'item_name': 'SPRING POCKET 18X159X199 SLEEP', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320018179199', 'item_name': 'SPRING POCKET 18X179X199 SLEEP', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8320018199199', 'item_name': 'SPRING POCKET 18X199X199 SLEEP', 'spec': 'KAWAT 2.00 MM'},
            {'item_number': 'W8022415089199', 'item_name': 'RAM BONEL 15X089X199 224 SLEEP', 'spec': 'KAWAT 2.240 MM TANPA BW DAN M'},
            {'item_number': 'W8022415099199', 'item_name': 'RAM BONEL 15X099X199 224 SLEEP', 'spec': 'KAWAT 2.240 MM TANPA BW DAN M'},
            {'item_number': 'W8022415119199', 'item_name': 'RAM BONEL 15X119X199 224 SLEEP', 'spec': 'KAWAT 2.240 MM TANPA BW DAN M'},
            {'item_number': 'W8022415159199', 'item_name': 'RAM BONEL 15X159X199 224 SLEEP', 'spec': 'KAWAT 2.240 MM TANPA BW DAN M'},
            {'item_number': 'W8022415179199', 'item_name': 'RAM BONEL 15X179X199 224 SLEEP', 'spec': 'KAWAT 2.240 MM TANPA BW DAN M'},
            {'item_number': 'W8022415199199', 'item_name': 'RAM BONEL 15X199X199 224 SLEEP', 'spec': 'KAWAT 2.240 MM TANPA BW DAN M'},
            {'item_number': 'W1050201610180', 'item_name': 'RAM BONEL 15X090X180 K 2.24 MM', 'spec': 'MULTIBED'},
            {'item_number': 'W1050201620180', 'item_name': 'RAM BONEL 15X100X180 K 2.24 MM', 'spec': 'MULTIBED'},
            {'item_number': 'W1050201630180', 'item_name': 'RAM BONEL 15X120X180 K 2.24 MM', 'spec': 'MULTIBED'},
            {'item_number': 'W1050201610090', 'item_name': 'RAM BONEL 15X090X200 K 2.24 MM', 'spec': 'MULTIBED'},
            {'item_number': 'W1050201620100', 'item_name': 'RAM BONEL 15X100X200 K 2.24 MM', 'spec': 'MULTIBED'},
            {'item_number': 'W1050201630120', 'item_name': 'RAM BONEL 15X120X200 K 2.24 MM', 'spec': 'MULTIBED'},
            {'item_number': 'W8022418087197', 'item_name': 'RAM BONEL 18X087X197 2.24 MM', 'spec': 'D8.1+D8.5 KAWAT 2.24 MM'},
            {'item_number': 'W8022418097197', 'item_name': 'RAM BONEL 18X097X197 2.24 MM', 'spec': 'D8.1+D8.5 KAWAT 2.24 MM'},
            {'item_number': 'W8022418117197', 'item_name': 'RAM BONEL 18X117X197 2.24 MM', 'spec': 'D8.1+D8.5 KAWAT 2.24 MM'},
            {'item_number': 'W8022418157197', 'item_name': 'RAM BONEL 18X157X197 2.24 MM', 'spec': 'D8.1+D8.5 KAWAT 2.24 MM'},
            {'item_number': 'W8022418177197', 'item_name': 'RAM BONEL 18X177X197 2.24 MM', 'spec': 'D8.1+D8.5 KAWAT 2.24 MM'},
            {'item_number': 'W8022418197197', 'item_name': 'RAM BONEL 18X197X197 2.24 MM', 'spec': 'D8.1+D8.5 KAWAT 2.24 MM'},
            {'item_number': 'W8224018087197', 'item_name': 'RAM BONEL 18X087X197 2.40 MM', 'spec': 'D8.1+D8.5 KAWAT 2.40 MM'},
            {'item_number': 'W8224018097197', 'item_name': 'RAM BONEL 18X097X197 2.40 MM', 'spec': 'D8.1+D8.5 KAWAT 2.40 MM'},
            {'item_number': 'W8224018117197', 'item_name': 'RAM BONEL 18X117X197 2.40 MM', 'spec': 'D8.1+D8.5 KAWAT 2.40 MM'},
            {'item_number': 'W8224018157197', 'item_name': 'RAM BONEL 18X157X197 2.40 MM', 'spec': 'D8.1+D8.5 KAWAT 2.40 MM'},
            {'item_number': 'W8224018177197', 'item_name': 'RAM BONEL 18X177X197 2.40 MM', 'spec': 'D8.1+D8.5 KAWAT 2.40 MM'},
            {'item_number': 'W8224018197197', 'item_name': 'RAM BONEL 18X197X197 2.40 MM', 'spec': 'D8.1+D8.5 KAWAT 2.40 MM'},
            {'item_number': 'W8224118074184', 'item_name': 'RAM BONEL 18X074X184 D8.1+D8.5', 'spec': 'KAWAT 2.40 MM + BW + TANPA M'},
            {'item_number': 'W8224118084184', 'item_name': 'RAM BONEL 18X084X184 D8.1+D8.5', 'spec': 'KAWAT 2.40 MM + BW + TANPA M'},
            {'item_number': 'W8224118104184', 'item_name': 'RAM BONEL 18X104X184 D8.1+D8.5', 'spec': 'KAWAT 2.40 MM + BW + TANPA M'},
            {'item_number': 'W8224118144184', 'item_name': 'RAM BONEL 18X144X184 D8.1+D8.5', 'spec': 'KAWAT 2.40 MM + BW + TANPA M'},
            {'item_number': 'W8224118164184', 'item_name': 'RAM BONEL 18X164X184 D8.1+D8.5', 'spec': 'KAWAT 2.40 MM + BW + TANPA M'},
            {'item_number': 'W8224118184184', 'item_name': 'RAM BONEL 18X184X184 D8.1+D8.5', 'spec': 'KAWAT 2.40 MM + BW + TANPA M'},
            {'item_number': 'W82224118074184', 'item_name': 'RAM BONEL 18X074X184 D8.1+D8.5', 'spec': 'KAWAT 2.24 MM + BW + TANPA M'},
            {'item_number': 'W82224118084184', 'item_name': 'RAM BONEL 18X084X184 D8.1+D8.5', 'spec': 'KAWAT 2.24 MM + BW + TANPA M'},
            {'item_number': 'W82224118104184', 'item_name': 'RAM BONEL 18X104X184 D8.1+D8.5', 'spec': 'KAWAT 2.24 MM + BW + TANPA M'},
            {'item_number': 'W82224118144184', 'item_name': 'RAM BONEL 18X144X184 D8.1+D8.5', 'spec': 'KAWAT 2.24 MM + BW + TANPA M'},
            {'item_number': 'W82224118164184', 'item_name': 'RAM BONEL 18X164X184 D8.1+D8.5', 'spec': 'KAWAT 2.24 MM + BW + TANPA M'},
            {'item_number': 'W82224118184184', 'item_name': 'RAM BONEL 18X184X184 D8.1+D8.5', 'spec': 'KAWAT 2.24 MM + BW + TANPA M'},
            {'item_number': 'W8224018074184', 'item_name': 'RAM BONEL 18X074X184 D8.1+D8.5', 'spec': 'BW + M GUARD + CORNER GUARD'},
            {'item_number': 'W8224018084184', 'item_name': 'RAM BONEL 18X084X184 D8.1+D8.5', 'spec': 'BW + M GUARD + CORNER GUARD'},
            {'item_number': 'W8224018104184', 'item_name': 'RAM BONEL 18X104X184 D8.1+D8.5', 'spec': 'BW + M GUARD + CORNER GUARD'},
            {'item_number': 'W8224018144184', 'item_name': 'RAM BONEL 18X144X184 D8.1+D8.5', 'spec': 'BW + M GUARD + CORNER GUARD'},
            {'item_number': 'W8224018164184', 'item_name': 'RAM BONEL 18X164X184 D8.1+D8.5', 'spec': 'BW + M GUARD + CORNER GUARD'},
            {'item_number': 'W8224018184184', 'item_name': 'RAM BONEL 18X184X184 D8.1+D8.5', 'spec': 'BW + M GUARD + CORNER GUARD'},
        ]
    }


def clear_database(db: Session):
    """Clear all data from database"""
    print("Clearing existing data...")
    db.query(ProductionLogProblemComment).delete()
    db.query(ProductionLog).delete()
    db.query(ProblemComment).delete()
    db.query(Item).delete()
    db.query(Supplier).delete()
    db.query(Shift).delete()
    db.query(Worker).delete()
    db.query(SubPosition).delete()
    db.query(Position).delete()
    db.query(Department).delete()
    db.query(Division).delete()
    db.commit()
    print("Database cleared!")


def seed_divisions(db: Session, priority_data: dict):
    """Seed divisions from priority data"""
    print("Seeding divisions...")
    divisions = []
    division_names = priority_data.get('divisions', [])
    
    division_map = {}
    for i, name in enumerate(division_names):
        code = f"DIV{i+1:03d}"
        division = Division(
            code=code,
            name=name
        )
        divisions.append(division)
        division_map[name] = division
        db.add(division)
    
    db.commit()
    print(f"[OK] Created {len(divisions)} divisions")
    return divisions, division_map


def seed_departments(db: Session, divisions: list, division_map: dict, priority_data: dict):
    """Seed departments from priority data"""
    print("Seeding departments...")
    departments = []
    dept_names = priority_data.get('departments', [])
    
    # Assign departments to first division (Kawat)
    kawat_division = division_map.get('Kawat')
    if not kawat_division:
        print("Warning: Kawat division not found, skipping departments")
        return departments, {}
    
    dept_map = {}
    for i, dept_name in enumerate(dept_names):
        code = f"DEPT{i+1:02d}"
        department = Department(
            division_id=kawat_division.id,
            code=code,
            name=dept_name
        )
        departments.append(department)
        dept_map[dept_name] = department
        db.add(department)
    
    db.commit()
    print(f"[OK] Created {len(departments)} departments")
    return departments, dept_map


def seed_positions(db: Session, priority_data: dict):
    """Seed positions from priority data"""
    print("Seeding positions...")
    positions = []
    pos_data = priority_data.get('positions', [])
    
    position_map = {}
    for pos in pos_data:
        code = pos['code'].upper()
        unit = pos['unit']
        name = pos.get('name')
        
        position = Position(
            code=code,
            name=name,
            unit=unit
        )
        positions.append(position)
        position_map[code] = position
        db.add(position)
    
    db.commit()
    print(f"[OK] Created {len(positions)} positions")
    return positions, position_map


def seed_sub_positions(db: Session, positions: list, position_map: dict, priority_data: dict):
    """Seed sub positions from priority data"""
    print("Seeding sub positions...")
    sub_positions = []
    sub_pos_data = priority_data.get('sub_positions', [])
    
    for sub_pos in sub_pos_data:
        code = sub_pos['code']
        position_code = sub_pos['position_code'].upper()
        
        if position_code in position_map:
            sub_position = SubPosition(
                position_id=position_map[position_code].id,
                code=code
            )
            sub_positions.append(sub_position)
            db.add(sub_position)
        else:
            print(f"Warning: Position code '{position_code}' not found for sub position '{code}'")
    
    db.commit()
    print(f"[OK] Created {len(sub_positions)} sub positions")
    return sub_positions


def seed_workers(db: Session, positions: list, position_map: dict, departments: list, dept_map: dict, priority_data: dict):
    """Seed workers from priority data"""
    print("Seeding workers...")
    workers = []
    workers_data = priority_data.get('workers', [])
    
    for worker_data in workers_data:
        name = worker_data['name']
        position_code = worker_data.get('position_code')
        dept_name = worker_data.get('department_name')
        password = worker_data.get('password')
        
        position_id = None
        if position_code and position_code.upper() in position_map:
            position_id = position_map[position_code.upper()].id
        elif position_code:
            print(f"Warning: Position code '{position_code}' not found for worker '{name}'")
        
        department_id = None
        if dept_name and dept_name in dept_map:
            department_id = dept_map[dept_name].id
        elif dept_name:
            print(f"Warning: Department '{dept_name}' not found for worker '{name}'")
        
        # Hash password if provided
        hashed_password = None
        if password:
            try:
                hashed_password = hash_password(password)
                print(f"  - {name}: password hashed")
            except Exception as e:
                print(f"  - {name}: Warning - failed to hash password: {str(e)}")
        
        worker = Worker(
            name=name,
            position_id=position_id,
            department_id=department_id,
            password=hashed_password
        )
        workers.append(worker)
        db.add(worker)
    
    db.commit()
    print(f"[OK] Created {len(workers)} workers")
    return workers


def seed_shifts(db: Session, priority_data: dict):
    """Seed shifts from priority data"""
    print("Seeding shifts...")
    shifts = []
    shift_names = priority_data.get('shifts', [])
    
    for name in shift_names:
        shift = Shift(name=name)
        shifts.append(shift)
        db.add(shift)
    
    db.commit()
    print(f"[OK] Created {len(shifts)} shifts")
    return shifts


def seed_suppliers(db: Session, priority_data: dict):
    """Seed suppliers from priority data"""
    print("Seeding suppliers...")
    suppliers = []
    supplier_names = priority_data.get('suppliers', [])
    
    for name in supplier_names:
        supplier = Supplier(name=name)
        suppliers.append(supplier)
        db.add(supplier)
    
    db.commit()
    print(f"[OK] Created {len(suppliers)} suppliers")
    return suppliers


def seed_items(db: Session, priority_data: dict):
    """Seed items from priority data"""
    print("Seeding items...")
    items = []
    items_data = priority_data.get('items', [])
    
    for item_data in items_data:
        item = Item(
            item_number=item_data['item_number'],
            item_name=item_data.get('item_name', ''),
            spec=item_data.get('spec', '')
        )
        items.append(item)
        db.add(item)
    
    db.commit()
    print(f"[OK] Created {len(items)} items")
    return items


def seed_problem_comments(db: Session, count: int = 5):
    """Seed problem comments with random data"""
    print(f"Seeding {count} problem comments...")
    problem_comments = []
    
    descriptions = [
        "Mesin rusak",
        "Pemadaman listrik",
        "Kesalahan operator",
        "Cacat material"
    ]
    
    for i in range(count):
        description = descriptions[i] if i < len(descriptions) else f"Masalah {i+1}: {fake.sentence()}"
        
        problem_comment = ProblemComment(
            description=description
        )
        problem_comments.append(problem_comment)
        db.add(problem_comment)
    
    db.commit()
    print(f"[OK] Created {len(problem_comments)} problem comments")
    return problem_comments


def seed_production_logs(
    db: Session,
    workers: list,
    positions: list,
    sub_positions: list,
    shifts: list,
    suppliers: list,
    items: list,
    problem_comments: list,
    dept_map: dict,
    count: int = 10
):
    """Seed production logs with random data"""
    print(f"Seeding {count} production logs...")
    production_logs = []
    
    # Create reverse map: department_id -> department_name
    dept_id_to_name = {dept.id: name for name, dept in dept_map.items()}
    
    # Get workers for approval (prefer coordinators and supervisors)
    coordinators = [w for w in workers if w.department_id and dept_id_to_name.get(w.department_id) == 'Koordinator']
    supervisors = [w for w in workers if w.department_id and dept_id_to_name.get(w.department_id) == 'Supervisor']
    approvers = coordinators + supervisors
    if not approvers:
        approvers = workers[:10] if len(workers) >= 10 else workers
    
    # Get operators only for production logs
    operator_workers = [w for w in workers if w.department_id and dept_id_to_name.get(w.department_id) == 'Operator']
    if not operator_workers:
        operator_workers = workers
    
    for i in range(count):
        worker = random.choice(operator_workers)
        position = random.choice(positions)
        
        # Get sub_positions that belong to this position
        position_sub_positions = [sp for sp in sub_positions if sp.position_id == position.id]
        sub_position = random.choice(position_sub_positions) if position_sub_positions and random.random() > 0.3 else None
        
        shift = random.choice(shifts)
        supplier = random.choice(suppliers) if random.random() > 0.2 else None
        item = random.choice(items)
        
        # Generate realistic quantities based on position unit
        if position.unit == 'pcs':
            qty_output = Decimal(str(round(random.uniform(50, 500), 2)))
        else:  # lmbr
            qty_output = Decimal(str(round(random.uniform(100, 1000), 2)))
        
        max_reject = qty_output * Decimal("0.1")
        qty_reject = Decimal(
            str(
                round(
                    random.uniform(0, float(max_reject)),
                    2
                )
            )
        )
        
        # Random problem duration (30% chance)
        problem_duration = random.randint(15, 120) if random.random() < 0.3 else None
        
        # Random approval status
        approved_coordinator = None
        approved_spv = None
        approved_coordinator_by = None
        approved_spv_by = None
        approved_coordinator_at = None
        approved_spv_at = None
        
        if random.random() > 0.4:  # 60% approved by coordinator
            approved_coordinator = True
            approved_coordinator_by = random.choice(approvers).id if approvers else None
            approved_coordinator_at = fake.date_time_between(start_date='-30d', end_date='now')
            
            if random.random() > 0.3:  # 70% of coordinator approved also approved by SPV
                approved_spv = True
                approved_spv_by = random.choice(approvers).id if approvers else None
                approved_spv_at = approved_coordinator_at + timedelta(hours=random.randint(1, 24))
        
        # Random created_at (within last 30 days)
        created_at = fake.date_time_between(start_date='-30d', end_date='now')
        
        production_log = ProductionLog(
            worker_id=worker.id,
            position_id=position.id,
            sub_position_id=sub_position.id if sub_position else None,
            shift_id=shift.id,
            supplier_id=supplier.id if supplier else None,
            item_id=item.id,
            qty_output=qty_output,
            qty_reject=qty_reject,
            problem_duration_minutes=problem_duration,
            created_at=created_at,
            approved_coordinator=approved_coordinator,
            approved_spv=approved_spv,
            approved_coordinator_at=approved_coordinator_at,
            approved_spv_at=approved_spv_at,
            approved_coordinator_by=approved_coordinator_by,
            approved_spv_by=approved_spv_by
        )
        production_logs.append(production_log)
        db.add(production_log)
    
    db.commit()
    print(f"[OK] Created {len(production_logs)} production logs")
    
    # Seed production_log_problem_comments (many-to-many)
    print("Linking problem comments to production logs...")
    plpc_count = 0
    for log in production_logs:
        # 40% chance to have problem comments (only if there's a problem duration)
        if random.random() < 0.4 and log.problem_duration_minutes:
            num_comments = random.randint(1, 3)
            selected_comments = random.sample(problem_comments, min(num_comments, len(problem_comments)))
            
            for pc in selected_comments:
                plpc = ProductionLogProblemComment(
                    production_log_id=log.id,
                    problem_comment_id=pc.id
                )
                db.add(plpc)
                plpc_count += 1
    
    db.commit()
    print(f"[OK] Created {plpc_count} production log problem comment links")
    
    return production_logs


def seed_production_targets(db: Session, positions: list, sub_positions: list, count: int = 10):
    """Seed production targets with random data"""
    print(f"Seeding {count} production targets...")
    targets = []
    
    for _ in range(count):
        position = random.choice(positions)
        
        # Get sub_positions that belong to this position
        position_sub_positions = [sp for sp in sub_positions if sp.position_id == position.id]
        sub_position = random.choice(position_sub_positions) if position_sub_positions and random.random() > 0.3 else None
        
        target_value = Decimal(str(round(random.uniform(100, 1000), 2)))
        
        target = ProductionTarget(
            target=target_value,
            position_id=position.id,
            sub_position_id=sub_position.id if sub_position else None
        )
        targets.append(target)
        db.add(target)
    
    db.commit()
    print(f"[OK] Created {len(targets)} production targets")
    return targets


def seed_attendances(db: Session, workers: list, count: int = 10):
    """Seed attendances with random data"""
    print(f"Seeding {count} attendances...")
    attendances = []
    
    for _ in range(count):
        worker = random.choice(workers)
        status = random.choice(list(AttendanceStatus))
        date = fake.date_between(start_date='-30d', end_date='today')
        time = fake.time_object()
        
        attendance = Attendance(
            worker_id=worker.id,
            status=status,
            date=date,
            time=time,
            notes=fake.sentence() if random.random() > 0.5 else None,
            approved_coordinator=random.choice([True, False, None]),
            approved_supervisor=random.choice([True, False, None])
        )
        attendances.append(attendance)
        db.add(attendance)
        
    db.commit()
    print(f"[OK] Created {len(attendances)} attendances")
    return attendances


def main():
    """Main seeder function"""
    print("=" * 60)
    print("Matrix Database Seeder")
    print("Using embedded priority data")
    print("=" * 60)
    
    # Get priority seed data
    print("\nLoading priority data...")
    priority_data = get_priority_data()
    
    # Print summary of data
    print(f"  - Divisions: {len(priority_data.get('divisions', []))}")
    print(f"  - Departments: {len(priority_data.get('departments', []))}")
    print(f"  - Positions: {len(priority_data.get('positions', []))}")
    print(f"  - Sub Positions: {len(priority_data.get('sub_positions', []))}")
    print(f"  - Shifts: {len(priority_data.get('shifts', []))}")
    print(f"  - Suppliers: {len(priority_data.get('suppliers', []))}")
    print(f"  - Workers: {len(priority_data.get('workers', []))}")
    print(f"  - Items: {len(priority_data.get('items', []))}")
    
    db: Session = SessionLocal()
    
    try:
        # Check for --yes flag
        parser = argparse.ArgumentParser(description='Seed database with initial data')
        parser.add_argument('--yes', '-y', action='store_true', help='Skip confirmation prompt')
        args = parser.parse_args()
        
        # Ask for confirmation if --yes flag not provided
        if not args.yes:
            response = input("\nThis will DROP ALL TABLES and recreate them. Continue? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("Seeder cancelled.")
                return
        
        # Drop and recreate tables
        print("\nDropping all tables (CASCADE)...")
        with engine.connect() as connection:
            try:
                connection.exec_driver_sql("DROP SCHEMA IF EXISTS public CASCADE")
            except Exception:
                pass
            connection.exec_driver_sql("CREATE SCHEMA IF NOT EXISTS public")
            try:
                connection.exec_driver_sql("SET search_path TO public")
            except Exception:
                pass
            connection.commit()
            
        print("Running Alembic migrations...")
        from alembic.config import Config
        from alembic import command
        
        # Ensure we are in the project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        alembic_ini_path = os.path.join(current_dir, "alembic.ini")
        
        alembic_cfg = Config(alembic_ini_path)
        command.upgrade(alembic_cfg, "head")
        
        try:
            from sqlalchemy import inspect
            inspector = inspect(engine)
            tables = inspector.get_table_names(schema="public")
            if "divisions" not in tables:
                print("Warning: tables not found after Alembic upgrade, creating via metadata...")
                Base.metadata.create_all(bind=engine)
        except Exception:
            Base.metadata.create_all(bind=engine)
        
        print("Database schema reset via Alembic!")
        
        # Seed in order (respecting foreign keys)
        divisions, division_map = seed_divisions(db, priority_data)
        departments, dept_map = seed_departments(db, divisions, division_map, priority_data)
        positions, position_map = seed_positions(db, priority_data)
        sub_positions = seed_sub_positions(db, positions, position_map, priority_data)
        workers = seed_workers(db, positions, position_map, departments, dept_map, priority_data)
        shifts = seed_shifts(db, priority_data)
        suppliers = seed_suppliers(db, priority_data)
        items = seed_items(db, priority_data)
        problem_comments = seed_problem_comments(db, count=20)
        production_logs = seed_production_logs(
            db, workers, positions, sub_positions,
            shifts, suppliers, items, problem_comments,
            dept_map, count=10
        )
        production_targets = seed_production_targets(db, positions, sub_positions, count=10)
        attendances = seed_attendances(db, workers, count=10)
        
        print("\n" + "=" * 60)
        print("[OK] Seeding completed successfully!")
        print("=" * 60)
        print(f"\nSummary:")
        print(f"  - Divisions: {len(divisions)}")
        print(f"  - Departments: {len(departments)}")
        print(f"  - Positions: {len(positions)}")
        print(f"  - Sub Positions: {len(sub_positions)}")
        print(f"  - Workers: {len(workers)}")
        print(f"  - Shifts: {len(shifts)}")
        print(f"  - Suppliers: {len(suppliers)}")
        print(f"  - Items: {len(items)}")
        print(f"  - Problem Comments: {len(problem_comments)}")
        print(f"  - Production Logs: {len(production_logs)}")
        print(f"  - Production Targets: {len(production_targets)}")
        print(f"  - Attendances: {len(attendances)}")
        print()
        
    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()

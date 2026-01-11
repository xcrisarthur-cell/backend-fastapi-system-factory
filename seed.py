
import os
import sys
import argparse
from decimal import Decimal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import (
    Division, Department, Position, SubPosition,
    Worker, Shift, Supplier, Item, ProblemComment,
    ProductionTarget
)
from app.security import hash_password

def get_priority_data():
    """Get priority data strictly from seeder_ref.txt"""
    return {
        'divisions': [
            {'code': 'DIV001', 'name': 'Kawat'},
            {'code': 'DIV002', 'name': 'Rangka'},
            {'code': 'DIV003', 'name': 'Bantal'},
            {'code': 'DIV004', 'name': 'IT'},
        ],
        'departments': [
            {'code': 'DEPT001', 'name': 'Operator'},
            {'code': 'DEPT002', 'name': 'Coordinator'},
            {'code': 'DEPT003', 'name': 'Supervisor'},
            {'code': 'DEPT004', 'name': 'Admin Production'},
            {'code': 'DEPT005', 'name': 'Superadmin'},
        ],
        'positions': [
            {'code': 'PER', 'name': 'Per', 'unit': 'pcs'},
            {'code': 'RAM', 'name': 'Ram', 'unit': 'lmbr'},
            {'code': 'TEMBAK_KAWAT', 'name': 'Tembak_Kawat', 'unit': 'lmbr'},
            {'code': 'POCKET', 'name': 'Pocket', 'unit': 'pcs'},
            {'code': 'ASSEMBLY', 'name': 'Assembly', 'unit': 'lmbr'},
            {'code': 'FRAME', 'name': 'Frame', 'unit': 'pcs'},
            {'code': 'SUPPLY', 'name': 'Supply', 'unit': 'lmbr'},
            {'code': 'POTONG', 'name': 'Potong', 'unit': 'pcs'},
            {'code': 'TEMBAK_RANGKA', 'name': 'Tembak_Rangka', 'unit': 'lmbr'},
            {'code': 'FINISH_GOOD', 'name': 'Finish_Good', 'unit': 'pcs'},
            {'code': 'PREPARATION', 'name': 'Preparation', 'unit': 'pcs'},
            {'code': 'ISI', 'name': 'ISI', 'unit': 'pcs'},
            {'code': 'JAHIT', 'name': 'Jahit', 'unit': 'pcs'},
            {'code': 'PACKING', 'name': 'Packing', 'unit': 'pcs'},
        ],
        'sub_positions': [
            {'code': 'FC60', 'position_code': 'PER'},
            {'code': 'SX80', 'position_code': 'PER'},
            {'code': 'SX80i', 'position_code': 'PER'},
            {'code': 'SX80is', 'position_code': 'PER'},
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
        'workers': [
            {'name': 'SLAMET PURNOMO', 'position_code': 'PER', 'department_name': 'Operator'},
            {'name': 'M HUSEN ALI', 'position_code': 'PER', 'department_name': 'Operator'},
            {'name': 'EDI SUHARDI', 'position_code': 'PER', 'department_name': 'Operator'},
            {'name': 'MAHMUD', 'position_code': 'PER', 'department_name': 'Operator'},
            {'name': 'FIKI ARIYANTO', 'position_code': 'PER', 'department_name': 'Operator'},
            {'name': 'RAHMAT SURYADI', 'position_code': 'PER', 'department_name': 'Operator'},
            {'name': 'ARIF HIDAYAT', 'position_code': 'RAM', 'department_name': 'Operator'},
            {'name': 'M THAMRIN', 'position_code': 'RAM', 'department_name': 'Operator'},
            {'name': 'JAKA SWARA', 'position_code': 'RAM', 'department_name': 'Operator'},
            {'name': 'BANGKIT PRAYOGA', 'position_code': 'RAM', 'department_name': 'Operator'},
            {'name': 'FAJAR ADITYA', 'position_code': 'RAM', 'department_name': 'Operator'},
            {'name': 'KHAFIT', 'position_code': 'RAM', 'department_name': 'Operator'},
            {'name': 'ALBERT IKHBAL', 'position_code': 'TEMBAK_KAWAT', 'department_name': 'Operator'},
            {'name': 'SUYANTO', 'position_code': 'TEMBAK_KAWAT', 'department_name': 'Operator'}, # Note: ref text says PETEMBAK_KAWATR but likely typo for TEMBAK_KAWAT, fixing to TEMBAK_KAWAT based on context or creating new position? I'll assume typo and map to TEMBAK_KAWAT for safety as position table doesn't have PETEMBAK_KAWATR
            {'name': 'RYANDI', 'position_code': 'TEMBAK_KAWAT', 'department_name': 'Operator'},
            {'name': 'RADIKA', 'position_code': 'TEMBAK_KAWAT', 'department_name': 'Operator'},
            {'name': 'DEDI', 'position_code': 'TEMBAK_KAWAT', 'department_name': 'Operator'},
            {'name': 'M IQHBAL', 'position_code': 'TEMBAK_KAWAT', 'department_name': 'Operator'},
            {'name': 'JIMAN', 'position_code': 'POCKET', 'department_name': 'Operator'},
            {'name': 'FIRMANSYAH', 'position_code': 'POCKET', 'department_name': 'Operator'},
            {'name': 'CAHDIANA', 'position_code': 'POCKET', 'department_name': 'Operator'},
            {'name': 'M TEGUH', 'position_code': 'POCKET', 'department_name': 'Operator'},
            {'name': 'DEDI SETIAWAN', 'position_code': 'ASSEMBLY', 'department_name': 'Operator'},
            {'name': 'AMIT', 'position_code': 'ASSEMBLY', 'department_name': 'Operator'},
            {'name': 'SUGINO', 'position_code': 'FRAME', 'department_name': 'Operator'},
            {'name': 'SUGIANTO', 'position_code': 'FRAME', 'department_name': 'Operator'},
            {'name': 'ALI', 'position_code': 'FRAME', 'department_name': 'Operator'},
            {'name': 'AFIAN NURCAHYO', 'position_code': 'FRAME', 'department_name': 'Operator'},
            {'name': 'KARNILA', 'position_code': 'SUPPLY', 'department_name': 'Operator'},
            {'name': 'FAIZ FADRUL', 'position_code': 'SUPPLY', 'department_name': 'Operator'},
            {'name': 'ZURIANA', 'position_code': 'POTONG', 'department_name': 'Operator'},
            {'name': 'ARDI KURNIAWAN', 'position_code': 'POTONG', 'department_name': 'Operator'},
            {'name': 'ANDIKA YOGASTIRA', 'position_code': 'TEMBAK_RANGKA', 'department_name': 'Operator'},
            {'name': 'REKA DARA S', 'position_code': 'TEMBAK_RANGKA', 'department_name': 'Operator'},
            {'name': 'DANI SETIAWAN', 'position_code': 'TEMBAK_RANGKA', 'department_name': 'Operator'},
            {'name': 'TARSIUS', 'position_code': 'FINISH_GOOD', 'department_name': 'Operator'},
            {'name': 'NGALIMAN', 'position_code': 'PREPARATION', 'department_name': 'Operator'},
            {'name': 'YOGI', 'position_code': 'ISI', 'department_name': 'Operator'},
            {'name': 'ANDREAS', 'position_code': 'ISI', 'department_name': 'Operator'},
            {'name': 'TANDI', 'position_code': 'JAHIT', 'department_name': 'Operator'},
            {'name': 'ADMAN HUSEN', 'position_code': 'PACKING', 'department_name': 'Operator'},
            # Management
            {'name': 'SUPER ADMIN', 'department_name': 'Superadmin', 'password': 'mas5indo'},
            {'name': 'KIKY', 'department_name': 'Admin Production', 'password': 'kiky1'},
            {'name': 'RINO ALYUWA', 'department_name': 'Admin Production', 'password': 'rino1'},
            {'name': 'PRIDO SAGALA', 'department_name': 'Supervisor', 'password': 'prido1'},
            {'name': 'ZAENAL ARIFIN', 'department_name': 'Coordinator', 'password': 'zaenal1'},
        ],
        'shifts': [
            'SHIFT 1',
            'SHIFT 2',
            'SHIFT 3'
        ],
        'suppliers': [
            'INTIRODA',
            'MEGA',
            'KINGDOM'
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
        ],
        'targets': [
            {'value': 13000, 'position_code': 'PER', 'sub_position_code': 'FC60'},
            {'value': 14000, 'position_code': 'PER', 'sub_position_code': 'SX80'},
            {'value': 16000, 'position_code': 'PER', 'sub_position_code': 'SX80i'},
            {'value': 18000, 'position_code': 'PER', 'sub_position_code': 'SX80is'},
            {'value': 32, 'position_code': 'RAM', 'sub_position_code': 'AS3-NEW'},
            {'value': 35, 'position_code': 'TEMBAK_KAWAT', 'sub_position_code': 'MEJA-1'},
            {'value': 35, 'position_code': 'TEMBAK_KAWAT', 'sub_position_code': 'MEJA-2'},
            {'value': 35, 'position_code': 'TEMBAK_KAWAT', 'sub_position_code': 'MEJA-3'},
            {'value': 29000, 'position_code': 'POCKET', 'sub_position_code': 'LSPR-NEW'},
            {'value': 45, 'position_code': 'ASSEMBLY', 'sub_position_code': None},
            {'value': 35, 'position_code': 'RAM', 'sub_position_code': 'AS3-OLD'},
            {'value': 35, 'position_code': 'RAM', 'sub_position_code': 'SX200'},
        ],
        'problem_comments': [
            'Mesin Rusak',
            'Pemadaman Listrik',
            'Kesalahan Operator',
            'Cacat Material',
            'Mesin Breakdown',
            'Setting Kawat',
            'Setting Mesin',
            'Kawat Nyangkut',
        ]
    }

def seed_divisions(db: Session, priority_data: dict):
    print("Seeding divisions...")
    divisions = []
    div_data = priority_data.get('divisions', [])
    
    division_map = {}
    for d in div_data:
        division = Division(
            code=d['code'],
            name=d['name']
        )
        divisions.append(division)
        division_map[d['name']] = division
        db.add(division)
    
    db.commit()
    print(f"[OK] Created {len(divisions)} divisions")
    return divisions, division_map

def seed_departments(db: Session, division_map: dict, priority_data: dict):
    print("Seeding departments...")
    departments = []
    dept_data = priority_data.get('departments', [])
    
    # Assign departments mostly to Kawat division as default or based on logic?
    # Ref text doesn't specify division for departments, but in previous code it was all Kawat.
    # We will stick to Kawat for now unless specified otherwise.
    kawat_division = division_map.get('Kawat')
    if not kawat_division:
        # Fallback to first available if Kawat missing (unlikely)
        kawat_division = list(division_map.values())[0]

    dept_map = {}
    for d in dept_data:
        department = Department(
            division_id=kawat_division.id,
            code=d['code'],
            name=d['name']
        )
        departments.append(department)
        dept_map[d['name']] = department
        db.add(department)
    
    db.commit()
    print(f"[OK] Created {len(departments)} departments")
    return departments, dept_map

def seed_positions(db: Session, priority_data: dict):
    print("Seeding positions...")
    positions = []
    pos_data = priority_data.get('positions', [])
    
    position_map = {}
    for pos in pos_data:
        position = Position(
            code=pos['code'],
            name=pos['name'],
            unit=pos['unit']
        )
        positions.append(position)
        position_map[pos['code']] = position
        db.add(position)
    
    db.commit()
    print(f"[OK] Created {len(positions)} positions")
    return positions, position_map

def seed_sub_positions(db: Session, position_map: dict, priority_data: dict):
    print("Seeding sub positions...")
    sub_positions = []
    sub_pos_data = priority_data.get('sub_positions', [])
    
    sub_position_map = {} # code -> id
    
    for sub_pos in sub_pos_data:
        position_code = sub_pos['position_code']
        if position_code in position_map:
            sub_position = SubPosition(
                position_id=position_map[position_code].id,
                code=sub_pos['code']
            )
            sub_positions.append(sub_position)
            db.add(sub_position)
            sub_position_map[sub_pos['code']] = sub_position
        else:
            print(f"Warning: Position code '{position_code}' not found for sub position '{sub_pos['code']}'")
    
    db.commit()
    # Refresh to get IDs
    for sp in sub_positions:
        db.refresh(sp)
        sub_position_map[sp.code] = sp
        
    print(f"[OK] Created {len(sub_positions)} sub positions")
    return sub_positions, sub_position_map

def seed_workers(db: Session, position_map: dict, dept_map: dict, priority_data: dict):
    print("Seeding workers...")
    workers = []
    workers_data = priority_data.get('workers', [])
    
    for worker_data in workers_data:
        name = worker_data['name']
        position_code = worker_data.get('position_code')
        dept_name = worker_data.get('department_name')
        password = worker_data.get('password')
        
        position_id = None
        if position_code and position_code in position_map:
            position_id = position_map[position_code].id
        elif position_code:
            print(f"Warning: Position code '{position_code}' not found for worker '{name}'")
        
        department_id = None
        if dept_name and dept_name in dept_map:
            department_id = dept_map[dept_name].id
        elif dept_name:
            print(f"Warning: Department '{dept_name}' not found for worker '{name}'")
        
        # Hash password if provided, else None (or default?)
        hashed_password = None
        if password:
            hashed_password = hash_password(password)
        elif dept_name in ['Superadmin', 'Admin Produksi', 'Supervisor', 'Koordinator']:
             # Set default password for management if not specified (though ref specifies them)
             pass 
        
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

def seed_problem_comments(db: Session, priority_data: dict):
    print("Seeding problem comments...")
    comments = []
    comment_data = priority_data.get('problem_comments', [])
    
    for desc in comment_data:
        comment = ProblemComment(description=desc)
        comments.append(comment)
        db.add(comment)
        
    db.commit()
    print(f"[OK] Created {len(comments)} problem comments")
    return comments

def seed_production_targets(db: Session, position_map: dict, sub_position_map: dict, priority_data: dict):
    print("Seeding production targets...")
    targets = []
    target_data = priority_data.get('targets', [])
    
    for t in target_data:
        pos_code = t['position_code']
        sub_pos_code = t['sub_position_code']
        value = t['value']
        
        if pos_code not in position_map:
            print(f"Warning: Position {pos_code} not found for target")
            continue
            
        pos_id = position_map[pos_code].id
        sub_pos_id = None
        
        if sub_pos_code:
            if sub_pos_code in sub_position_map:
                sub_pos_id = sub_position_map[sub_pos_code].id
            else:
                 print(f"Warning: Sub Position {sub_pos_code} not found for target")
        
        target = ProductionTarget(
            target=Decimal(str(value)),
            position_id=pos_id,
            sub_position_id=sub_pos_id
        )
        targets.append(target)
        db.add(target)
        
    db.commit()
    print(f"[OK] Created {len(targets)} production targets")
    return targets

def main():
    print("=" * 60)
    print("Matrix Database Seeder (Strict Mode)")
    print("=" * 60)
    
    priority_data = get_priority_data()
    db = SessionLocal()
    
    try:
        parser = argparse.ArgumentParser(description='Seed database with strict data')
        parser.add_argument('--yes', '-y', action='store_true', help='Skip confirmation prompt')
        parser.add_argument('--seed-only', action='store_true', help='Skip database reset')
        args = parser.parse_args()
        
        if not args.seed_only:
            if not args.yes:
                if input("Reset DB? (y/n): ").lower() != 'y': return
            
            # Reset logic
            print("\nResetting schema...")
            with engine.connect() as conn:
                # Try to drop schema with CASCADE, but handle permission errors gracefully
                try:
                    conn.exec_driver_sql("DROP SCHEMA IF EXISTS public CASCADE")
                    conn.exec_driver_sql("CREATE SCHEMA public")
                    conn.exec_driver_sql("GRANT ALL ON SCHEMA public TO public")
                    conn.commit()
                    print("[OK] Schema reset successfully")
                except Exception as e:
                    conn.rollback()
                    print(f"[WARNING] Could not drop/create schema: {e}")
                    print("[INFO] Attempting to drop tables individually...")
                    
                    # Fallback: Drop tables individually
                    Base.metadata.drop_all(bind=conn)
                    conn.commit()
                    print("[OK] Tables dropped successfully")
                    
                    # Ensure schema public exists
                    try:
                        conn.exec_driver_sql("CREATE SCHEMA IF NOT EXISTS public")
                        conn.commit()
                    except Exception:
                        pass
            
            print("Running Migrations...")
            from alembic.config import Config
            from alembic import command
            alembic_cfg = Config("alembic.ini")
            command.upgrade(alembic_cfg, "head")
            
            # Fallback check
            try:
                from sqlalchemy import inspect
                inspector = inspect(engine)
                if "divisions" not in inspector.get_table_names(schema="public"):
                    Base.metadata.create_all(bind=engine)
            except:
                Base.metadata.create_all(bind=engine)
                
        else:
            print("Skipping reset (--seed-only)...")
            # Ensure tables exist via fallback if needed
            try:
                from sqlalchemy import inspect
                inspector = inspect(engine)
                if "divisions" not in inspector.get_table_names(schema="public"):
                     print("Tables missing, creating via metadata...")
                     Base.metadata.create_all(bind=engine)
            except:
                 pass

        # Seed Data
        divisions, div_map = seed_divisions(db, priority_data)
        departments, dept_map = seed_departments(db, div_map, priority_data)
        positions, pos_map = seed_positions(db, priority_data)
        sub_positions, sub_pos_map = seed_sub_positions(db, pos_map, priority_data)
        seed_workers(db, pos_map, dept_map, priority_data)
        seed_shifts(db, priority_data)
        seed_suppliers(db, priority_data)
        seed_items(db, priority_data)
        seed_problem_comments(db, priority_data)
        seed_production_targets(db, pos_map, sub_pos_map, priority_data)
        
        print("\n[OK] Seeding Completed Successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()

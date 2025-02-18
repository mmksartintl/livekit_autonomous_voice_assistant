import sqlite3
from typing import Optional
from dataclasses import dataclass
from contextlib import contextmanager

@dataclass
class Car:
    vin: str
    owner: str
    make: str
    model: str
    year: int
    description_service: str
    date_service: str

class DatabaseDriver:
    def __init__(self, db_path: str = "auto_db.sqlite"):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Create cars table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cars (
                    vin TEXT PRIMARY KEY,
                    owner TEXT NOT NULL,
                    make TEXT NOT NULL,
                    model TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    description_service TEXT NOT NULL,
                    date_service TEXT NOT NULL
                )
            """)
            conn.commit()

    def create_car(self, vin: str, owner: str, make: str, model: str, year: int, description_service: str, date_service: str) -> Car:

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO cars (vin, owner, make, model, year, description_service, date_service) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (vin, owner, make, model, year, description_service, date_service)
            )
            conn.commit()
            return Car(vin=vin, owner=owner, make=make, model=model, year=year, description_service=description_service, date_service=date_service)

    def get_car_by_vin(self, vin: str) -> Optional[Car]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cars WHERE vin = ?", (vin,))
            row = cursor.fetchone()
            if not row:
                return None
            
            return Car(
                vin=row[0],
                owner=row[1],
                make=row[2],
                model=row[3],
                year=row[4],
                description_service=row[5],
                date_service=row[6]
                )

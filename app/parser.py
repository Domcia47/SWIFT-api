import csv
from app.database import SessionLocal
from app.models import SwiftCode
from pathlib import Path


def parse_swift(file):
    db = SessionLocal()
    file_path = Path(__file__).resolve().parent.parent / "data" / file
    with open(file_path, newline='') as mycsv:
        reader = csv.DictReader(mycsv)
        for row in reader:
            code = row['SWIFT CODE']
            is_headquarter = code.endswith("XXX")

            swift = SwiftCode(
                swiftCode=code,
                address=row['ADDRESS'],
                bankName=row['NAME'],
                countryISO2=row['COUNTRY ISO2 CODE'],
                countryName=row['COUNTRY NAME'],
                headquarter_bic=None if is_headquarter else code[:8] + "XXX"
            )

            db.add(swift)
        db.commit()
    db.close()

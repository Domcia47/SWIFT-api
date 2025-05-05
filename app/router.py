from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.params import Body
from sqlalchemy.orm import Session
from database import SessionLocal
from models import SwiftCode
from parser import parse_swift
from sqlalchemy.exc import IntegrityError


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/v1/swift-codes/{swift_code}")
def get_swift_details(swift_code: str, db: Session = Depends(get_db)):
    swift = db.query(SwiftCode).filter(SwiftCode.swiftCode == swift_code).first()

    # Jeśli nie znaleziono, zwróć błąd 404
    if not swift:
        raise HTTPException(status_code=404, detail="SWIFT code not found")

    is_hq = swift.headquarter_bic is None
    data = {
        "address": swift.address,
        "bankName": swift.bankName,
        "countryISO2": swift.countryISO2,
        "countryName": swift.countryName,
        "isHeadQuarter": swift.isHeadquarter,
        "swiftCode": swift.swiftCode
    }

    if is_hq:
            data["branches"] = [
                {
                    "address": swift.address,
                    "bankName": swift.bankName,
                    "countryISO2": swift.countryISO2,
                    "isHeadQuarter": swift.isHeadquarter,
                    "swiftCode": swift.swiftCode
                }
                for branch in swift.branches
            ]

    return data

@router.get("/v1/swift-codes/country/{country_iso2}")
def get_swift_codes_by_country(country_iso2: str, db: Session = Depends(get_db)):
    swift_list = db.query(SwiftCode).filter(SwiftCode.countryISO2 == country_iso2.upper()).all()

    if not swift_list:
        raise HTTPException(status_code=404, detail="No SWIFT codes found for this country")

    country_name = swift_list[0].countryName if swift_list else "Unknown"

    data = {
        "countryISO2": country_iso2.upper(),
        "countryName": country_name,
        "swiftCodes": []
    }

    for bank in swift_list:
        is_hq = bank.headquarter_bic is None
        data["swiftCodes"].append({

            "address": bank.address,
            "bankName": bank.bankName,
            "countryISO2": bank.countryISO2,
            "swiftCode": bank.swiftCode,
            "isHeadQuarter": is_hq
        })

    return data


@router.post("/v1/swift-codes")
def add_swift_code(body: dict = Body(...), db: Session = Depends(get_db)):
    required_fields = ["address", "bankName", "countryISO2", "countryName", "isHeadquarter", "swiftCode"]

    # Walidacja wymaganych pól
    for field in required_fields:
        if field not in body:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

    # Czy SWIFT już istnieje
    existing = db.query(SwiftCode).filter(SwiftCode.swiftCode == body["swiftCode"]).first()
    if existing:
        raise HTTPException(status_code=400, detail="SWIFT code already exists")

    # Ustal headquarter_bic tylko jeśli nie jest HQ
    headquarter_bic = None
    if not body["isHeadquarter"]:
        headquarter_bic = body["swiftCode"][:8] + "XXX"

    new_swift = SwiftCode(
        swiftCode=body["swiftCode"],
        address=body["address"],
        bankName=body["bankName"],
        countryISO2=body["countryISO2"].upper(),
        countryName=body["countryName"],
        headquarter_bic=headquarter_bic
    )

    try:
        db.add(new_swift)
        db.commit()
        return {"message": "SWIFT code added successfully"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database error while adding SWIFT code")

@router.delete("/v1/swift-codes/{swift_code}")
def delete_swift_code(swift_code: str, db: Session = Depends(get_db)):
    swift_entry = db.query(SwiftCode).filter(SwiftCode.swiftCode == swift_code).first()

    if not swift_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"SWIFT code '{swift_code}' not found."
        )

    db.delete(swift_entry)
    db.commit()

    return {"message": "SWIFT code deleted successfully."}

@router.post("/upload_swift_data/")
def upload_swift_data(file: str, db: Session = Depends(get_db)):
    swift_codes = parse_swift(file)

    for swift in swift_codes:
        db.add(swift)

    db.commit()  # Zatwierdzamy zmiany w bazie
    return {"message": "Dane zostały załadowane do bazy"}

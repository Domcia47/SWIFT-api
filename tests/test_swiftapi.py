import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))



from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from app.models import SwiftCode



client = TestClient(app)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_hq_get(db):
    hq = SwiftCode(
        swiftCode="ABCDEFGHXXX",
        address="Polna 123",
        bankName="Your Bank",
        countryISO2="PL",
        countryName="Poland",
        headquarter_bic=None
    )

    db.add(hq)
    db.commit()

    response = client.get("/v1/swift-codes/ABCDEFGHXXX")
    assert response.status_code == 200
    data = response.json()
    assert data["swiftCode"] == "ABCDEFGHXXX"
    assert data["isHeadQuarter"] is True
    assert data["branches"] == []

def test_branch_get(db):
    branch = SwiftCode(
        swiftCode="ABCDEFGH001",
        address="Kwiatowa 45",
        bankName="Your Bank",
        countryISO2="PL",
        countryName="Poland",
        headquarter_bic="ABCDEFGHXXX"
    )

    db.add(branch)
    db.commit()

    response = client.get("/v1/swift-codes/ABCDEFGH001")
    assert response.status_code == 200
    data = response.json()
    assert data["swiftCode"] == "ABCDEFGH001"
    assert data["isHeadQuarter"] is False

def test_branch_linked_to_hq_get(db):
    hq = SwiftCode(
        swiftCode="ABCDEFGHXXX",
        address="Polna 123",
        bankName="Your Bank",
        countryISO2="PL",
        countryName="Poland",
        headquarter_bic=None
    )
    db.add(hq)
    db.commit()

    branch = SwiftCode(
        swiftCode="ABCDEFGH001",
        address="Kwiatowa 45",
        bankName="Your Bank",
        countryISO2="PL",
        countryName="Poland",
        headquarter_bic="ABCDEFGHXXX"

    )
    db.add(branch)
    db.commit()

    response = client.get("/v1/swift-codes/ABCDEFGHXXX")
    assert response.status_code == 200
    data = response.json()
    assert data["swiftCode"] == "ABCDEFGHXXX"
    assert data["isHeadQuarter"] is True
    assert data["branches"] ==  [{
        'address': 'Polna 123',
        'bankName': 'Your Bank',
        'countryISO2': 'PL',
        'isHeadQuarter': True,
        'swiftCode': 'ABCDEFGHXXX'
    }]
def test_get_nonexistent_swift_code(db):
    response = client.get("/v1/swift-codes/NONEXIST123")
    assert response.status_code == 404

def test_get_swift_codes_by_country(db):
    db.add(SwiftCode(
        swiftCode="PLBANK123",
        address="Bank St 1",
        bankName="Polish Bank",
        countryISO2="PL",
        countryName="Polska",
        headquarter_bic=None
    ))
    db.add(SwiftCode(
        swiftCode="PLBANK456",
        address="Bank St 2",
        bankName="Polish Bank Branch",
        countryISO2="PL",
        countryName="Polska",
        headquarter_bic="PLBANK123"
    ))
    db.commit()

    response = client.get("/v1/swift-codes/country/PL")

    assert response.status_code == 200
    data = response.json()

    assert data["countryISO2"] == "PL"
    assert data["countryName"] == "Polska"
    assert len(data["swiftCodes"]) == 2

    swift_code = data["swiftCodes"][0]
    assert swift_code["swiftCode"] == "PLBANK123"
    assert swift_code["isHeadQuarter"] is True

    swift_code = data["swiftCodes"][1]
    assert swift_code["swiftCode"] == "PLBANK456"
    assert swift_code["isHeadQuarter"] is False

def test_get_swift_codes_no_data(db):
    response = client.get("/v1/swift-codes/country/US")

    assert response.status_code == 404
    data = response.json()

    assert data["detail"] == "No SWIFT codes found for this country"



def test_post_headquarter(db):
    body = {
        "swiftCode": "HQBANKPLXXX",
        "address": "Main St 1",
        "bankName": "Test Bank",
        "countryISO2": "pl",
        "countryName": "Poland",
        "isHeadquarter": True
    }

    response = client.post("/v1/swift-codes", json=body)
    assert response.status_code == 200
    assert response.json() == {"message": "SWIFT code added successfully"}

    hq = db.query(SwiftCode).filter_by(swiftCode="HQBANKPLXXX").first()
    assert hq is not None
    assert hq.headquarter_bic is None

def test_post_branch(db):
    db.add(SwiftCode(
        swiftCode="HQBANKPLXXX",
        address="Main St 1",
        bankName="Test Bank",
        countryISO2="PL",
        countryName="Poland",
        headquarter_bic=None
    ))
    db.commit()

    body = {
        "swiftCode": "HQBANKPL001",
        "address": "Branch St 2",
        "bankName": "Test Bank",
        "countryISO2": "pl",
        "countryName": "Poland",
        "isHeadquarter": False
    }

    response = client.post("/v1/swift-codes", json=body)
    assert response.status_code == 200
    assert response.json() == {"message": "SWIFT code added successfully"}

    branch = db.query(SwiftCode).filter_by(swiftCode="HQBANKPL001").first()
    assert branch is not None
    assert branch.headquarter_bic == "HQBANKPLXXX"







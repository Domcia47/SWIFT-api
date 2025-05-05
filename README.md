# SWIFT Code API

## Description

This application allows for storing and managing SWIFT (BIC) codes of banks. Users can add, view, and manage SWIFT codes, checking which ones are headquarters (HQ) and which ones are branches. The application uses FastAPI for API handling and SQLite as the database.

## Requirements

* Python 3.8+
* SQLite (by default, but you can change it to another database)
* FastAPI
* Uvicorn

## Installation

### 1. Clone the repository

```bash
git clone <REPOSITORY_URL>
cd <PROJECT_FOLDER_NAME>
```

### 2. Install the dependencies

Install all the required packages by running the following command:

```bash
pip install -r requirements.txt
```

## Running the Application

To run the application locally, use the following command:

```bash
uvicorn app.main:app --reload  --port 8080
```

The application will be available at `http://localhost:8080/docs`.

### 3. Check the application

Once the app is running, the API will be accessible under the following endpoints:

* **GET** `/v1/swift-codes/{swift_code}` - Retrieves the details for a SWIFT code.
* **POST** `/v1/swift-codes` - Adds a new SWIFT code to the database.

## Directory Structure

```plaintext
<PROJECT_ROOT>/
├── app/
│   ├── __init__.py
│   ├── main.py       # Main application file
│   ├── router.py     # API endpoint definitions
│   ├── models.py     # Database models (SQLAlchemy)
│   ├── database.py   # Database connection
│   └── parser.py     # CSV parser
├── requirements.txt  # Project dependencies list
└── README.md         # This file
```

## Example Requests

### Add a new SWIFT code (POST)

```bash
curl -X 'POST' \
  'http://127.0.0.1:8080/v1/swift-codes' \
  -H 'Content-Type: application/json' \
  -d '{
  "address": "123 Bank St, New York",
  "bankName": "Example Bank",
  "countryISO2": "US",
  "countryName": "United States",
  "isHeadquarter": true,
  "swiftCode": "EXAMPUS1XXX"
}'
```

### Retrieve SWIFT code details (GET)

```bash
curl -X 'GET' \
  'http://127.0.0.1:8080/v1/swift-codes/EXAMPUS1XXX' \
  -H 'accept: application/json'
```

## Testing

To test the API, you can use tools such as:

* [Postman](https://www.postman.com/)
* [cURL](https://curl.se/)
* [Insomnia](https://insomnia.rest/)


### Example tests:

1. **GET `/v1/swift-codes/{swift_code}`** – Retrieves the details of the bank, including whether it is a headquarter.
2. **POST `/v1/swift-codes`** – Adds a new bank to the database.

## Notes

* The database uses SQLite (the file `swift.db`), which is automatically created the first time the application is run.
* You can customize the database configuration in `database.py`.


# SWIFT Code API

## Description

This application allows for storing and managing SWIFT (BIC) codes of banks. Users can add, view, and manage SWIFT codes, checking which ones are headquarters (HQ) and which ones are branches. The application uses FastAPI for API handling and SQLite as the database.

## Requirements

* Python 3.8+
* SQLite
* FastAPI
* Uvicorn

## Installation


### 1. Clone the repository

```bash
git clone https://github.com/Domcia47/SWIFT-api
cd SWIFT-API
```

**Note:** All commands below should be run from the root directory of the repository (\SWIFT-API).

### 2. Install the dependencies
Create virtual environment:

```bash
python -m venv venv
```
Next for Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

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
* **GET** ` /v1/swift-codes/country/{countryISO2code}` - Retrieves the details for a specific country.
* **POST** `/v1/swift-codes` -  Adds new SWIFT code entries to the database for a specific country.
* **DELETE** `/v1/swift-codes/{swift-code}` - Deletes swift-code data if swiftCode matches the one in the database.


## Directory Structure

```plaintext
<PROJECT_ROOT>/
├── app/
│   ├── init_db.py    # Initializes sqlite databaes
│   ├── main.py       # Main application file
│   ├── router.py     # API endpoint definitions
│   ├── models.py     # Database models (SQLAlchemy)
│   ├── database.py   # Database connection
│   └── parser.py     # CSV parser
├── data/
│   ├── swift.db      # SQLite database
├── tests/
│   ├── test_swiftapi.py  # Unit tests
├── requirements.txt      # Project dependencies list
└── README.md             # This file
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
  'http://localhost:8080/v1/swift-codes/TPEOPLPWXXX' \
  -H 'accept: application/json'
```

## Interactive API Documentation
FastAPI provides an automatic, interactive GUI for testing your API, powered by Swagger UI.

Once the server is running, open your browser and navigate to:

http://localhost:8080/docs

This interface lets you:

* Explore all available endpoints,
* View request/response formats,
* Test endpoints directly from the browser.

## Unit Tests
This project includes a set of unit tests to ensure core functionality works as expected. The tests are located in the tests/ directory and are written using the built-in pytest framework.

To run the tests use:

```bash
pytest tests/
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

* The database uses SQLite (the file `swift.db`), which was initialized using init_db.py.


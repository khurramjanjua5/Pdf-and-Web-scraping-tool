# PDF and Web Scraping Project

This project extracts data from PDF files and performs web scraping to collect additional information. The extracted data is stored in a SQLite database and can be downloaded in Excel format.

## Dependencies

Ensure you have the following dependencies installed:

- Python 3.x
- tabula-py
- camelot-py
- requests
- BeautifulSoup4
- Flask
- pandas
- SQLite3

## Installation

1. Clone the repository to your local machine:

git clone https://github.com/your-username/pdf-and-web-scraping.git

## Usage
Navigate to the project directory:
cd pdf-and-web-scraping

## Start the Flask server:
python app.py

## Access the API endpoints:
Store data: POST /store_data
Download Excel file: GET /download_excel

## API Documentation
Endpoint: /store_data
Method: POST
Description: This endpoint allows users to upload a PDF file and provide a URL for web scraping. The data will be extracted from the PDF file and the provided URL, transformed, and stored in the database.

Request Body:

pdf_path (string): Path to the PDF file to be uploaded.
url (string): URL for web scraping additional information.
Response:

Success (200 OK):
Message: "Data stored successfully."
Failure (500 Internal Server Error):
Error: "Failed to store data in the database."



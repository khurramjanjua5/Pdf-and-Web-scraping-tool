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

```bash
git clone https://github.com/your-username/pdf-and-web-scraping.git

## Usage
Navigate to the project directory:
cd pdf-and-web-scraping

Start the Flask server:
python app.py

Access the API endpoints:
Store data: POST /store_data
Download Excel file: GET /download_excel

API Endpoints
POST /store_data: Upload a PDF file and provide a URL for web scraping. The data will be stored in the database.
GET /download_excel: Download the stored data in Excel format.
Contributing
If you'd like to contribute to this project, please fork the repository, make your changes, and submit a pull request.





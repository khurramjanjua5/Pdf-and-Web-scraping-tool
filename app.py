import tabula
import camelot
import requests
from bs4 import BeautifulSoup
import sqlite3
from flask import Flask, request, jsonify, send_file
import pandas as pd

app = Flask(__name__)
# PDF scraping function
def extract_data_from_pdf(pdf_path, pages='all'):
    try:
        tables = camelot.read_pdf(pdf_path, pages=pages)
        if tables:
            return [table.df for table in tables]
        dfs = tabula.read_pdf(pdf_path, pages=pages)
        return dfs
    except Exception as e:
        print("Error occurred during PDF extraction:", str(e))
        return []

# Web scraping function
def scrape_additional_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad response status
        soup = BeautifulSoup(response.content, 'html.parser')
        additional_info = soup.find_all('div', class_='additional-info', recursive=True)
        return [info.get_text(strip=True) for info in additional_info]
    except requests.RequestException as e:
        print("Request failed during web scraping:", str(e))
        return []
    except Exception as e:
        print("Error occurred during web scraping:", str(e))
        return []

# Data transformation function
def transform_data(pdf_data, web_data):
    transformed_data = []
    for i in range(min(len(pdf_data), len(web_data))):
        transformed_entry = {
            'pdf_data': pdf_data[i].to_dict(orient='records')[0] if pdf_data else None,
            'web_data': web_data[i] if web_data else None
        }
        transformed_data.append(transformed_entry)
    return transformed_data

# Database interaction function
def save_to_database(data):
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS transformed_data
                        (id INTEGER PRIMARY KEY, 
                         pdf_title TEXT, 
                         pdf_content TEXT, 
                         web_data TEXT)''')
        for entry in data:
            pdf_data = entry['pdf_data']
            web_data = entry['web_data']
            pdf_title = pdf_data.get('column_name_1') if pdf_data else None
            pdf_content = pdf_data.to_string(index=False) if pdf_data else None
            cursor.execute('''INSERT INTO transformed_data 
                               (pdf_title, pdf_content, web_data) 
                               VALUES (?, ?, ?)''',
                           (pdf_title, pdf_content, web_data))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("SQLite error during database interaction:", str(e))
        return False
    except Exception as e:
        print("Error occurred during database interaction:", str(e))
        return False

# API endpoint for data storage
@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        request_data = request.get_json()
        pdf_path = request_data.get('pdf_path')
        url = request_data.get('url')

        pdf_data = extract_data_from_pdf(pdf_path)
        web_data = scrape_additional_info(url)
        transformed_data = transform_data(pdf_data, web_data)

        if save_to_database(transformed_data):
            return jsonify({"message": "Data stored successfully."}), 200
        else:
            return jsonify({"error": "Failed to store data in the database."}), 500
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": "An error occurred while processing the request."}), 500

# API endpoint for downloading data in Excel format
@app.route('/download_excel', methods=['GET'])
def download_excel():
    try:
        conn = sqlite3.connect('data.db')
        query = "SELECT * FROM transformed_data"
        df = pd.read_sql_query(query, conn)
        conn.close()

        excel_filename = 'transformed_data.xlsx'
        df.to_excel(excel_filename, index=False)

        return send_file(excel_filename, as_attachment=True)
    except Exception as e:
        print("Error occurred during Excel download:", str(e))
        return jsonify({"error": "An error occurred while downloading Excel file."}), 500

if __name__ == '__main__':
    app.run(debug=True)

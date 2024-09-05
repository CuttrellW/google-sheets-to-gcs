import logging
import flask

app = flask.Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GoogleSheetsImport:
    def __init__(self, sheet_id: str, bucket_name: str, file_name: str):
        self.sheet_id = sheet_id
        self.bucket_name = bucket_name
        self.file_name = file_name

    def process_sheet(self):
        # process the sheet
        pass


@app.route('/process_sheet', methods=['POST'])
def process_sheet():
    data = flask.request.json
    processor = GoogleSheetsImport(**data)
    processor.process_sheet()
    return "OK", 200


if __name__ == '__main__':
    app.run(debug=True)
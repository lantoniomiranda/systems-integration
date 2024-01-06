import base64
from io import StringIO
from xml_converter.csv_to_xml_converter import CSVtoXMLConverter
from xml_converter.validator import validate
from database import database


def import_csv(path, db_file_name):
    try:
        print('IMPORT_CSV')
        xml_file = CSVtoXMLConverter(path)
        xml_to_str = xml_file.to_xml_str()
        print('XML_TO_STR -> ', xml_to_str)
        valid = validate(xml_file)
        if valid:
            print('Valid --> ', valid)
            result = database.storeFile(xml_to_str, db_file_name)
            print(result)
            if result is None:
                return "Failed to store file in the database."
            return result
    except Exception as e:
        print(f"An error occurred with the function: {e}")


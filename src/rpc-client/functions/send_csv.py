import os
from .enconder_file import encoder_csv


def send_csv(server):
    print('SEND_CSV')
    csv_name = input('Digite o nome do ficheiro: ').strip() + '.csv'
    csv_path = os.path.join('/data', csv_name)

    encoded_string = encoder_csv(csv_path)

    db_file_name = input('Friendly name para guardar na base de dados: ').strip()

    try:
        print('INSIDE TRY')
        response = server.import_csv(csv_path, db_file_name)
        print('Response -> ', response)
    except Exception as e:
        print(f"An error occurred sending to server: {e}")

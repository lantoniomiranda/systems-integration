import base64


def encoder_csv(file_path):
    try:
        with open(file_path, "rb") as csv_file:
            encoded_csv = base64.b64encode(csv_file.read())

        encoded_string = encoded_csv.decode('utf-8')

        return encoded_string
    except Exception as e:
        print(f"Erro ao codificar o csv: {e}")
import os.path
import psycopg2


class Database:
    def storeFile(self, file_path, db_file_name):
        global connection, cursor
        try:
            with open(os.path.join(file_path), 'r') as file:
                xml = file.read()
            connection = psycopg2.connect(user="is",
                                          password="is",
                                          host="is-db",
                                          port="5432",
                                          database="is")

            cursor = connection.cursor()
            cursor.execute('''INSERT INTO imported_documents(file_name, xml) VALUES (%s, %s)''', (db_file_name, xml))

            connection.commit()

            return "File stored successfully in the database."

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)
            connection.rollback()
            return "Error {error}".format(error=error)

        finally:
            if connection:
                cursor.close()
                connection.close()

    def query(self, query, params=None):
        global connection, cursor

        connection = psycopg2.connect(user="is",
                                          password="is",
                                          host="is-db",
                                          port="5432",
                                          database="is")

        print('Connected to database...')
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        print('Cursor executed')
        return result


    def hello(self):
        return 'Hello'
import psycopg2


class Database:

    def storeFile(self, file, db_file_name):
        global connection, cursor
        try:
            connection = psycopg2.connect(user="is",
                                          password="is",
                                          host="is-db",
                                          port="5432",
                                          database="is")

            cursor = connection.cursor()
            cursor.execute('''INSERT INTO imported_documents(file_name, xml) VALUES (%s, %s)''', (db_file_name, file))

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

    def query(self, query):
        global connection, cursor
        try:
            connection = psycopg2.connect(user="is",
                                          password="is",
                                          host="is-db",
                                          port="5432",
                                          database="is")

            cursor = connection.cursor()
            cursor.execute(query)

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()

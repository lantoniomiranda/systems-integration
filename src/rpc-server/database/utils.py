import psycopg2


class Database:

    def storeFile(self, file):
        global connection, cursor
        try:
            connection = psycopg2.connect(user="is",
                                          password="is",
                                          host="is-db",
                                          port="5432",
                                          database="is")

            cursor = connection.cursor()
            cursor.execute('''INSERT INTO imported_documents(file_name, xml) VALUES ('file_xml', %s)''', (file))

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

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

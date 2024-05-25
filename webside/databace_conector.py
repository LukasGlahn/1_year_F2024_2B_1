import sqlite3

class DataBase():

    def __init__(self,database):
        self.database = database

    def add_to_databace(self,query,data):
        try:
            conn = sqlite3.connect(self.database)
            cur = conn.cursor()
            cur.execute(query,data)
            conn.commit()

        except sqlite3.Error as sql_e:
            conn.rollback()
            return f'sqlite encounterd a error: {sql_e}'

        except Exception as e:
            return f'encounterd a error: {e}'

        finally:
            conn.close()


    def get_databace_data(self,query,max_output = 20):
        try:
            conn = sqlite3.connect(self.database)
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchmany(max_output)
            return rows

        except sqlite3.Error as sql_e:
            print(f'sqlite encounterd a error: {sql_e}')
            conn.rollback()

        except Exception as e:
            print(f'encounterd a error: {e}')

        finally:
            conn.close()

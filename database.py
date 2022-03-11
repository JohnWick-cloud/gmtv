import sqlite3

class Sqlite:

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_id(self, list_name):
        with self.connection:
            return self.cursor.execute(f"SELECT msg_id FROM id WHERE group_name = '{list_name}'").fetchall()

    def get_all_id(self,list_name):
        with self.connection:
            return self.cursor.execute(f"SELECT msg_id FROM id WHERE group_name = '{list_name}'").fetchone()


    def add_id(self, list_name, msg_id):
        with self.connection:
            return self.cursor.execute("INSERT  INTO 'id' VALUES (?,?)",( list_name, msg_id))

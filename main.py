import pymysql

class DataBase:
    def __init__(self):
        self.connection = pymysql.connect(
            host= 'localhost',
            user= 'root',
            password='',
            db='scrapyn'
        )

        self.cursor = self.connection.cursor()

        
        

    def select_table(self, table):
        sql = ''

        try:
            self.cursor.execute(sql)

        except Exception as e:
            raise

    def close(self):
        self.connection.close()
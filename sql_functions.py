import pymysql
import re

class SQL():
    def __init__(self, db, user, password):
        self.db = db
        self.user = user
        self.password = password
    #Open cursor & connection
    def open_db(self):
        conn = pymysql.connect(host='localhost', user=self.user, 
               password=self.password, db=self.db, unix_socket='/tmp/mysql.sock' )
        cur = conn.cursor(pymysql.cursors.DictCursor)
        return conn, cur
    #Close cursor & connection
    def close_db(self, conn, cur):
        cur.close()
        conn.close()
    #Read Table
    def read_table(self, table, columns="title"):
        cols = columns.split(",")
        opt = "([ ])"

        conn, cur = self.open_db()
        sql = "select * from "+table
        cur.execute(sql)
        r = cur.fetchone()

        while r:
            for col in cols:
                print(r[re.sub(opt, "", col)], end="|")
            print("\n")
            r = cur.fetchone()
        self.close_db(conn, cur)
    #Get Column names of Table
    def get_table_columns(self, table):
        columns = []
        conn, cur = self.open_db()
        sql = "select column_name from information_schema.columns where table_name='"+table+"';"
        cur.execute(sql)
        r = cur.fetchone()
        while r:
            columns.append(r["COLUMN_NAME"])
            r = cur.fetchone()
        self.close_db(conn, cur)
        return columns
    #Input Data Function
    def input_data(self, table, columns, data):
        cols = columns.split(",")
        try:
            columns.remove("enter_date")
        except:
            pass
        conn, cur = self.open_db()
        sql1 = "insert into "+table+"("+columns
        sql2 = ") values("
        sql3 = ")"
        for i in range(len(cols)):
            if i==0:
                sql2 = sql2+"%s"
            else:
                sql2 = sql2+", %s"
        sql = sql1+sql2+sql3

        buffer = []
        for d in data:
            buffer.append(d)

            if len(buffer) % 10 == 0:
                cur.executemany(sql, buffer)
                conn.commit()
                buffer = []
        if buffer:
            cur.executemany(sql, buffer)
            conn.commit()
        
        self.close_db(conn, cur)
    #Input Data Function for Movie Table
    def input_data_to_movie(self, data):
        conn, cur = self.open_db()
        sql = """
                insert into movie(title, movie_rate, netizen_score, netizen_count, journalist_score, journalist_count, scope, playing_time, opening_date, director, image) 
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        buffer = []
    
        for d in data:
            t = (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9], d[10]) 
            buffer.append(t)
            
            if len(buffer) % 10 == 0:
                # 여러 개를 execute하므로 executemany 사용
                cur.executemany(sql, buffer)
                conn.commit()
                buffer = []
        
        if buffer:
            cur.executemany(sql, buffer)
            conn.commit()
            
        self.close_db(conn, cur)
if __name__ == '__main__':
    SQL(db="naver_movie", user="naver", password="naver").read_table(table="movie", 
                                                                    columns="title, movie_rate, netizen_score, netizen_count, \
                                                                            journalist_score, journalist_count, scope, playing_time, \
                                                                            opening_date, director, image")
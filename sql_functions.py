import pymysql

class SQL():
    def __init__(self):
        pass
    def open_db(self, db, user, password):
        conn = pymysql.connect(host='localhost', user=user, 
               password=password, db=db, unix_socket='/tmp/mysql.sock' )
        cur = conn.cursor(pymysql.cursors.DictCursor)
        return conn, cur
    def close_db(self, conn, cur):
        cur.close()
        conn.close()
    def read_table(self, db, table, user, password):
        conn, cur = self.open_db(db, user, password)
        sql = "select * from "+table
        cur.execute(sql)
        r = cur.fetchone()
        while r:
            print(r['title'])
            r = cur.fetchone()
        self.close_db(conn, cur)
    def get_table_columns(self, db, table, user, password):
        columns = []
        conn, cur = self.open_db(db, user, password)
        sql = "select column_name from information_schema.columns where table_name='"+table+"';"
        cur.execute(sql)
        r = cur.fetchone()
        while r:
            columns.append(r["COLUMN_NAME"])
            r = cur.fetchone()
        self.close_db(conn, cur)
        return columns
    # def input_data(self, db, table, user, password, data):
    #     columns = self.get_table_columns(db, table, user, password)
        # try:
        #     columns.remove("enter_date")
        # except:
        #     pass
        # conn, cur = self.open_db(db, user, password)
        # sql1 = "insert into "+table+"("
        # sql2 = ") values("
        # sql3 = ")"
        # for i, col in enumerate(columns):
        #     if i==0:
        #         sql1 = sql1+col
        #         sql2 = sql2+"%s"
        #     else:
        #         sql1 = sql1+", "+col
        #         sql2 = sql2+", %s"
        # sql = sql1+sql2+sql3

        # print(sql)
        # print(i)

        # inputs = []
        # for dt in data:
        #     input = "("
        #     for i, d in enumerate(dt):
        #         if i==0:
        #             input = input = str(d)
        #         else:
        #             input = input+", "+str(d)
        #     input = input+")"
        #     inputs.append(input)

        # buffer = []
        # for d in inputs:
        #     buffer.append(d)

        #     if len(buffer) % 2 == 0:
        #         cur.executemany(sql, buffer)
        #         conn.commit()
        #         buffer = []
        
        # self.close_db(conn, cur)
    def input_data_to_movie(self, data):
        conn, cur = self.open_db("naver_movie", "naver", "naver")
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
    def change_null_in_movie(self):
        conn1, cur1 = self.open_db("naver_movie", "naver", "naver")
        conn2, cur2 = self.open_db("naver_movie", "naver", "naver")
        conn3, cur3 = self.open_db("naver_movie", "naver", "naver")
        conn4, cur4 = self.open_db("naver_movie", "naver", "naver")
        conn5, cur5 = self.open_db("naver_movie", "naver", "naver")
        conn6, cur6 = self.open_db("naver_movie", "naver", "naver")
        conn7, cur7 = self.open_db("naver_movie", "naver", "naver")
        conn8, cur8 = self.open_db("naver_movie", "naver", "naver")
        conn9, cur9 = self.open_db("naver_movie", "naver", "naver")
        conn10, cur10 = self.open_db("naver_movie", "naver", "naver")
        sql1 = """update movie
                set movie_rate = NULL
                where movie_rate = 'null'
        """
        sql2 = """update movie
                set netizen_score = NULL
                where netizen_score = 'null'
        """
        sql3 = """update movie
                set netizen_count = NULL
                where netizen_count = 'null'
        """
        sql4 = """update movie
                set journalist_score = NULL
                where journalist_score = 'null'
        """
        sql5 = """update movie
                set journalist_count = NULL
                where journalist_count= 'null'
        """
        sql6 = """update movie
                set scope = NULL
                where scope = 'null'
        """
        sql7 = """update movie
                set playing_time = NULL
                where playing_time = 'null'
        """
        sql8 = """update movie
                set opening_date = NULL
                where opening_date = 'null'
        """
        sql9 = """update movie
                set director = NULL
                where director = 'null'
        """
        sql10 = """update movie
                set image = NULL
                where image = 'null'
        """
        cur1.execute(sql1)
        cur2.execute(sql2)
        cur3.execute(sql3)
        cur4.execute(sql4)
        cur5.execute(sql5)
        cur6.execute(sql6)
        cur7.execute(sql7)
        cur8.execute(sql8)
        cur9.execute(sql9)
        cur10.execute(sql10)
        self.close_db(conn1, cur1)
        self.close_db(conn2, cur2)
        self.close_db(conn3, cur3)
        self.close_db(conn4, cur4)
        self.close_db(conn5, cur5)
        self.close_db(conn6, cur6)
        self.close_db(conn7, cur7)
        self.close_db(conn8, cur8)
        self.close_db(conn9, cur9)
        self.close_db(conn10, cur10)

if __name__ == '__main__':
    sample = [['극장판 엉덩이 탐정: 수플레 섬의 비밀',
                '전체 관람가',
                7.5,
                28,
                5.67,
                3,
                '애니메이션,가족,코미디',
                '59',
                '2022-05-05',
                '자코 아키후미',
                'https://movie-phinf.pstatic.net/20220405_51/1649144698523czjrT_JPEG/movie_image.jpg?type=m99_141_2'],
                ['액션동자',
                '전체 관람가',
                10.0,
                4,
                5.0,
                1,
                '액션',
                '99',
                '2022-05-05',
                '최영민',
                'https://movie-phinf.pstatic.net/20220425_136/1650877572992bhbVe_JPEG/movie_image.jpg?type=m99_141_2']]
    # SQL().read_table("naver_movie", "movie", "naver", "naver")
    # SQL().read_table("university", "enrol", "naver", "naver")
    # SQL().input_data("naver_movie", "movie", "naver", "naver", sample)
    SQL().input_data_to_movie(sample)
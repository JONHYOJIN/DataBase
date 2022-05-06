import pymysql

def open_db():
   conn = pymysql.connect(host='localhost', user='univ', 
               password='univ', db='university', unix_socket='/tmp/mysql.sock' )
   
   cur = conn.cursor(pymysql.cursors.DictCursor)
   
   return conn, cur

def close_db(conn, cur):
    cur.close()
    conn.close()
    
    
def gen_good_score_list():
    # 문장 수만큼 cursor와 connection을 만들자
    conn1, cur1 = open_db()
    conn2, cur2 = open_db()
    
    # 중간&기말 점수가 모두 85점 이상인 학생들의 이름, 과목, 중간점수, 기말점수
    sql = """
        select s.sname, c.cname, e.midterm, e.final
        from student s, course c, enrol e
        where s.sno = e.sno and c.cno = e.cno
        and e.midterm >= 85 and e.final >= 85;
    """

    cur1.execute(sql)
    r = cur1.fetchone()
    
    insert_sql = """insert into good_score_list(sname, cname, midterm, final, medium)
                    values(%s, %s, %s, %s, %s)"""
    
    buffer = []
    
    while r:
        t = (r['sname'], r['cname'], r['midterm'], r['final'], (r['midterm']+r['final'])/2.0 ) 
        buffer.append(t)
        
        if len(buffer) % 2 == 0:
            # 여러 개를 execute하므로 executemany 사용
            cur2.executemany(insert_sql, buffer)
            conn2.commit()
            buffer = []
            
        r = cur1.fetchone()
    
    if buffer:
        cur2.executemany(insert_sql, buffer)
        conn2.commit()  
        
    close_db(conn1, cur1)
    close_db(conn2, cur2)
    

if __name__ == '__main__':
    gen_good_score_list()    
        
        
    
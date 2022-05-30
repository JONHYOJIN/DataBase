from crawling import Naver_scrapping
from sql_functions import SQL

#Naver Movie Data Crawling
scrapper = Naver_scrapping()
scrapper.land_page()
movies = scrapper.get_movie_information()

#Contact Database
naver = SQL(db="naver_movie", user="naver", password="naver")
#Input Movie Data to SQL DataBase
naver.input_data(table = "movie",
                columns="title, movie_rate, netizen_rate, netizen_count, \
                         journalist_score, journalist_count, scope, playing_time, \
                         opening_date, director, image", 
                data=movies)

#Read Movie Data from SQL DataBase
naver.read_table(table="movie", 
                 columns="id, title, movie_rate, netizen_rate, netizen_count, \
                 journalist_score, journalist_count, scope, playing_time, \
                 opening_date, director, image, enter_date")
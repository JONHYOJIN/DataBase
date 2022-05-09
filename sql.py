from crawling import Naver_scrapping
from sql_functions import SQL

#Naver Movie Data Crawling
scrapper = Naver_scrapping()
scrapper.land_page()
movies = scrapper.get_movie_information()

#Input Movie Data to SQL DataBase
naver = SQL(db="naver_movie", user="naver", password="naver")
naver.input_data(table = "movie",
                columns="title, movie_rate, netizen_score, netizen_count, \
                         journalist_score, journalist_count, scope, playing_time, \
                         opening_date, director, image", 
                data=movies)

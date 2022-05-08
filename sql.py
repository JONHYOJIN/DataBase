from crawling import Naver_scrapping
from sql_functions import SQL

#Naver Movie Data Crawling
scrapper = Naver_scrapping()
scrapper.land_page()
movies = scrapper.get_movie_information()

#Input Movie Data to SQL DataBase
SQL().input_data(db="naver_movie", 
                table="movie", 
                user="naver", password="naver",
                columns="title, movie_rate, netizen_score, netizen_count, \
                        journalist_score, journalist_count, scope, playing_time, \
                        opening_date, director, image", 
                data=movies)

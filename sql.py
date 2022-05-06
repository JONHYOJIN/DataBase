from crawling import Naver_scrapping
from sql_functions import SQL

scrapper = Naver_scrapping()
scrapper.land_page()
movies = scrapper.get_movie_information()


SQL().input_data_to_movie(movies)
SQL().change_null_in_movie()
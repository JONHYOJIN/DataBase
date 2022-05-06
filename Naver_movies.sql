create database naver_movie;
use naver_movie;
create table movie(
	title varchar(30) primary key,
    movie_rate varchar(10) not null,
    netizen_score float,
    netizen_count integer,
    journalist_score float,
    journalist_count integer,
    scope varchar(30),
    playing_time integer,
    opening_date datetime,
    director varchar(20),
    image varchar(512),
    enter_date datetime default now()
);

drop table movie;

select * from movie;

create user 'naver'@'%' identified by 'naver';
grant all privileges on naver_movie.* to 'naver'@'%';

select column_name from information_schema.columns where table_name='movie';


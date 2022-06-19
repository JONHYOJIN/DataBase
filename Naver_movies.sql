create database naver_movie;
use naver_movie;
create table movie(
	id integer auto_increment primary key,
	title varchar(30),
    movie_rate varchar(10),
    netizen_rate float,
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
select * from movie;
select count(*) from movie;

create user 'naver'@'%' identified by 'naver';
grant all privileges on naver_movie.* to 'naver'@'%';

drop table movie;

select * from movie;

select column_name from information_schema.columns where table_name='movie';

select * from pybo_question
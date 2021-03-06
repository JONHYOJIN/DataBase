create database naver;
use naver;

create user 'hyojin'@'%' identified by 'gywls';
grant all privileges on naver.* to 'hyojin'@'%';

drop database naver;

create table movie(
	movie_code integer primary key,
    title varchar(100),
    original_title varchar(100),
    opening_date datetime,
    playing_time integer,
    domestic_rate varchar(10),
    foreign_rate varchar(10),
    subtitle varchar(200),
    content varchar(2000),
    poster_url varchar(512),
    audience_rate float,
    journalist_rate float,
    netizen_rate float,
    audience_count integer,
    journalist_count integer,
    netizen_count integer,
    cumulative_audience integer
);
create table actor(
	actor_code integer primary key,
    actor_name varchar(100),
    original_actor_name varchar(100)
);
create table movie_actor(
	movie_code integer not null,
    actor_code integer not null,
	foreign key (movie_code) references movie(movie_code),
    foreign key (actor_code) references actor(actor_code),
    
    cast varchar(5),
    role varchar(20),
    
    primary key (movie_code, actor_code)
);
create table director(
	director_code integer primary key,
    director_name varchar(100),
    original_director_name varchar(100)
);
create table movie_director(
	movie_code integer not null,
    director_code integer not null,
	foreign key (movie_code) references movie(movie_code),
    foreign key (director_code) references director(director_code),
    
    primary key (movie_code, director_code)
);
create table image(
	movie_code integer not null,
    image_url varchar(512) not null,
    foreign key (movie_code) references movie(movie_code),
    
    primary key (movie_code, image_url)
);
create table video(
	movie_code integer not null,
    video_url varchar(512) not null,
    video_title varchar(30),
    foreign key (movie_code) references movie(movie_code),
    
    primary key (movie_code, video_url)
);
create table jenre(
    movie_code integer not null,
    jenre_name varchar(10) not null,
    foreign key (movie_code) references movie(movie_code),
    
    primary key (movie_code, jenre_name)
);
create table nation(
	movie_code integer not null,
    country varchar(15) not null,
    foreign key (movie_code) references movie(movie_code),
    
    primary key (movie_code, country)
);
create table point(
	movie_code integer not null,
    point_id varchar(30) not null,
    foreign key (movie_code) references movie(movie_code),
    
    point_content varchar(500),
    point_date datetime,
    point_good integer,
    point_bad integer,
    point_star integer

);
create table review(
	review_code integer primary key,
    review_id varchar(30),
    review_title varchar(100),
    review_content varchar(2000),
    review_date datetime,
    review_lookup integer,
    review_recommend integer
);
create table movie_review(
	movie_code integer not null,
    review_code integer not null,
    foreign key (movie_code) references movie(movie_code),
    foreign key (review_code) references review(review_code),
    
    primary key (movie_code, review_code)
);
create table review2(
	review_code integer not null,
    foreign key (review_code) references review(review_code),
    review2_id varchar(30),
    review2_content varchar(500),
    review2_date datetime,
    review2_good integer,
    review2_bad integer
);

create index movie_title on Movie(title);
create index opening_date on Movie(opening_date);
create index movie_audience_rate on Movie(audience_rate);
create index movie_journalist_rate on Movie(journalist_rate);
create index movie_netizen_rate on Movie(netizen_rate);
create index movie_original_title on Movie(original_title);
create index movie_subtitile on Movie(subtitle);


create index actor_actor_name on Actor(actor_name);
create index director_director_name on Director(director_name);

select * from review2;
select * from review;
select * from actor;
select * from director;
select * from video;
select * from image;
select * from jenre;
select * from nation;
select * from movie;


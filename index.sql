use university;

create table student10M(
	sno int primary key auto_increment,
    sname char(4) not null,
    dept int not null,
    year int,
    memo varchar(500),
    enter_date datetime default now()
);
create table course1M(
	cno int primary key auto_increment,
    cname char(4),
    dept int,
    memo varchar(500),
    enter_date datetime default now()
);
create table enrol10M(
	sno int,
    cno int,
    midterm int,
    final int,
    memo varchar(500),
    enter_date datetime default now(),
    foreign key (sno) references student10M(sno),
    foreign key (cno) references course1M(cno)
);

select * from student10M;
-- index 이름은 하나의 table에서 unique하면 됨
create index idx_sname on student10M(sname);
-- 함수가 들어가면 인덱스를 사용 못함
select * from student10M where lower(sname)='hong';
-- HONG에 넣으면 인덱스 사용 가능(But 대문자도 다 나옴)
select * from student10M where sname=lower("HONG");

-- 조건이 2개면 선택도(Selectivity)에 따라 결정됨(갯수가 적은거)
-- 둘 다 선택도가 낮으면 Full Scan 할 수도 있음
-- 따라서 Multi index 사용(순서가 중요함)
create index idx_sname_dept on student10M(sanme, dept);
create index idx_dept_sname on student10M(dept, sname);

-- sname
select dept, count(*)
from student10M
group by dept;

-- year dept multi index
select dept, count(*)
from student10M
where year=3
group by dept;


select dept, count(*)
from student10M
where sname="HONG"
order by dept;

select dept, count(*)
from student10M
where dept=71
order by sname;

-- 다중 테이블 인덱스
select *
from student10M s, enrol10M e
where s.sno=e.sno
and s.sname='HONG';

create index idx_sname on student10M(sname);

-- join query
select distinct s1.*
from student10M s1, student1M s2
where s1.sname=s2.sname
and s1.dept=71;






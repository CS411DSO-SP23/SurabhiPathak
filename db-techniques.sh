#! /usr/bin/bash


# First:

#Created a view on University and Faculty tables for specific positions that are filled in a university
#View make the queries simpler and reduces the overahead of writing long queries too which was the case here

create view univ_faculty_view as select distinct university.name as univ_name from university, faculty where university.id = faculty.university_id and position in ('Project Manager','Professor','Assistant Professor','Associate Professor', 'Professor of Computer Science', 'Assistant Professor of Computer Science', 'Dean','Research Professor, Computer Science','Lecturer','Senior Lecturer');


# Second:

create index keyword_name on keyword (name);

select name as keyword from publication_keyword, publication, keyword where publication_keyword.publication_id = publication.id and keyword.id = publication_keyword. keyword_id  and year >= 2012 group by name order by count(*) desc limit 20;

#Before Indexing time:
#20 rows in set (2.66 sec)

#After indexing on the name column of "keyword" table:
#20 rows in set (2.48 sec)


# Third:

I added a foreign key contraint in the faculty table for university_id to maintain referential integrity with the university table.

mysql> alter table faculty  add constraint foreign key (university_id) references university (id);
Query OK, 5782 rows affected (0.37 sec)
Records: 5782  Duplicates: 0  Warnings: 0







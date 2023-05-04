import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import pymysql


# First Widget

def getAllUniversities (cursor):
 # allUniversities = "select distinct name from university"
 #allUniversities = "select distinct university.name as univ_name from university, faculty where university.id = faculty.university_id and position in ('Project Manager','Professor','Assistant Professor','Associate Professor', 'Professor of Computer Science', 'Assistant Professor of Computer Science', 'Dean','Research Professor, Computer Science','Lecturer','Senior Lecturer')"
 # I am using a mySql View here that replaces the above long query to a simpler one

 # Using a view here----
 allUniversities = "select univ_name from univ_faculty_view"
 cnx = mysql.connector.connect(host='127.0.0.1', user='root', password='Welcome1', database='academicworld')
 cursor = cnx.cursor()
 cursor.execute(allUniversities)
 result = cursor.fetchall()
 cursor.close()
 cnx.close()
 result = [i[0] for i in result]
 return result


def universityId(universityName, cnx):
  universityId='select id from university where name ="' + str(universityName) +'"'
  cnx = mysql.connector.connect(host='127.0.0.1', user='root', password='Welcome1', database='academicworld')
  id = pd.read_sql(universityId, cnx)
  cnx.close()
  return id["id"][0]



def facultyPositions(university_id, cursor):
  allFacultyPositions="select position, count(*) as count from university, faculty where faculty.university_id = university.id and university.id = " +  str(university_id) + " and position in ('Project Manager','Professor','Assistant Professor','Associate Professor', 'Professor of Computer Science', 'Assistant Professor of Computer Science', 'Dean','Research Professor, Computer Science','Lecturer','Senior Lecturer') group by position"
  cnx = mysql.connector.connect(host='127.0.0.1', user='root', password='Welcome1', database='academicworld')
  cursor = cnx.cursor()
  cursor.execute(allFacultyPositions)
  result = cursor.fetchall()
  cursor.close()
  cnx.close()
  #result = [i[0] for i in result]
  return result


  #Second Widget


def getPublicationYears(cursor):
   # years='select distinct year from publication where year >= 2012 order by year desc'
    years = 'select distinct year from publication, faculty_publication where publication.id = faculty_publication.publication_id and year >= 2012'
    cnx = mysql.connector.connect(host='127.0.0.1', user='root', password='Welcome1', database='academicworld')
    cursor = cnx.cursor() 
    #print ("Publication Year is ", years)
    cursor.execute(years)
    years = cursor.fetchall()
    cursor.close()
    years = [i[0] for i in years]
    cnx.close()
   # col_list = df[“year”].values.tolist()
    return years

  
def getPublicationCount(year, cursor):
    #print("Year is " , year)
    #top20PubCount = "select name, count(faculty_publication.publication_id) as publication_count from faculty, faculty_publication, publication where faculty.id = faculty_publication.faculty_id and publication.id = faculty_publication.publication_id and publication.num_citations > 10 and year = " +  str(year) + " group by faculty.name having count(faculty_publication.publication_id) > 10 order by publication_count desc limit 20"
    top20PubCount = "select name as facultyname, count(faculty_publication.publication_id) as publication_count from faculty, faculty_publication, publication where faculty.id = faculty_publication.faculty_id and publication.id = faculty_publication.publication_id and publication.num_citations > 10 and year = " +  str(year) + " group by faculty.name order by publication_count desc limit 20"
    cnx = mysql.connector.connect(host='127.0.0.1', user='root', password='Welcome1', database='academicworld')
    cursor = cnx.cursor()
    cursor.execute(top20PubCount)
    result = cursor.fetchall()
    cursor.close()
    cnx.close()
    return result


 #Third Widget query

def getTop20Publications(year, cursor):
   # print ("Year inside getTop20Pub " + str(year) )
    cnx = mysql.connector.connect(host='127.0.0.1', user='root', password='Welcome1', database='academicworld')
    cursor = cnx.cursor()
    #top20Publications = "select faculty.name as faculty_name, publication.title as publication_title, num_citations from faculty, publication, faculty_publication where faculty.id = faculty_publication.faculty_id and publication.id = faculty_publication.publication_id and year = " + str(year) +  " order by num_citations desc limit 20"
    top20Publications = "select faculty.name as faculty_name, publication.title as publication_title from faculty, publication, faculty_publication where faculty.id = faculty_publication.faculty_id and publication.id = faculty_publication.publication_id and year = " + str(year) +  " order by num_citations desc limit 20"  
    cursor.execute(top20Publications)
    result = cursor.fetchall()
    cursor.close()
    cnx.close()
    return result




  #Fourth Widget query

def getTop20Keywords(cursor):
   # top20Keywords = "select name, count(*) publication_count from publication_keyword, publication, keyword where publication_keyword.publication_id = publication.id and keyword.id = publication_keyword. keyword_id  and year >= 2012 group by name order by publication_count desc limit 20"
    top20Keywords = "select name as keyword from publication_keyword, publication, keyword where publication_keyword.publication_id = publication.id and keyword.id = publication_keyword. keyword_id  and year >= 2012 group by name order by count(*) desc limit 20"
    #print ("INFO top 20 keywords " + top20Keywords)
    cnx = mysql.connector.connect(host='127.0.0.1', user='root', password='Welcome1', database='academicworld')
    cursor = cnx.cursor()
    cursor.execute(top20Keywords)
    result= cursor.fetchall()
    result = [i[0] for i in result]
    cursor.close()
    #print ("top 20 keywords", result)
    cnx.close()
    return result



def getFacultyKRC(keyword, cursor):
    top20keywordRelevance = "select faculty.name as facultyname, sum(publication_keyword.score*publication.num_citations) as krc from faculty, publication, publication_keyword, faculty_publication, keyword where publication_keyword.publication_id = faculty_publication.publication_id and publication.id = publication_keyword.publication_id and keyword.id = publication_keyword.keyword_id  and keyword.name  = '" + str(keyword)  + "' and faculty_publication.faculty_id = faculty.id group by faculty_id order by KRC desc limit 20"
    cnx = mysql.connector.connect(host='127.0.0.1', user='root', password='Welcome1', database='academicworld')
    cursor = cnx.cursor()
    cursor.execute(top20keywordRelevance)
    result = cursor.fetchall()
    cursor.close()
    cnx.close()
    #print ("Faculty KRC" , result)
    return result


  #Update Widget Query
  #select name, phone from faculty where name like 'Alex%';
  #def updateFacultyPhone():
    
    
  # Delete or Add Widget Query

def insert_new_faculty():
  cnx = mysql.connector.connect(host='127.0.0.1', user='root', password='Welcome1', database='academicworld')
  cursor = cnx.cursor()

  add_faculty = ("INSERT INTO faculty_bak_for_updates "
               "(name, position, research_interest, email, phone, photo_url, university_id ) "
               "VALUES (%s, %s, %s, %s, %s)")

    # Insert new faculty
  cursor.execute(add_faculty)
   
  # Make sure data is committed to the database
  cursor.close()
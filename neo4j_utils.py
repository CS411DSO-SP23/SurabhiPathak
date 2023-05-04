

from neo4j import __version__ as neo4j_version
print(neo4j_version)
from neo4j import GraphDatabase
from pandas import DataFrame
import pandas as pd
#import py2neo

class Neo4jConnection:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response


def neo4j_data(univ_name):
    print ("University is " , univ_name)
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="Welcome1")
   
    
    # query_string_2="""
    # MATCH (university:INSTITUTE {name: "University of illinois at Urbana Champaign"})<-[:AFFILIATION_WITH]-(n:FACULTY)-[interested:INTERESTED_IN] -> (k:KEYWORD)  with k as keyword, count(n.name) as faculty_count  RETURN keyword.name, faculty_count order by faculty_count desc limit 20
    # """

    query_string_2=f"MATCH (university:INSTITUTE {{ name: '{univ_name}' }})<-[:AFFILIATION_WITH]-(n:FACULTY)-[interested:INTERESTED_IN] -> (k:KEYWORD)  with k as keyword, count(n.name) as faculty_count RETURN keyword.name, faculty_count order by faculty_count desc limit 20"
    # query_string_2=""""
    # MATCH (university:INSTITUTE)<-[:AFFILIATION_WITH]-(n:FACULTY)-[interested:INTERESTED_IN] -> (k:KEYWORD)  with k as keyword, count(n.name) as faculty_count where university.name = \${"univ_name"} RETURN keyword.name, faculty_count order by faculty_count desc limit 20
    # """
    print ("In Neo4J")
    print (query_string_2)

    dtf_data = DataFrame([dict(_) for _ in conn.query(query_string_2, db='academicworld')])
   # print (dtf_data)
    return dtf_data
    



       
    conn.close()
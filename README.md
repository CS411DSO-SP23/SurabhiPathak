Title: Know your faculties and their publications

Purpose:
(1) The Application will share details about the various faculty positions in the selected university
(2) Faculties associated with publications which have maximum number of citations
(3) Facutlies associated with the top Keyword-Relevance-Citations.
(4) UUIC Faculties contact details and keywords they are interested


Target users of this application are reasearch students and the aspiring students who want to know more about the faculties and universities they are affiliated with.
The main objective of this application is to share the faculty, publications and university details with simple and attractive widgets without getting into the specifics of creating SQL queries to access the database tables.

What is the application scenario? Who are the target users? What are the objectives?

Demo: Give the link to your video demo. Read the video demo section below to understand what contents are expected in your demo.

Installation: I used the existing dataset for all the queries and only created a backup faculty table for add/update operations.

Usage: The application is python/Dash Plotly based with MySQL, Mongo and Neo4j as the backend DBs. A user can build the source on a local VM/Laptop and run it via Chrome/Safari or any of your favorite brower.

Design: The front of the application is based off Dash Plotly and backend is using MySQL, MongoDB and Neo4J queries. The communication between the backend and the front end happens via Dash functons and a combination of Python, Panda, datatable functions as well.

What is the design of the application? Overall architecture and components.
Implementation:  I created multiple .py files dedicated for a specific database queries to keep the functiona manageable. app.py is a glue with Dash/Plotly.
I used python libraries for dash, datatables, pandas to build the application. Visual code is the development env for the application.


Database Techniques: I have implemented three database techniques:
1. Created a view on the Faculty table

2. Create an index on the "name" column of the University Table to improve the performance of the application as I am using this column with multiple widgets.

3. Created a sample table of faculty and added a constraint that phone cannot be null. I added another FK constraint in faculty_publication table referenced to publication.

Extra-Credit Capabilities: What extra-credit capabilities have you developed if any?

Contributions: Worked on this project on my own due to time constraints. Office hours and the TAs helped resolve blocking issues.


List of requirements:
 R1. Useful- the target users will use it for something beneficial : Research students will find the application very useful and will get a high level view of their faculties credentials, publications and strengths across universities and publication years.

 R2. Cool- such an application does not commonly exist today  : The application I have developed is presentable and easy to use. I have not come across such an application in the academic world.

R3, R4 and R5 : I am using the academic world dataset we used for our machine problems.

R6, R7, R8 and R9: I have  six widgets. Five  of them are query widgets and one of the widget is for the add and update operations using MongoDB. I was not able to get the update working but add to the MongoDB document works fine.

I have used Neo4J for the histogram widget and the rest are with MySQL.

R10, R11, R12 : I have used three DB techniques: Indexed a table to a column which was frequently used, Created a view to simplify the length of the query in the application code and added a foreign key constraint on the faculty table for column "university_id" with university table to make sure when a record is added/updated in the faculty table, this constraint makes sure the university_id is present in the university table. It will help with referential integrity. More details on the DB technique commands are in db-techniques.sh file included in the source code.



Media Upload Link: https://mediaspace.illinois.edu/media/t/1_cflga69u 

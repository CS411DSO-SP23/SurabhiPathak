import dash     # need Dash version 1.21.0 or higher
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table, callback             # , ctx # "ctx" is not accessed (Pylance)
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.express as px
from bson import ObjectId           # pip install bson
import pymongo                      # pip install pymongo
from pymongo import MongoClient
from pandas import DataFrame

# Connect to local server
client = MongoClient("mongodb://127.0.0.1:27017/")
# Use the database academicworld
#print(client.list_database_names())
mydb = client["academicworld"]

#print(mydb.list_collection_names())
# Use the collection
collection = mydb.faculty


def showFacultyinfo():
  # Show the faculty member’s name, phone number, and email from a university
  filter_query = {"affiliation.name": "University of illinois at Urbana Champaign"}
  mongoQuery = 'collection.aggregate([{ $match: filter_query }, { $project: { "_id": 0, name: 1, position: 1, email: 1, phone:1 } }, { $sort: { name: 1 } }, {$limit:10}])'
  #mongoQuery = collection.find({'affiliation.name': 'University of illinois at Urbana Champaign'}, { "_id": 0, "name": 1, "position": 1, "email": 1, "phone":1 } ) # works
  mongoQuery = collection.find(filter_query, { "_id": 0, "name": 1, "position": 1, "email": 1, "phone":1 } )
  records_df = DataFrame(list(mongoQuery))
  return records_df


# Update example
  def updateFacultyInfo(currvalue, newvalue):
    myquery = { "address": "Valley 345" }
    newvalues = { "$set": { "address": "Canyon 123" } }

    mycol.update_one(myquery, newvalues)

    #print "customers" after the update:
    for x in mycol.find():
      print(x)






      
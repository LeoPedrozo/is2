# ----- Example Python program to create a database in PostgreSQL using Psycopg2 -----
# import the PostgreSQL client for Python
import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to PostgreSQL DBMS

con = psycopg2.connect("user=postgres host='localhost' password='admin'");

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);

# Obtain a DB Cursor

cursor = con.cursor();

#Nombre de la base de datos
name_Database = "nuevaDB_it5";

# Create table statement

sqlCreateDatabase = "create database " + name_Database + ";"

# Create a table in PostgreSQL database

cursor.execute(sqlCreateDatabase);
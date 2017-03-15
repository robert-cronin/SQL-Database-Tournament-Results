# Title: SQL-Database-Tournament-Results
# Description:
A simple algorithm to record the players, match results and develop swisspairings of a tournament (python code connects to PostgreSQL database)

# Files:
1 - tournament.py
    An implementation of a Swiss-system tournament using sql through the psycopg2 python module. Explanations for each function is given in doc strings of individual definitions
    Author: Robert Cronin

2 - tournament_test.py
    Contains test cases for tournament.py to validate all functions
    Author: Udacity representative

3 - tournament.sql
    Contains table definitions for the Swiss-system tournament

# How to run project:
1 - Initialize the tournament.sql database file using PostgreSQL:
    $ psql tournament.sql

2 - Run through the tournament testing file on CMD line:
    $ python tournament_test.py

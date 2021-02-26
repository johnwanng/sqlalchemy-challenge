# SQLAlchemy Homework - Surfs Up!

## Introduction

The first part of the project uses Python and SQLAlchemy to do basic climate analysis and data exploration of climate database. All of the following analysis are completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

The second part of the project uses Flask API based on the queries that were previously developed in the first part.

These are Flask routes below:

1. /

	Home page. It will list all routes that are available.


2. /api/v1.0/precipitation

	Return the JSON representation of the dictionary using date as the key and prcp as the value.


3. /api/v1.0/stations

	Return a JSON list of stations from the dataset.


4. /api/v1.0/tobs

	Query the dates and temperature observations of the most active station for the last year of data and return a JSON list of temperature observations (TOBS) for the previous year.


5.  /api/v1.0/<start> and /api/v1.0/<start>/<end>

	Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.


# Technologies
 
Python 3.8.5
SQLAlchemy
Flask
 
## Setup 

1. Download and extract the zip file

2. Open Terminal (on Mac) or Open Bash (on PC)

3. Navigate to the sqlalchemy-challenge folder

4. Open the climate_starter.ipynb file and it contains python, sqlalchemy and matplotlib codes that perform the various analysis and ploting result.

5. Open the app.py file and it contains Flask API based routine.

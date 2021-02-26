import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, extract

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite",echo=False)


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start_date> and /api/v1.0/<start>/<end_date> <br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Convert the query results to a dictionary using date as the key and prcp as the value.
    #Return the JSON representation of your dictionary.
    session = Session(engine)
    allPrcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.prcp > 0).order_by(Measurement.date).all()
    session.close()
    all_pre = []
    for date, prcp in allPrcp:
        pre_dict = {}
        pre_dict[date] = prcp
        all_pre.append(pre_dict) 

    return jsonify(all_pre)

@app.route("/api/v1.0/stations")
def stations():
    #Return a JSON list of stations from the dataset.
    session = Session(engine)
    results = session.query(Station.station).order_by(Station.station).all()
    session.close()
    all_stat = []
    for station in results:
        stat_dict = {}
        stat_dict["Station"] = station
        all_stat.append(stat_dict)

    return jsonify(all_stat)


@app.route("/api/v1.0/tobs")
def tobs():
    #Query the dates and temperature observations of the most active station for the last year of data.
    #Return a JSON list of temperature observations (TOBS) for the previous year.    
    session = Session(engine)
    maxDateList = session.query(func.max(Measurement.date)).first()
    year, month, day = map(int, maxDateList[0].split('-'))
    session = Session(engine)
    lastYearMostActive = session.query(Measurement.station, func.count(Measurement.station).label('Station Count')).filter(extract('year',Measurement.date) == year).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == lastYearMostActive[0]).filter(extract('year',Measurement.date) == year).order_by(Measurement.date).all() 
    session.close()

    all_tob = []
    for date, tob in results:
        pre_tob = {}
        pre_tob[date] = tob
        all_tob.append(pre_tob) 

    return jsonify(all_tob)


@app.route("/api/v1.0/<start_date>")
def start(start_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()
    # Create a dictionary from the row data and append to a list of all_statistics
    all_statistics = []
    for Min, Avg, Max in results:
        statistics_dict = {}
        statistics_dict["Minimum"] = Min
        statistics_dict["Average"] = Avg
        statistics_dict["Maximum"] = Max
        all_statistics.append(statistics_dict) 
    return jsonify(all_statistics)

@app.route("/api/v1.0/<start_date>/<end_date>")
def startEnd(start_date,end_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    # Create a dictionary from the row data and append to a list of all_statistics
    all_statistics = []
    for Min, Avg, Max in results:
        statistics_dict = {}
        statistics_dict["Minimum"] = Min
        statistics_dict["Average"] = Avg
        statistics_dict["Maximum"] = Max
        all_statistics.append(statistics_dict)
    return jsonify(all_statistics)


if __name__ == "__main__":
    app.run(debug=True)


import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table

Measure = Base.classes.measurement
Station = Base.classes.station

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
        f"--------------------------<br/>"
        f"To know all precipitations:<br/>          /api/v1.0/precipitation <br/><br/>"
        f"Display all the stations:  <br/>     /api/v1.0/stations<br/><br/>"
        f"Search the tobs for a specific station: <br/>    /api/v1.0/tobs<br/><br/>"
        f"To kwnon the statistic for the most observed station (insert the date like the format given): <br/>/api/v1.0/start/yyyy-mm-dd <br/><br/>"
        f"Search the statistics for a given dates: <br/> /api/v1.0/start/end//yyyy-mm-dd/yyyy-mm-dd<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
# Create our session (link) from Python to the DB
    session = Session(engine)

    """Retuurn a list of all precipitations"""
    # Query all passengers
    results = session.query(Measure.date,Measure.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/stations")
def station():
# Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all passengers
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def stationmoreob():
# Create our session (link) from Python to the DB
    session = Session(engine)

       
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    station = 'USC00519397'
    # Query all tobs given the station and the date
    results = session.query(Measure.tobs).\
    filter(func.strftime("%Y-%m-%d", Measure.date)>= query_date ).\
    filter(Measure.station==station).all()

    session.close()

    # Convert list of tuples into normal list
    tobs = list(np.ravel(results))

    return jsonify(tobs)

@app.route("/api/v1.0/start/<start>")
def startdate(start):
# Create our session (link) from Python to the DB
    session = Session(engine)    
    
    query_date = start
    station = 'USC00519397'
    # Query all tobs given the station and the date
    results =     session.query(
        Measure.station,func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs)
    ).filter(func.strftime("%Y-%m-%d", Measure.date)>= query_date ).filter(Measure.station==station).all()


    session.close()

    # Convert list of tuples into normal list
    statistics = list(np.ravel(results))

    return jsonify(statistics)

@app.route("/api/v1.0/start/end/<start>/<end>")
def startend(start,end):
# Create our session (link) from Python to the DB
    session = Session(engine)    
    
    start_date = start
    end_date = end
    station = 'USC00519397'
    # Query all tobs given the station and the date
    results =session.query(func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs)).\
        filter(Measure.date >= start_date).filter(Measure.date <= end_date).all()


    session.close()

    # Convert list of tuples into normal list
    statistics = list(np.ravel(results))

    return jsonify(statistics)


# @TODO: Complete the routes for your app here
# YOUR CODE GOES HERE

if __name__ == "__main__":
    # @TODO: Create your app.run statement here
    # YOUR CODE GOES HERE
    app.run(debug=True)

import datetime as dt
import numpy as np
import pandas as pd

# Import SQLite dependencies after the other dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Set up the Database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create a variable for each of the classes so that it can be 
# referenced later. 
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to the database
session = Session(engine)

# Set up Flask app
app = Flask(__name__)

# Define the welcome route (or root) using this code
@app.route("/")

#Create a welcome  function
def welcome():
    return(
        '''
        Welcome to the Climate Analysis API!
        Available Routes:
        /api/v1.0/percipitation
        /api/v1.0/stations
        /api/v1.0/tobs
        /api/v1.0/temp/start/end
        ''' )

# Create a precipitation route
# Get the date and precipitation for the previous year.
@app.route("/api/v1.0/precipitation")
# def precipitation():
#     prev_year = dt.date(2017, 8, 23) - dt.timedelata(days=365)
#     precipitation = session.query(Measurement.date, Measurement.prcp).\
#         filter(Measurement.date >= prev_year).all()
#     precip = {date: prcp for date, prcp in precipitation}
#     return jsonify(precip)

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Create the Station route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
    
# Create monthly temperature route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Create Statistics Route

# @app.route("/api/v1.0/temp/start/end")

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        resutls = session.query(*sel).\
            filter(Measurement.date >= start).ass()
        temps = list(np.ravel(results))
        return jsonify(temps = temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

### DID NOT WORK!! 

if __name__ == "__main__":
    # @TODO: Create your app.run statement here
    # YOUR CODE GOES HERE
    app.run(debug=True)

# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create the engine using the sqlite file in Resources
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Breakdown of the routes, including instructions on how to query the dynamic routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Static Routes:<br/>"
        "<br/>"
        f"/api/v1.0/<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        "<br/>"
        f"Dynamic Routes:<br/>"
        "<br/>"
        f"Type the Start Date after /api/v1.0/ in YYYY-MM-DD format, followed by a second / and the End Date, also in YYYY-MM-DD format. <br/>"
        "<br/>"
        f"/api/v1.0/<start><br/>" 
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    one_year_precip = session.query(Measurement.date, Measurement.prcp).\
                        filter(Measurement.date >= '2016-08-23').\
                        order_by(Measurement.date).all()
    
    session.close()

    # Convert the query to a list of dictionaries
    one_year_precip_list = [{'date': date,
                             'prcp': prcp}
                             for date, prcp in one_year_precip]
    
    return jsonify(one_year_precip_list)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the station data
    station_result = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Convert the query to a list of dictionaries
    station_list = [{'station': station,
                     'name': name,
                     'latitude': latitude,
                     'longitude': longitude,
                     'elevation': elevation}
                     for station, name, latitude, longitude, elevation in station_result]
    
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve observations from the most-active station
    temperature_data = session.query(Measurement.date, Measurement.tobs, Measurement.station).\
                                    filter(Measurement.station == 'USC00519281').\
                                    filter(Measurement.date >= '2016-08-18').all()
    session.close()

    # Convert the query to a list of dictionaries
    temperature_list = [{'date': date,
                         'tobs': tobs, 
                         'station': station}
                         for date, tobs, station in temperature_data]
    
    return jsonify(temperature_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the minimum, maximum, and average temperatures observed from the state date to the most recent entry
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                            filter(Measurement.date >= start).all()
    session.close()

    # Extract the values from the query result
    tmin, tmax, tavg = results[0]

    # Convert the query to a list of dictionaries
    result_dict = {'start_date': start,
                   'tmin': tmin,
                   'tmax': tmax,
                   'tavg': tavg}

    return jsonify(result_dict)

@app.route("/api/v1.0/<start>/<end>")
def date_range(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the minimum, maximum, and average temperatures observed from the state date to the end date
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                            filter(Measurement.date >= start).\
                            filter(Measurement.date <= end).all()
    session.close()

    # Extract the values from the query result
    tmin, tmax, tavg = results[0]

    # Convert the query to a list of dictionaries
    result_dict = {'start_date': start,
                   'end_date': end,
                   'tmin': tmin,
                   'tmax': tmax,
                   'tavg': tavg}

    return jsonify(result_dict)

if __name__ == '__main__':
    app.run(debug=True)
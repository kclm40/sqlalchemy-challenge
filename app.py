#dependencies

import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

#save references
Measurement = Base.classes.measurement
Station = Base.classes.station

#setup Flask

app = Flask(__name__)

#Flask Routes
@app.route("/")
def homepage():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/prcp<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start format:yyyy-mm-dd]/[end format:yyyy-mm-dd]<br/>"
    )


@app.route("/api/v1.0/prcp")
def prcp():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-24').filter(Measurement.date <= '2017-08-23').order_by(Measurement.date.asc()).all()

    session.close()

#convert the query results to a dictionary using date as the key and prcp as the value
    all_prcp = [] 
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        all_prcp.append(prcp_dict)

#return the JSON representation of your dictionary
    return jsonify(all_prcp)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/station")
def station():
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


#Query the dates and temperature observations of the most active station for the previous year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    most_active = 'USC00519281'

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-24').filter(Measurement.date <= '2017-08-23').filter(Measurement.station == most_active).order_by(Measurement.date).all()
    session.close()

    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates from the start date through the end date (inclusive).

@app.route("/api/v1.0/<start>")
def Start(start):
    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()
    

    all_start = [] 
    for min, avg, max in results:
        all_start_dict = {}
        all_start_dict["Min_Temperature"] = min
        all_start_dict["Avg_Temperature"] = avg
        all_start_dict["Max_Temperature"] = max
        all_start.append(all_start_dict)

    return jsonify(all_start)

@app.route("/api/v1.0/<start>/<end>")
def Start_end_date(start, end):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    start_end = []
    for min, avg, max in results:
        start_end_dict = {}
        start_end_dict["Min_Temperature"] = min
        start_end_dict["Avg_Temperature"] = avg
        start_end_dict["Max_Temperature"] = max
        start_end.append(start_end_dict)

    return jsonify(start_end)

if __name__ == '__main__':
    app.run(debug=True)





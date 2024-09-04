from flask import jsonify, request, current_app as app, abort
from database_prod.data_types import *
import datetime

def get_class_by_name(class_name):
    try:
        model_class = globals()[class_name]
        return model_class
    except KeyError:
        return None

def get_instrument_id_by_class_name(class_name, session):
    """Fetch InstrumentId from the Instruments table based on class name."""
    instrument = session.query(Instrument).filter_by(name=class_name).first()
    if instrument:
        return instrument.id
    else:
        return None

@app.route('/checkConnection', methods=['GET'])
def check_connection():
    return jsonify({"message": "Connection successful!"}), 200

@app.route('/getClass/<class_name>', methods=['GET'])
def get_class(class_name):
    try:
        model_class = get_class_by_name(class_name)
        
        if model_class is None:
            abort(404, description=f"Class '{class_name}' not found.")

        session = app.session()
        results = session.query(model_class).all()
        
        results_list = [result.to_dict() for result in results]

        return jsonify(results_list)

    except Exception as e:
        abort(400, description=f"An error occurred: {str(e)}")

@app.route('/bookTrade/<class_name>', methods=['POST'])
def book_trade(class_name):
    session = None
    try:
        # Get the model class by name (e.g., 'Options')
        model_class = get_class_by_name(class_name)
        if model_class is None:
            abort(404, description=f"Class '{class_name}' not found.")

        session = app.session()
        instrument_id = get_instrument_id_by_class_name(class_name, session)
        if instrument_id is None:
            abort(404, description=f"Instrument not found for class '{class_name}'.")

        print("instrumentId", instrument_id)

        # Get the data from the request body (except for 'tradeID')
        trade_data = request.get_json()
        if not trade_data:
            abort(400, description="No data provided in the request body.")
        
        # Create a new row in the 'Trades' table with the current UTC timestamp
        new_trade = Trade(timestamp=datetime.datetime.now(datetime.UTC), instrument_id=instrument_id)
        session.add(new_trade)
        session.commit()

        # Get the trade ID for the newly created trade
        trade_id = new_trade.id
        print("trade_id", trade_id)

        # Add a new row to the specific class table (e.g., 'Options') with the provided data
        trade_data['trade_id'] = trade_id  # Add the tradeID to the data
        new_row = model_class(**trade_data)  # Use the model to create a new row instance
        session.add(new_row)
        session.commit()

        return jsonify({"message": "Trade booked successfully!", "id": trade_id}), 201
    
    except Exception as e:
        if session:
            session.rollback()
        abort(400, description=f"An error occurred: {str(e)}")
    finally:
        if session:
            session.close()
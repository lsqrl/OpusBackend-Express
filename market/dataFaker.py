import os
from flask import Flask, jsonify, request
import numpy as np
from scipy.stats import truncnorm
from threading import Lock
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Initialize the spot value and a lock for thread safety
spot = 1.1
rate = 0.04
volatility = 0.01

spot_lock = Lock()

are_set = False

CORS(app, resources={r"/*": {"origins": os.getenv("FRONTEND_ORIGIN")}})

# TODO: 3/3 Have getNumbers for Euro, BTC (around 58.444k) and ETH (around 2.282k)
@app.route('/getNumbers')
def get_numbers():
    global spot, are_set, rate, volatility
    current_spot = {
        'EURO': spot,
        'BTC': spot*65740,
        'ETH': spot*2478}
    if not are_set:
        # Generate rate from a normal distribution
        epsilon = np.random.normal(0, volatility)

        # Update the spot value with 50/50 probability of increasing or decreasing
        with spot_lock:
            if np.random.rand() > 0.5:
                spot *= (1 + epsilon)
            else:
                spot *= (1 - epsilon)
        current_spot = {
            'EURO': spot,
            'BTC': spot*65740,
            'ETH': spot*2478
            }
    # Return the results as JSON
    return jsonify({
        'spot': current_spot,
        'rate': rate,
        'volatility': volatility
    })

    # {'currency': 'value'} x 3

@app.route('/setValues', methods=['POST'])
def set_values():
    global spot, volatility, rate, are_set

    # Extract values from the JSON payload
    data = request.json

    new_spot = data.get('spot')
    new_volatility = data.get('volatility')
    new_rate = data.get('rate')

    # Lock the spot update for thread safety
    with spot_lock:
        if new_spot is not None:
            spot = new_spot
        if new_volatility is not None:
            volatility = new_volatility
        if new_rate is not None:
            rate = new_rate
    are_set =  True
    return jsonify({
        'message': 'Values updated successfully',
        'spot': spot,
        'volatility': volatility,
        'rate': rate
    })


@app.route('/reset', methods=['GET'])
def reset():
    global are_set
    are_set =  False
    return jsonify({
        'message': 'Reset succeeded'
    })


# Route to list all implemented API methods
@app.route('/methods', methods=['GET'])
def list_api_methods():
    """Endpoint to list all the implemented API methods"""
    output = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint not in ['static', 'list_api_methods']:
            methods = ', '.join(rule.methods - {"OPTIONS", "HEAD"})
            output.append({
                "endpoint": rule.endpoint,
                "url": rule.rule,
                "methods": methods
            })
    return jsonify(output)

if __name__ == '__main__':
    app.run(host=os.getenv("BASE_URL"), port=5004) # host="0.0.0.0",

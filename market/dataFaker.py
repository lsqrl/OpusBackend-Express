import os
from flask import Flask, jsonify, request
import numpy as np
from scipy.stats import truncnorm
from threading import Lock
from flask_cors import CORS

app = Flask(__name__)

# Initialize the spot value and a lock for thread safety
spot = 1.1
spot_lock = Lock()

are_set = False

CORS(app, resources={r"/*": {"origins": "https://opusdigital.vercel.app"}})

# TODO: 3/3 Have getNumbers for Euro, BTC (around 58.444k) and ETH (around 2.282k)
@app.route('/getNumbers')
def get_numbers():
    global spot, are_set
    current_spot = {
        'EURO': spot,
        'BTC': spot*58412,
        'ETH': spot*2246}
    if not are_set:
        # Generate volatility from a truncated normal distribution (always positive)
        mean_vol = 0.1
        std_vol = 0.1
        a, b = (0 - mean_vol) / std_vol, np.inf  # Truncate at 0 to ensure positivity
        volatility = truncnorm.rvs(a, b, loc=mean_vol, scale=std_vol)
        # Ensure volatility is strictly between 0.01 and 0.9
        volatility = max(min(volatility, 0.9), 0.01)

        # Generate rate from a normal distribution
        mean_rate = 0.04
        std_rate = 0.03
        rate = np.random.normal(mean_rate, std_rate)

        # Randomly decide to multiply rate by (1 + epsilon) or (1 - epsilon)
        epsilon = volatility
        if np.random.rand() > 0.5:
            rate *= (1 + epsilon)
        else:
            rate *= (1 - epsilon)

        # Update the spot value with 50/50 probability of increasing or decreasing
        with spot_lock:
            if np.random.rand() > 0.5:
                spot *= (1 + epsilon)
            else:
                spot *= (1 - epsilon)
        current_spot = {
            'EURO': spot,
            'BTC': spot*58412,
            'ETH': spot*2246
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


@app.route('/reset', methods=['POST'])
def reset():
    global are_set
    are_set =  False
    return None


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

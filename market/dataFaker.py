from flask import Flask, jsonify, request
import numpy as np
from scipy.stats import truncnorm
from threading import Lock

app = Flask(__name__)

# Initialize the spot value and a lock for thread safety
spot = 1.1
spot_lock = Lock()

@app.route('/getNumbers')
def get_numbers():
    global spot

    # Generate volatility from a truncated normal distribution (always positive)
    mean_vol = 0.01
    std_vol = 0.01
    a, b = (0 - mean_vol) / std_vol, np.inf  # Truncate at 0 to ensure positivity
    volatility = truncnorm.rvs(a, b, loc=mean_vol, scale=std_vol)

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
        current_spot = spot  # Store the updated spot value

    # Return the results as JSON
    return jsonify({
        'spot': current_spot,
        'rate': rate,
        'volatility': volatility
    })

@app.route('/setValues', methods=['POST'])
def set_values():
    global spot, volatility, rate

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

    return jsonify({
        'message': 'Values updated successfully',
        'spot': spot,
        'volatility': volatility,
        'rate': rate
    })


if __name__ == '__main__':
    app.run(port=5004)

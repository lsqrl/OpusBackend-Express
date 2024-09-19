from flask import Flask, jsonify
from pricer.api.utils import calculate_option_greeks, calculate_option_price  # Importing the function from fetchOptionDelta.py

app = Flask(__name__)

@app.route('/calculateGreeks', methods=['GET'])
def calculate_greeks():
    try:
        # Hardcoded values for volatility, rate, and spot
        volatility = 0.2  # Example hardcoded volatility
        rate = 0.05       # Example hardcoded risk-free rate
        spot = 1.1        # Example hardcoded spot price
        
        delta, gamma, theta, vega = calculate_option_greeks(volatility, rate, spot)
        
        # Return the result as a JSON response
        return jsonify({
            'delta': delta,
            'gamma': gamma,
            'theta': theta,
            'vega': vega
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/calculatePrice', methods=['GET'])
def calculate_price():
    try:
        # Hardcoded values for volatility, rate, and spot
        volatility = 0.2  # Example hardcoded volatility
        rate = 0.05       # Example hardcoded risk-free rate
        spot = 1.1        # Example hardcoded spot price
        
        price = calculate_option_price(volatility, rate, spot)
        
        # Return the result as a JSON response
        return jsonify({'price': price})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(port=5001,debug=True)

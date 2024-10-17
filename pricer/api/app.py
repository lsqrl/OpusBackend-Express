import os
import requests
from flask import Flask, jsonify
from pricer.api.utils import calculate_option_greeks, calculate_option_price  # Importing the function from fetchOptionDelta.py

app = Flask(__name__)

@app.route('/calculateGreeks', methods=['GET'])
def calculate_greeks():
    try:
        market_response = requests.get('http://localhost:5004/getNumbers')
        if market_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch market data from external service'}), 500
        volatility = float(market_response.json().get('volatility'))
        rate = float(market_response.json().get('rate'))
        spot = float(market_response.json().get('spot'))
        
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
        market_response = requests.get('http://localhost:5004/getNumbers')
        if market_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch market data from external service'}), 500
        volatility = float(market_response.json().get('volatility'))
        rate = float(market_response.json().get('rate'))
        spot = float(market_response.json().get('spot'))
        
        price = calculate_option_price(volatility, rate, spot)
        
        # Return the result as a JSON response
        return jsonify({'price': price})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

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
    app.run(host=os.getenv("BASE_URL"), port=5001, debug=True)


# TODO: 2/3 add a POST request that calls option_price(strike, expiry, rate, volatility, notional, spot, option_type)
# which is in pricer\analytics\optionPrice.py
# if spot, volatility, rate are not in the request body, then they are taken from localhost:5004/market/getNumbers
# otherwise they are from request body.
# also, add the currency in request body so that you can filter through the response of getNumbers
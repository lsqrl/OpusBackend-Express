import os
import requests
from flask import Flask, jsonify, request
from pricer.api.utils import calculate_option_greeks, calculate_option_price  # Importing the function from fetchOptionDelta.py
from pricer.analytics.optionPrice import option_price
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "https://opusdigital.vercel.app"}})

@app.route('/calculateGreeks', methods=['GET'])
def calculate_greeks():
    currency = request.args.get('currency')
    try:
        market_response = requests.get(f"http://{os.getenv("BASE_URL")}:5004/getNumbers")
        if market_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch market data from external service'}), 500
        volatility = float(market_response.json().get('volatility'))
        rate = float(market_response.json().get('rate'))
        spot = float(market_response.json().get('spot')[currency])
        
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
    currency = request.args.get('currency')
    try:
        market_response = requests.get(f"http://{os.getenv("BASE_URL")}:5004/getNumbers")
        if market_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch market data from external service'}), 500
        volatility = float(market_response.json().get('volatility'))
        rate = float(market_response.json().get('rate'))
        spot = float(market_response.json().get('spot')[currency])
        
        price = calculate_option_price(volatility, rate, spot)
        
        # Return the result as a JSON response
        return jsonify({'price': price})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# TODO: 2/3 
# if spot, volatility, rate are not in the request body, then they are taken from localhost:5004/market/getNumbers
# also, add the currency in request body so that you can filter through the response of getNumbers
@app.route('/priceOption', methods=['POST'])
def price_option():
    try:
        data = request.get_json()
        
        # Extract the parameters from the request body
        strike = data.get('strike')
        expiry = data.get('expiry')
        notional = data.get('notional')
        option_type = data.get('option_type')
        currency = data.get('currency')

        # Check if spot, volatility, and rate are provided, otherwise fetch from the external service
        spot = data.get('spot')
        volatility = data.get('volatility')
        rate = data.get('rate')

        if spot is None or volatility is None or rate is None:
            response = requests.get(f"http://{os.getenv("BASE_URL")}:5004/getNumbers")
            if spot is None:
                spot = float(response.json().get('spot')[currency])
            if volatility is None:
                volatility = float(response.json().get('volatility'))
            if rate is None:
                rate = float(response.json().get('rate'))
        
        price = option_price(strike, expiry, rate, volatility, notional, spot, option_type)
        return jsonify({'price': price}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
    app.run(host=os.getenv("BASE_URL"), port=5001,debug=True)


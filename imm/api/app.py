import os
import requests
from flask import Flask, request, jsonify
from pricer.analytics.optionDelta import option_delta  # Assuming optionDelta is in pricer.analytics
from datetime import datetime, timezone
from pricer.analytics.optionPrice import option_price
from pricer.analytics.optionDelta import option_delta
from pricer.analytics.optionVega import option_vega
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)

# Once we can mark to market everything and the ARM, we use their inputs to adjust our prices: that’s the IMM. Examples:

# - We need to decrease Delta (ARM) → we will decrease the price to buy calls.
# - A given trade would bring us to a position costly to hedge (ARM) → we will increase the price for that trade.

## MVP

# Modification of Black-Scholes pricing for new options.

# V=V_{\text{BS}}+\varepsilon(\delta_{\text{portfolio}})

# - After the ARM

# - When you display the price of an option, you first calculate its “fair price” via BS (ChatGPT given),
# then you add or subtract some amount depending on our risk.

# - The idea is to decrease the Delta, always. So if a new option increases our Delta, then its price should be *higher* than BS. 
# If it decreases it, price should be *lower* than BS.

load_dotenv()
CORS(app, resources={r"/*": {"origins": os.getenv("FRONTEND_ORIGIN")}})


@app.route('/displayAdjustedPrice', methods=['POST'])
# Given data for an option, display the adjusted price
# Adjusted = "pricer price" + "arm contribution"
def display_adj_price():
    try:
        # TODO: 1/3 again add a currency in the request body so that you can filter through the response of getNumbers
        # and again, if spot, volatility, rate are in the request body, then you do not take them from getNumbers
        # if vega and delta (both!) are in the request body, then you do not call calculateGreek
        data = request.json
        strike = data.get('strike')
        expiry_time = data.get('expiry_time')
        notional = data.get('notional')
        option_type = data.get('type')
        currency = data.get('currency')
        vega = data.get('vega')
        delta = data.get('delta')
        historical_vol = data.get('historical_vol')

        if currency is None:
            currency = "EURO"

        expiry_datetime = datetime.strptime(expiry_time, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)

        # Get the current time as a timezone-aware datetime in UTC
        current_time = datetime.now(timezone.utc)

        # Calculate the time to expiry in years
        time_to_expiry = (expiry_datetime - current_time).days / 365.0

        
        # Check if spot, volatility, and rate are provided, otherwise fetch from the external service
        spot = data.get('spot')
        volatility = data.get('volatility')
        rate = data.get('rate')

        if spot is None or volatility is None or rate is None:    
            market_response = requests.get(f"http://{os.getenv("BASE_URL")}:5004/getNumbers")

            if market_response.status_code != 200:
                return jsonify({'error': 'Failed to fetch market data from external service'}), 500
            if volatility is None:
                volatility = float(market_response.json().get('volatility'))
            if rate is None:
                rate = float(market_response.json().get('rate'))
            if spot is None:
                spot = float(market_response.json().get('spot')[currency])
        p1 = option_price(strike, time_to_expiry, rate, volatility, notional, spot, option_type)

        d1 = option_delta(strike, time_to_expiry, rate, volatility, notional, spot, option_type)

        v1 = option_vega(strike, time_to_expiry, rate, volatility, notional, spot, option_type)

        if vega is None or delta is None:
            response = requests.get(f"http://{os.getenv("BASE_URL")}:5001/calculateGreeks", params={'currency': currency})
            if response.status_code == 200:
                D = response.json().get('delta')
                V = response.json().get('vega')
            else:
                return jsonify({"error": "Could not fetch portfolio greeks"}), 500
        else:
            D = delta
            V = vega
        
        # Step 4: Default bid and ask calculations
        default_bid = p1 * 0.95  # p1 - 5%
        default_ask = p1 * 1.05  # p1 + 5%

        # Step 5: Calculate final bid and ask

        adjustment = p1 * round(historical_vol // 0.1 * 0.1, 1) * (1 + V / 100000)

        final_bid = default_bid - adjustment
        final_ask = default_ask + adjustment

        # Return the final bid and ask as JSON
        return jsonify({
            "option_delta": d1,
            "portfolio_delta": D,
            "option_vega": v1,
            "portfolio_vega": V,
            "fair_price": p1,
            "bid": final_bid,
            "ask": final_ask
        })
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
    app.run(host=os.getenv("BASE_URL"), port=5003)

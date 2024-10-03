import requests
from flask import Flask, request, jsonify
from pricer.analytics.optionDelta import option_delta  # Assuming optionDelta is in pricer.analytics
from datetime import datetime, timezone
from pricer.analytics.optionPrice import option_price
from pricer.analytics.optionDelta import option_delta
from pricer.analytics.optionVega import option_vega

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

# Hardcoded values for volatility, rate, and spot
VOLATILITY = 0.2  # example value
RATE = 0.05       # example value
SPOT = 1.1        # example value

@app.route('/displayAdjustedPrice', methods=['POST'])
# Given data for an option, display the adjusted price
# Adjusted = "pricer price" + "arm contribution"
def display_adj_price():
    try:
        data = request.json
        strike = data.get('strike')
        expiry_time = data.get('expiry_time')
        notional = data.get('notional')
        option_type = data.get('type')

        expiry_datetime = datetime.strptime(expiry_time, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)

        # Get the current time as a timezone-aware datetime in UTC
        current_time = datetime.now(timezone.utc)

        # Calculate the time to expiry in years
        time_to_expiry = (expiry_datetime - current_time).days / 365.0
        
        p1 = option_price(strike, time_to_expiry, RATE, VOLATILITY, notional, SPOT, option_type)

        d1 = option_delta(strike, time_to_expiry, RATE, VOLATILITY, notional, SPOT, option_type)

        v1 = option_vega(strike, time_to_expiry, RATE, VOLATILITY, notional, SPOT, option_type)

        response = requests.get('http://localhost:5001/calculateGreeks')
        if response.status_code == 200:
            D = response.json().get('delta')
            V = response.json().get('vega')
        else:
            return jsonify({"error": "Could not fetch portfolio greeks"}), 500
        
        # Step 4: Default bid and ask calculations
        default_bid = p1 * 0.95  # p1 - 5%
        default_ask = p1 * 1.05  # p1 + 5%

        # Step 5: Calculate final bid and ask
        final_bid = default_bid * (1 - d1 / D) * (1 - v1 / V)
        final_ask = default_ask * (1 + d1 / D) * (1 - v1 / V)

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
    app.run(port=5003)

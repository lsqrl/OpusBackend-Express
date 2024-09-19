import requests
from flask import Flask, request, jsonify
from pricer.analytics.optionDelta import option_delta
from pricer.analytics.optionVega import option_vega
from datetime import datetime, timezone

app = Flask(__name__)

# Hardcoded threshold value
DELTA_THRESHOLD = 1000000
VEGA_THRESHOLD = 1000000
GAMMA_THRESHOLD = 10000000
THETA_THRESHOLD = 1000000

@app.route('/bookFXOption', methods=['POST'])
def generate_post_request():
    try:
        # Step 1: Extract query parameters from the GET request
        data = request.json
        underlying_id = data.get('underlying_id')
        accounting_id = data.get('accounting_id')
        bank_account_id = data.get('bank_account_id')
        premium_currency_id = data.get('premium_currency_id')
        option_type = data.get('type')  # CALL or PUT
        direction = data.get('direction')  # BUY or SELL
        notional = float(data.get('notional'))
        strike = float(data.get('strike'))
        premium_settlement_date = data.get('premium_settlement_date')
        expiry_time = data.get('expiry_time')

        greek_response = requests.get('http://localhost:5001/calculateGreeks')
        if greek_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch greeks from external service'}), 500
        d1 = float(greek_response.json().get('delta'))
        v1 = float(greek_response.json().get('vega'))

        # Step 3: Calculate d2 using pricer.analytics.optionDelta
        # Example arguments for optionDelta - adjust as needed for your function's signature
        # Convert expiry_time to a timezone-aware datetime object in UTC
        expiry_datetime = datetime.strptime(expiry_time, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)

        # Get the current time as a timezone-aware datetime in UTC
        current_time = datetime.now(timezone.utc)

        # Calculate the time to expiry in years
        time_to_expiry = (expiry_datetime - current_time).days / 365.0

        #TODO: fetch market data
        volatility = 0.2  # Example hardcoded volatility
        rate = 0.05       # Example hardcoded risk-free rate
        spot = 1.1        # Example hardcoded spot price

        d2 = option_delta(strike, time_to_expiry, rate, volatility, notional, spot, option_type)
        v2 = option_vega(strike, time_to_expiry, rate, volatility, notional, spot, option_type)

        # Step 4: Check if d1 + d2 is greater than the threshold# Step 4: Check if d1 + d2 is greater than the threshold
        delta_sum = d1 + d2
        if delta_sum > DELTA_THRESHOLD:
            return jsonify({
                'error': 'Delta sum exceeds threshold',
                'original_delta': d1,
                'new_delta': d2,
                'delta_sum': delta_sum,
                'delta_threshold': DELTA_THRESHOLD
            }), 400
        
        vega_sum = v1 + v2
        if vega_sum > VEGA_THRESHOLD:
            return jsonify({
                'error': 'Vega sum exceeds threshold',
                'original_vega': v1,
                'new_vega': v2,
                'vega_sum': vega_sum,
                'vega_threshold': VEGA_THRESHOLD
            }), 400

        # Step 5: Prepare the POST request body
        post_data = {
            "underlying_id": underlying_id,
            "accounting_id": accounting_id,
            "bank_account_id": bank_account_id,
            "premium_currency_id": premium_currency_id,
            "type": option_type,
            "direction": direction,
            "notional": notional,
            "strike": strike,
            "premium_settlement_date": premium_settlement_date,
            "expiry_time": expiry_time
        }

        # Step 6: Send the POST request to bookTrade endpoint
        post_response = requests.post(
            'http://localhost:5000/bookTrade/FXOption/FXOption',
            json=post_data,
            headers={'Content-Type': 'application/json'},
            timeout=20  # Wait up to 20 seconds for a response
        )

        if post_response.status_code == 201:
            return jsonify({'message': 'Trade booked successfully'}), 200
        else:
            return jsonify({'error': 'Failed to book trade'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5002)

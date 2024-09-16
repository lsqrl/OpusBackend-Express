from flask import Flask, jsonify
from arm.fetchOptionDelta import calculate_option_delta  # Importing the function from fetchOptionDelta.py

app = Flask(__name__)

@app.route('/calculateDelta', methods=['GET'])
def calculate_delta():
    try:
        # Hardcoded values for volatility, rate, and spot
        volatility = 0.2  # Example hardcoded volatility
        rate = 0.05       # Example hardcoded risk-free rate
        spot = 1.1        # Example hardcoded spot price
        
        # Call the calculate_option_delta function from fetchOptionDelta.py
        delta = calculate_option_delta(volatility, rate, spot)
        
        # Return the result as a JSON response
        return jsonify({'delta': delta})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5001,debug=True)

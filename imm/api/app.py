import requests
from flask import Flask, request, jsonify
from pricer.analytics.optionDelta import option_delta  # Assuming optionDelta is in pricer.analytics
from datetime import datetime, timezone

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

@app.route('/displayAdjustedPrice', methods=['POST'])
# Given data for an option, display the adjusted price
# Adjusted = "pricer price" + "arm contribution"
def display_adj_price():
    return 0 

if __name__ == '__main__':
    app.run(port=5003)

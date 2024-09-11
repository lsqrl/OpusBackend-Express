import math
from scipy.stats import norm

def option_price(strike, expiry, rate, volatility, notional, spot, option_type):
    """
    Calculate the price of a European option using the Black-Scholes formula.
    
    Parameters:
    strike (float): Strike price of the option.
    expiry (float): Time to expiry in years.
    rate (float): Risk-free interest rate (annualized).
    volatility (float): Volatility of the underlying asset (annualized).
    notional (float): Notional amount of the option.
    spot (float): Spot price of the underlying asset.
    option_type (str): Type of the option ('call' or 'put'). Default is 'call'.
    
    Returns:
    float: Price of the option.
    """
    
    # Calculate d1 and d2
    d1 = (math.log(spot / strike) + (rate + 0.5 * volatility ** 2) * expiry) / (volatility * math.sqrt(expiry))
    d2 = d1 - volatility * math.sqrt(expiry)
    
    if option_type == 'call':
        # Call option price
        price = (spot * norm.cdf(d1) - strike * math.exp(-rate * expiry) * norm.cdf(d2)) * notional
    elif option_type == 'put':
        # Put option price
        price = (strike * math.exp(-rate * expiry) * norm.cdf(-d2) - spot * norm.cdf(-d1)) * notional
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")
    
    return price

# # Example usage
# strike_price = 100
# expiry_in_years = 1
# risk_free_rate = 0.05
# volatility = 0.2
# notional_amount = 1000
# spot_price = 105

# # Call option price
# call_price = option_price(strike_price, expiry_in_years, risk_free_rate, volatility, notional_amount, spot_price, option_type='call')
# print(f"Call option price: {call_price}")

# # Put option price
# put_price = option_price(strike_price, expiry_in_years, risk_free_rate, volatility, notional_amount, spot_price, option_type='put')
# print(f"Put option price: {put_price}")

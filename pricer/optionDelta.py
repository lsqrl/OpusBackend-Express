import math
from scipy.stats import norm

def option_delta(strike, expiry, rate, volatility, notional, spot, option_type):
    """
    Calculate the delta of a European option using the Black-Scholes formula.
    
    Parameters:
    strike (float): Strike price of the option.
    expiry (float): Time to expiry in years.
    rate (float): Risk-free interest rate (annualized).
    volatility (float): Volatility of the underlying asset (annualized).
    notional (float): Notional amount of the option.
    spot (float): Spot price of the underlying asset.
    option_type (str): Type of the option ('call' or 'put'). Default is 'call'.
    
    Returns:
    float: Delta of the option.
    """
    
    # Calculate d1
    d1 = (math.log(spot / strike) + (rate + 0.5 * volatility ** 2) * expiry) / (volatility * math.sqrt(expiry))
    
    if option_type == 'call':
        # Call option delta
        delta = norm.cdf(d1) * notional
    elif option_type == 'put':
        # Put option delta
        delta = (norm.cdf(d1) - 1) * notional
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")
    
    return delta

# # Example usage
# strike_price = 100
# expiry_in_years = 1
# risk_free_rate = 0.05
# volatility = 0.2
# notional_amount = 1000
# spot_price = 105

# # Call option delta
# call_delta = option_delta(strike_price, expiry_in_years, risk_free_rate, volatility, notional_amount, spot_price, option_type='call')
# print(f"Call option delta: {call_delta}")

# # Put option delta
# put_delta = option_delta(strike_price, expiry_in_years, risk_free_rate, volatility, notional_amount, spot_price, option_type='put')
# print(f"Put option delta: {put_delta}")

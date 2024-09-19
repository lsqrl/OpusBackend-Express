import math
from scipy.stats import norm

def option_theta(strike, expiry, rate, volatility, notional, spot, option_type):
    """
    Calculate the theta of a European option using the Black-Scholes formula.
    
    Parameters:
    strike (float): Strike price of the option.
    expiry (float): Time to expiry in years.
    rate (float): Risk-free interest rate (annualized).
    volatility (float): Volatility of the underlying asset (annualized).
    notional (float): Notional amount of the option.
    spot (float): Spot price of the underlying asset.
    option_type (str): Type of the option ('CALL' or 'PUT').
    
    Returns:
    float: Theta of the option.
    """
    d1 = (math.log(spot / strike) + (rate + 0.5 * volatility ** 2) * expiry) / (volatility * math.sqrt(expiry))
    d2 = d1 - volatility * math.sqrt(expiry)
    
    # Common term
    term1 = -(spot * norm.pdf(d1) * volatility) / (2 * math.sqrt(expiry))
    
    # Theta calculation for CALL and PUT
    if option_type == 'CALL':
        term2 = rate * strike * math.exp(-rate * expiry) * norm.cdf(d2)
        theta = (term1 - term2) * notional
    elif option_type == 'PUT':
        term2 = rate * strike * math.exp(-rate * expiry) * norm.cdf(-d2)
        theta = (term1 + term2) * notional
    else:
        raise ValueError("Invalid option type. Use 'CALL' or 'PUT'.")
    
    return theta

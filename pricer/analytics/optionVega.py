import math
from scipy.stats import norm

def option_vega(strike, expiry, rate, volatility, notional, spot, option_type):
    """
    Calculate the vega of a European option using the Black-Scholes formula.
    
    Parameters:
    strike (float): Strike price of the option.
    expiry (float): Time to expiry in years.
    rate (float): Risk-free interest rate (annualized).
    volatility (float): Volatility of the underlying asset (annualized).
    notional (float): Notional amount of the option.
    spot (float): Spot price of the underlying asset.
    option_type (str): Type of the option ('CALL' or 'PUT').
    
    Returns:
    float: Vega of the option.
    """
    d1 = (math.log(spot / strike) + (rate + 0.5 * volatility ** 2) * expiry) / (volatility * math.sqrt(expiry))
    
    # Vega calculation
    vega = spot * norm.pdf(d1) * math.sqrt(expiry) * notional / 100
    
    return vega

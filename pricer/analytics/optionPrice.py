import math
from scipy.stats import norm
from scipy.optimize import brentq

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
    option_type (str): Type of the option ('CALL' or 'PUT'). Default is 'CALL'.
    
    Returns:
    float: Price of the option.
    """
    
    # Calculate d1 and d2
    d1 = (math.log(spot / strike) + (rate + 0.5 * volatility ** 2) * expiry) / (volatility * math.sqrt(expiry))
    d2 = d1 - volatility * math.sqrt(expiry)
    
    if option_type == 'CALL':
        price = (spot * norm.cdf(d1) - strike * math.exp(-rate * expiry) * norm.cdf(d2)) * notional
    elif option_type == 'PUT':
        price = (strike * math.exp(-rate * expiry) * norm.cdf(-d2) - spot * norm.cdf(-d1)) * notional
    else:
        raise ValueError("Invalid option type. Use 'CALL' or 'PUT'.")
    
    return price

def implied_volatility(price, strike, expiry, rate, notional, spot, option_type, tol=1e-6):
    """
    Calculate the implied volatility for a European option using the Black-Scholes formula.
    
    Parameters:
    price (float): Observed market price of the option.
    strike (float): Strike price of the option.
    expiry (float): Time to expiry in years.
    rate (float): Risk-free interest rate (annualized).
    notional (float): Notional amount of the option.
    spot (float): Spot price of the underlying asset.
    option_type (str): Type of the option ('CALL' or 'PUT').
    tol (float): Tolerance level for the numerical method (default is 1e-6).
    
    Returns:
    float: Implied volatility of the option.
    """
    
    # Define a function that calculates the difference between observed price and model price
    def price_diff(volatility):
        return option_price(strike, expiry, rate, volatility, notional, spot, option_type) - price

    # Use the Brent method to find the root of the price difference function
    # The volatility must be between 0 and 500% (5.0 in decimal form)
    implied_vol = brentq(price_diff, 1e-6, 5.0, xtol=tol)

    return implied_vol
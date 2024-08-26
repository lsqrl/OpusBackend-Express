import math
from scipy.stats import norm

def black_scholes_delta(S, K, T, r, sigma, option_type="call"):
    """
    Calculate the delta of an option using the Black-Scholes formula.

    Parameters:
    S : float
        Current stock price
    K : float
        Option strike price
    T : float
        Time to maturity (in years)
    r : float
        Risk-free interest rate (annual)
    sigma : float
        Volatility of the underlying asset (annual)
    option_type : str
        "call" for call option, "put" for put option

    Returns:
    delta : float
        Delta of the option
    """
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    
    if option_type == "call":
        delta = norm.cdf(d1)
    elif option_type == "put":
        delta = norm.cdf(d1) - 1
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")
    
    return delta

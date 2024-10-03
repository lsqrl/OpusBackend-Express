from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
import os

url = URL.create(    
    drivername="postgresql",      
    username=os.getenv("POSTGRES_USERNAME"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="localhost",
    port=5432,
    database="postgres"
)
engine = create_engine(url)
connection = engine.connect()

def get_portfolio_details(name):
    # Query the PostgreSQL table
    query = """SELECT t.timestamp as timestamp, p.name as portfolio_name, i.name as instrument_name FROM trades.portfolios p
    JOIN trades.trades_to_portfolios ttp
    ON ttp.portfolio_id = p.id
    JOIN trades.trades t
    ON ttp.trade_id = t.id
    JOIN trades.instruments i
    ON i.id = t.instrument_id
    WHERE p.name = (:param_name)"""
    df = connection.execute(text(query), {"param_name": name})    
    return df

def get_portfolio_list():
    query = """SELECT name from trades.portfolios"""
    df = connection.execute(text(query)) 
    return df

def get_trade_type():
    query = """SELECT name from trades.instruments"""
    df = connection.execute(text(query)) 
    return df
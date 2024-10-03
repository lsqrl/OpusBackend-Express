from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
import pandas as pd
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
    query = f"""SELECT t.timestamp as timestamp, p.name as portfolio_name, t.id as trade_id, i.name as instrument_name FROM trades.portfolios p
    JOIN trades.trades_to_portfolios ttp
    ON ttp.portfolio_id = p.id
    JOIN trades.trades t
    ON ttp.trade_id = t.id
    JOIN trades.instruments i
    ON i.id = t.instrument_id
    WHERE p.name = '{name}'"""  
    df = pd.read_sql_query(query, engine)
    return df

def get_trade_detail(trade_ids, table_name):
    # we want to understand the details of all the trades
    if table_name == "FXOption":
        table_name = "fx_options"
    elif table_name == "FXSpot":
        table_name = "fx_spot"
    elif table_name == "FiatFunding":
        table_name = "fiat_funding"
    query = f"""SELECT * FROM trades.{table_name} WHERE trade_id IN ({",".join(trade_ids)})"""
    df = pd.read_sql_query(query, engine)
    return df

def get_portfolio_list():
    query = """SELECT name from trades.portfolios"""
    df = connection.execute(text(query)) 
    return df

def get_trade_type():
    query = """SELECT name from trades.instruments"""
    df = connection.execute(text(query)) 
    return df
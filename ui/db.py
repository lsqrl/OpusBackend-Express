from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os

url = URL.create(    
    drivername="postgresql",      
    username=os.getenv("POSTGRES_USERNAME"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_NETWORK"),
    port=5432,
    database=os.getenv("POSTGRES_DATABASE")
)
engine = create_engine(url)
connection = engine.connect()

def map_class_to_table(class_name):
    if class_name == "FXOption":
        table_name = "fx_options"
    elif class_name == "FXSpot":
        table_name = "fx_spot"
    elif class_name == "FiatFunding":
        table_name = "fiat_funding"
    return table_name

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
    table_name = map_class_to_table(table_name)
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

def get_table_details(table_name):
    table_name = map_class_to_table(table_name)
    schema_name = 'trades'
    
    query = f"""SELECT 
    cols.column_name, 
    cols.data_type, 
    cons.constraint_type
    FROM 
        information_schema.columns AS cols
    LEFT JOIN (
        SELECT 
            tc.constraint_type,
            kcu.column_name 
        FROM 
            information_schema.table_constraints AS tc 
        JOIN 
            information_schema.key_column_usage AS kcu 
        ON 
            tc.constraint_name = kcu.constraint_name 
            AND tc.table_name = kcu.table_name
        WHERE 
            tc.table_name = '{table_name}'
        AND 
            tc.table_schema = '{schema_name}'
    ) AS cons
    ON 
        cols.column_name = cons.column_name
    WHERE 
        cols.table_name = '{table_name}'
    AND 
        cols.table_schema = '{schema_name}';

    """
    #-- cols.is_nullable, 
    #-- cols.character_maximum_length,
    #-- cols.column_default,
    df = connection.execute(text(query)) 
    return df
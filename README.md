# OpusBackend-Express
Opus Express backend, lightweight to run on a remote server

# Setup
Before running the server, make sure that you have created an .env file

Add the database parameters:
1. POSTGRES_USERNAME
2. POSTGRES_PASSWORD
3. POSTGRES_NETWORK
4. POSTGRES_DATABASE

Also make sure to set up the BASE_URL namely:
1. BASE_URL = "0.0.0.0" for remote deployment
2. BASE_URL = "127.0.0.1" for on-prem deployment

## Requirements
Set up a virtual environment:
```
pip install --user virtualenv
virtualenv venv
.\venv\Scripts\activate
```
Make sure to install all the python requirements:
```
pip install --user -r requirements.txt
```

# Run
First make sure to run the most recent version of the database:
```
python database_prod/initialize_database.py
```
In two separate terminals run:
```
python ./startServers.py
```
and
```
streamlit run ./ui/app.py
```
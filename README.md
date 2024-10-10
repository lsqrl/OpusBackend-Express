# OpusBackend-Express
Opus Express backend, lightweight to run on a remote server

# Setup
Before running the server, make sure that you have exported:
1. POSTGRES_USERNAME
2. POSTGRES_PASSWORD

These variables have to be set up in:
1. ui/db.py
2. database_prod/initialize_database.py

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
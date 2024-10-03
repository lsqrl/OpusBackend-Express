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

## Notes for pygraphviz and erdantic installations on Windows

On Windows 10, pip 24.1 and python 3.12. It took me these steps to complete the installation.

Download and install Graphviz: https://graphviz.org/download/

Then run the following command:pi
```
python -m pip install --config-settings="--global-option=build_ext" --config-settings="--global-option=-IC:\Program Files\Graphviz\include" --config-settings="--global-option=-LC:\Program Files\Graphviz\lib" pygraphviz
```
# Database
An SQL database that supports the Opus system.

This version of the database has been designed at the end of July 2024.

In order to be able to run this, please make sure to install PostgresDB, run it and insert the appropriate username and password.

Since the code is written in python, please install the requirements:
```
pip install -r requirements.txt
```

## How to build the data model and generate corresponding data
Look at your system's diagram. Describe the system users and make a list of their possible actions.
Once the actions are in place, identify the entities that are needed to support these users and their actions.

Don't forget to identify the system's needs as well.

Once the Data model is designed, generate different scenarios you would like to showcase.
There will be 3 types of data:
1. static data - always the same (example: list of currencies, countries in the world etc.)
2. data that comes from an API - timeseries data
3. data that gets generated by the actions of the system and its users (initially fake, later real)

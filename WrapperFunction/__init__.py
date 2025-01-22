import azure.functions as func

#import fastapi
#
#app = fastapi.FastAPI()
#
#@app.get("/sample")
#async def index():
#    return {
#        "info": "Try /hello/Shivani for parameterized route.",
#    }
#
#
#@app.get("/hello/{name}")
#async def get_name(name: str):
#    return {
#        "name": name,
#    }
from fastapi import FastAPI, Query
import snowflake.connector as sf
import os

# Use environment variables for sensitive data
username = os.getenv('SNOWFLAKE_USER', 'DEV_FINOPS_PYTH_USR')
password = os.getenv('SNOWFLAKE_PASSWORD', '22YjDChTVX9s')
account = os.getenv('SNOWFLAKE_ACCOUNT', 'vcg_dm.west-europe.azure')
warehouse = os.getenv('SNOWFLAKE_WAREHOUSE', 'DEV_CIC_ETL_WHS')
database = os.getenv('SNOWFLAKE_DATABASE', 'DEV_CIC_DB')

# Initialize FastAPI app
app = FastAPI()

# Establish a connection to Snowflake
ctx = sf.connect(
    user=username,
    password=password,
    account=account,
    warehouse=warehouse,
    database=database,
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Finops Data application!"}

@app.get('/fetchdata')
async def fetchdata():
    try:
        with ctx.cursor() as cursor:
            # Execute query
            cursor.execute("SELECT 1")
            # Fetch results
            results = cursor.fetchall()
            # Return the results as a JSON response
            return {"data": results}
    except Exception as e:
        return {"error": str(e)}
    

@app.get("/getappid")
async def fetchdata(application_id: str = Query(..., description="Dummy application ID")):
    """
    Fetches data based on the provided application ID.
    """
    try:
        with ctx.cursor() as cursor:
            # Query using the dummy application ID
            cursor.execute(f"SELECT 'app id {application_id} found' AS result")
            # Fetch the result
            result = cursor.fetchone()
            return {"data": result[0]}  # Return the first column of the result
    except Exception as e:
        return {"error": str(e)}

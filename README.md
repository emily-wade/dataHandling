# dataHandling
This repo is for data handling techniques used within SDP.

## Contents:
- dataHandlingFunctions.py - contains all functions that can be used for all aspects of data handling.
- flattenJson.py - contains functions to be used for flattening JSON data. Adapted from flatten-json Python package to make fit for purpose.
- requirements.txt - all packages/modules required to run functions in dataHandlingFunctions.py file.
- exampleRawData.txt - example of raw data from Gecko that can be used to test functions.
- Braze-Push-Notifications.txt - example of source sample data that can be used to test functions.


## Possible tasks:
#### Raw data from Gecko -> Python DataFrame
- Purpose: to perform initial data analysis once data has landed in raw.
- Data in Gecko is not readable JSON - using `jsonFormatter()` will make this readable.
- Using `createDataframe()` will then convert this to a Python Dataframe to be used in initial analysis.
- For those not familiar with data analysis using Python, I'd recommend taking a look at the Pandas package. [This article](https://www.analyticsvidhya.com/blog/2021/05/a-comprehensive-guide-to-data-analysis-using-pandas-hands-on-data-analysis-on-imdb-movies-data/) by Analytics Vidhya has some handy starting points.

#### Source sample data -> Tech Spec
- Purpose: to create a draft tech spec in Excel.
- Sample data is (as far as I'm aware) always in JSON format - using `createTechSpec()` will flatten the data, create a dataframe, store the source field names and then add target field names (by converting to camelCase where necessary) and identify source data types.
- This is then exported to Excel, ready to be checked and completed by the analyst.

## Setup:
You will need to install python, pip and virtualenv if not already done: 
1. Install Python: https://www.python.org/downloads/
2. Install pip: Python3 usually comes with pip pre-installed but if `pip list` throws the error "pip command not found" then download get-pip.py from https://bootstrap.pypa.io/get-pip.py. Open cmd, navigate to the folder you downloaded the .py file to, and run `python3 get-pip.py`
3. Continue with the steps below

If you have python installed: 
1. Clone this repo and navigate to it in cmd
2. Install requirements.txt: run `pip install -r requirements.txt`
3. You should now to be able to run the .py scripts in this repo. There are 2 ways to do this:  
    a. Inside the dataHandlingFunctions.py you can run the entire script then at the bottom call the functions you wish to use  
    b. Create a separate python file inside the same folder and run `from dataHandlingFunctions import <functionName>` to import the function you wish to use. Then you can call the functions in this file. 

## Examples:
```
# Example: Raw data from Gecko -> Python DataFrame
jsonData = geckoToJsonFormatter("exampleRawData.txt")
df = createDataframe(jsonData)
print(df)
```

```
# Example: Source sample data -> Tech Spec
filePathFrom = "Braze-Push-Notifications.txt"
filePathTo = "BrazePushNotifications-TechSpec.xlsx"
techSpec = createTechSpec(filePathFrom, filePathTo)
print(techSpec)
```

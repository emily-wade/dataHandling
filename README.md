# dataHandling
This repo is for data handling techniques used within SDP.

## Contents:
- dataHandlingFunctions.py - contains all functions that can be used for all aspects of data handling.
- flattenJson.py - contains functions to be used for flattening JSON data. Adapted from flatten-json Python package to make fit for purpose.
- requirements.txt - all packages/modules required to run functions in dataHandlingFunctions.py file.

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

## Usage:
<i>WIP</i>

## Examples:
<i>WIP</i>




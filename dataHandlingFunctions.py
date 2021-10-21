#!/usr/bin/env python
# coding: utf-8

# In[1]:


# imports
import json
import pandas as pd
from collections import defaultdict
import re
from inflection import camelize
from flattenJson import flatten


# In[2]:


def geckoToJsonFormatter(filePath):
    """
    Purpose: converts raw data outputted from Gecko into array of JSON messages 
             raw data is not JSON readable and requires delimiters between messages before analysis
    Inputs: filePath (path to Gecko raw data output)
    Outputs: jsonData (array of JSON messages split by ",")
    """
    # read in data from raw
    with open(filePath, "r") as f:
        content = f.read()

    # create array to append json objects to from raw data
    jsonData = []

    # initialise decoder
    decoder = json.JSONDecoder()

    # loop to append each json object to array
    while content:
        obj, idx = decoder.raw_decode(content)
        content = content[idx:].strip()
        jsonData.append(obj)
        
    # return array of json objects
    return jsonData


# In[8]:


def jsonFlattener(filePath):
    """
    Purpose: reads and flattens JSON data (sample or production data from source team)
    Inputs: filePath (path to sample/prod data)
    Outputs: jsonFlattened (list of dictionaries, each dict represents one JSON message,
                            keys are period-separated field names, values are values)
    """
    # read in data
    with open(filePath, "r") as f:
        content = f.read()
        data = json.loads('[{}]'.format(content))
        
    # flatten using adapted version of flatten-json package
    jsonFlattened = [flatten(d) for d in data]

    # return array of json objects
    return jsonFlattened


# In[4]:


def createDataframe(jsonData):
    """
    Purpose: create DataFrame to perform intial analysis and data profiling as part of Milestone 1.
    Inputs: jsonData (output from previous function)
    Outputs: df (DataFrame with column headers as keys and each row representing 1 message from Gecko output)
    """
    # initialise defaultdict (req to convert multiple dictionaries into a single dictionary)
    # eg converts 
    #    d1 = {key1: x1, key2: y1}  
    #    d2 = {key1: x2, key2: y2} 
    # into
    #    d = {key1: (x1, x2), key2: (y1, y2)}

    dd = defaultdict(list)

    # create array to append one dictionary per message to
    data = []
    # appends k:v pairs from __data, __sdpMetadata and __includesSdpMetadata blocks to data
    for i in jsonData:
        
        d = {}
        for k, v in i.items():
            d[k] = v
        data.append(d)

    # convert array containing multiple dictionaries to list
    for d in tuple(data):
        for k, v in d.items():
            dd[k].append(v)

    # create dataframe from list of k:v pairs for all messages
    # 1 row per message
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k,v in dd.items()]))
    
    return df


# In[5]:


def getFieldNames(df):
    """
    Purpose: create 2 lists of field names, one for source field names and one for target field names
    Inputs: fieldNames (list of field names with parent field names removed outputted from getFieldNames function)
    Outputs: sourceFieldNames (list of field names, flattened df columns)
             targetFieldNames (list of field names converted to camelCase)
    """
    # source field names are just dataframe columns
    sourceFieldNames = df.columns
    
    # create list of fields to create target field names from
    # split on delimiter and remove parent field names
    fieldNames = [col.split('.')[-1] for col in list(df.columns)]
    
    # empty list to add transformed field names to
    targetFieldNames = []
    
    # for every field in the list
    for field in fieldNames:
        # check if first part is uppercase
        # when splitting on delimiter
        if re.split(' ; |_|, |\*|\n', field)[0].isupper():
            # then convert first part to lowercase and keep the rest the same 
            targetFieldNames.append(re.split(' ; |_|, |\*|\n', field)[0].lower() + ' '.join(re.split(' ; |_|, |\*|\n', field)[1:]))
        # when splitting on ' ' 
        elif field.split()[0].isupper():
            # then convert first part to lowercase and keep the rest the same
            # and append to list
            targetFieldNames.append(field.split()[0].lower() + ' '.join(field.split()[1:]))
        else:
            # append to list as is
            targetFieldNames.append(field)
            
    # use camelize lib to convert targetFieldNames to camelCase
    # additionally remove spaces as camelize package doesn't do this
    targetFieldNames = [camelize(field, False).replace(' ', '') for field in targetFieldNames]
    
    # return list of target field names
    return sourceFieldNames, targetFieldNames

# this does not cater for fieldNames that have no delimiter and are all lower case
# this will of course need to be checked manually by analyst


# In[11]:


def createTechSpec(filePathFrom, filePathTo):
    """
    Purpose: create tech spec with columns Source Field Name, Target Field Name, Source Data Type
    Inputs: df (dataframe created as output in createDataframe function) 
    Outputs: techSpec (dataframe created with columns matching tech spec)
    """
    jsonFlattened = jsonFlattener(filePathFrom)
    df = createDataframe(jsonFlattened)
    sourceFieldNames, targetFieldNames = getFieldNames(df)
    
    # get python data types from dataframe
    dataTypes = df.dtypes
    
    # create tech spec dataframe
    techSpec = pd.DataFrame(list(zip(df.columns, targetFieldNames, dataTypes)),
                        columns=['Source Field Name', 'Target Field Name', 'Source Data Type'])
    
    # change python data types to json data types
    techSpec["Source Data Type"].replace({"object": "STRING", "int64": "NUMERIC", "bool": "BOOLEAN"}, inplace=True)
    
    # export to Excel
    techSpec.to_excel(filePathTo, index=False)
    
    return techSpec


# In[13]:


# TO RUN: EXAMPLE
# SAMPLE DATA TO TECH SPEC IN EXCEL (1 ROW PER JSON MSG)
filePathFrom = r"C:\Users\EWD05\OneDrive - Sky\Documents\Tickets\Braze Push Notifications\Braze-Push-Notifications.txt"
filePathTo = 'BrazePushNotifications-TechSpec.xlsx'
techSpec = createTechSpec(filePathFrom, filePathTo)
techSpec


# In[ ]:


# TO RUN: EXAMPLE
# GECKO RAW TO DATAFRAME READY FOR INITIAL DATA PROFILING (1 ROW PER JSON MSG)
jsonData = geckoToJsonFormatter("exampleRawData.txt")
df = createDataframe(jsonData)
df


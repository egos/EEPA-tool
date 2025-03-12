# CRW_trigger

The CRW ERF Tool (referred to as 'The Tool') has been developed by the World Bank to assist CRW ERF calculation partners in performing trigger calculations and identifying countries that may be eligible for CRW ERF funding.
This application is in python , numpy , pandas,  the interface has been developed with the python [streamlit library](https://streamlit.io/). 

notes dev : PivotCountry , Output_Main_Prep, Output_Main sur l'importance du formalisme des chiffres dans les rapports 

# Table of contents
1. [Installation](#Installation)
1. [detailed installation](#detailed-installation)
1. [use the code locally](#use-the-code-locally)
1. [Tools Structuration](#Tools-Structuration)
    1. [application sections](#application-sections)
    1. [Datasets](#Datasets)
    1. [word documents export](#word-documents-export)


# Installation
To launch the application locally you must have installed the following libraries list. Please have a look at their documentation to get them installed. For ease of installation i recommend using [anaconda distribution](https://www.anaconda.com/products/distribution).
- Python 3 (via anaconda)
- Pandas (via anaconda)
- Numpy (via anaconda)
- Jupyter notebook (via anaconda)

dependencies 
- plotly
- pickles
- openpyxl
- XlsxWriter
- Streamlit

for install all dependencies after conda installation use command:
```pip install -r requirements_local.txt```

# detailed installation
in case of non-develloppers

1. install anaconda [anaconda distribution](https://www.anaconda.com/products/distribution).
2. in anaconda navigator launch VScode (visual studio code)
3. in VScode open AY folder
4. dependecy installation :
   1. open command prompt terminal in vscode wait env activation
   2. type in the terminal (each time wait for the end of installation):  ``pip install -r requirements_local.txt`` 
5. launch application , in the terminal type  ``streamlit run main.py``

# use the code locally 
To use the code locally and if jupyter is installed you can use the [AYtools_Notebook.ipynb](AYtools_Notebook.ipynb) which imports the functions from [utils.py](utils.py).
To launch the application locally, type the command line in the current directory ```streamlit run main.Py```, the app will launch in your default web browser. 

# Tools Structuration
streamlit is a framework that allows you to easily design an application in python. The code is structured in top down and follows the order of the application sections of the calculations and are carried out by section then the display of the results.

![screenshot](assets\diagramme_code_CRW_ERF_trigger_tool.jpg)

## update input data
replace input in default_data folder , respect the neame of each file
- -01. Input_Parameters.csv
- -02n. Input_Data.csv
- -03. Lookup_IDAyear.csv
- -04. Lookup_InArrear_v2.csv

## application sections :
The structure of the code of [main.py](main.py) follow the breakdown of the application sections : 
- 1 - Disclaimer and user guide section
- 2a - Input - Parameters 
- 2b - Input - FEWS IPC data
- 2c - Input - IDA year reference table
- 2d - Input - In Arrear Country reference table
- 3 - Additional information for map
- 4 - Output - CRW ERF trigger results
- 5 - Output - CRW ERF trigger report
- 6 - Output - Subnational Food Security Report

## Datasets :
All needed dataset and values are stored in the dictionnary "data" who contained the detailed information by categories : 
- input data
    - Input_Parameters
    - Input_data
    - Lookup_IDAyear
    - Lookup_InArrear
- uploaded_file : current input data via st.file_uploader , default data set are in the folder [default_input](default_input)
- PivotCountry : result dataframe of main calulation (return from Calculation func)
- Input_data2 : input data modified after main calulation
- Country : list of countries 
- Not_IDA : list of not IDA countries
- MaxCalYear : last years of data
- Conf_format : dictionnary to format with filter the result table in section 4 - Output - CRW ERF trigger results
- Output_Main_Prep : 
- Output_Main :
- WordCalculation : 

## repository content:
- [assets](assets) - the images and text used in the app
- [outputs](outputs) - in case of running tools in local mode , folder for store results
- [CRW_Notebook.ipynb](CRW_Notebook.ipynb) - a notebook that allows you to run locally all the calculations steps from [application sections](#application-sections) 
- [main.py](main.py) - streamlit & interface part
- [utils.py](utils.py) - containes all function used by main.py and CRW_Notebook.ipynb
- [default dataset](default_input) - the default dataset loading by the program , which also been used as a template for the user and can bve downloaded


# word documents export

the word export section uses the export pattern word.docx file to serve as a text base, passages with {} are automatically updated with the values ​​calculated by the tool


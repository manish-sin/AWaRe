# Objective of this Files
# In file we will write code to generate report form the log of AWaRe The Report will have two charts
# CHART1 : A Pie chart shoing major Softwares used such as Google Chrome
# CHART2 :When we click on any section of Pie Chart(Any application), an bar-chart opens contain files names on any application
# As we create Chart we will improvise based on Char.js capablity. There will be multiple charts,


# Step 1: Data Filtering
# Convert all "NaN" in -window- level to "Ideal" ------------ Done
# Delete First Entry ------------- Done
# #(Optional)Substract consequtive entries in -Time Stamp- find duration and make a fresh coulum -duration-

# Importing Necessary Library
import pandas as pd
import numpy as np
from datetime import date
import datetime

import socketio
from flask import Flask, render_template, jsonify, url_for
from flask_socketio import SocketIO, send, emit
today = date.today()
date = "2020-05-20"



def get_date_specific_log(date):

    # Import the csv generated using the aware utility and converting the time string into date time format
    df = pd.read_csv("awl.csv", index_col='Unnamed: 0') #C:/Users/manis/Desktop/

    # drop the first row which is used as a marker and to find the time difference between application
    df = df.drop(0)
    df = df.reset_index(drop=True)
    # Fill all the empty cell with Ideal value
    df.fillna('Ideal', inplace=True)


    # Step 2: CHART 1
    # Create a datafrme which cab be used to plot chart, in same way way as we do in excel. Alternative suggesion are welcome
    # Convert Datasheet into list

    # Filter out the Application name from the window and place them in new window
    # step 1: split the window name to extract application name i.1. the last string after a  "-"
    # Step 2: store the application name in the newly created Column -Application-

    df["Application"] = 0  # new column created
    index = 0
    for window in df["Window"]:
        app = window.split("-")  # Step 1
        app = app[-1]
        df.loc[index, "Application"] = app  # step2
        index = index + 1
    max_date = df['Time Stamp'][0][:10]
    min_date = df['Time Stamp'][df.last_valid_index()][:10]
    df = df[df['Time Stamp'].map(lambda x: date in x)]

    df_date = df
    return df_date, max_date, min_date

# IMPROVEMENT
# 1. Avoid Use of For Loop
# Create Pivot table which will be  to Graph
# All the application which has been used below say 30 sec will be clubed as Miscleneous application and drop all such rows
# We will also create a list of app "misc_apps", which we are going to drop anyway from the dataframe  so that we can use them for chart 2.
# make a new entry as "misc" in the dataframe and duration will be sum of all these app
# Convert the dataframe into list

def chart_of_apps(df):

    # Declearing a list which will be sent to chart.js
    chart_list1 = []

    # Step1: Pivot table
    app_chart1 = pd.pivot_table(df, values="Suration", index=["Application"], aggfunc=np.sum).reset_index()
    print(app_chart1)
    # Threshold duration to conside if an app needs to be put in mislaneous category
    thrashold = 30
    # basic declearation for dataframe manupulation
    low_threshold = 2
    misc = 0
    index = 0
    misc_apps = []  # declearling enpty list to store apps which will be placed in mislaneous category
    print(app_chart1)
    for item in app_chart1["Suration"]:
        if (item < thrashold):  # Step 2: operation to be done for each row which are leaa than threshold
            if (item > low_threshold):
                misc = misc + item  # cumulative time of each app
                misc_app = app_chart1["Application"][index]  # getting the name of sub-application to store in "misc_apps"
                misc_apps.append(misc_app)  # step4: creating list misc_apps
            app_chart1.drop([index], inplace=True)
        index = index + 1

    misc_entry = ["Miscellaneous", misc]

    # Step 4: making entry of misc app in the dataframe
    if (misc > 0):
        app_chart1.loc[len(app_chart1)] = misc_entry
    app_chart1 = app_chart1.reset_index(drop=True)
    app_chart1["SlNo"] = range(len(app_chart1))
    # step 5 convert data frme to list
    chart_list1.append(app_chart1.Application.tolist())
    app_chart1["Duration"] = (app_chart1.Suration / 60).astype('int32')
    chart_list1.append(app_chart1["Duration"].tolist())
    chart_list1.append(len(app_chart1))
    #print(chart_list1)
    return chart_list1, misc_apps
    # print(app_chart1)

# Step 3: CHART 2
# Create a datafrme for each section of Pie-chart which cab be used to plot chart, in same way way as we do in excel.
# Note Every item will be poltted. Alternative suggesion are welcome
# Convert Datasheet into list
# Chart 2 will have as many sub charts as there are Applications with Different Name,
# so we create as many dataframe Method to do so will be to
# Make as many Data frame as there are application category

# Steps to make char
# We First make a pivot table to get relevant dataframe for the chart
# relevent dataframe = here we make a table which contains total dutation againste each sub-application
# However we will add application name against each sub-application for purpose of manupulating dataframe to get Sub-charts
# Then We convert Dataframe into list, such that each data can be easily acesses by Chart.Js

# Note1: by "application" or "apps" we refer to category of window usch as "Google Chrome" or "Excel"
# Note2: by "sub-application" or sub-apps: we refer to file name under each window
def chart_of_subapps(df,misc_apps, app_name):
    # Step 1: Catagorise app with small duration into a "misc" app category
    index = 0
    for app in df["Application"]:
        if (app in misc_apps):  # misc_apps is list of application/windows which were used for less than threshold time
            df.loc[index, "Application"] = "Miscellaneous"  # in the  -Application- Column we replce values with "misc" to catagorise
    
        index = index + 1
    # Step 2: Create a pivot table
    app_chart2 = pd.pivot_table(df, values="Suration", index=["Window"],
                                aggfunc=np.sum).reset_index()  # , columns=["Application"]
    #print(app_chart2)
    # Step 3: Add another column having application name, do se we will use a dictionaly to map sub-apps to app
    df_dict = dict(zip(df.Window, df.Application))
    app_chart2['apps'] = app_chart2['Window'].map(df_dict)  # "app_chart2" is the required dataframe
    #print(app_chart2)
    # Step 4: Convert Datafrme to list and Sublist "chart2_list"
    app_list = app_chart2.apps.unique()  # it is list of apps
    # chart2_list = app_list.tolist()
    # chart_list.append(chart2_list)
    num_of_apps = [len(app_list)]  # total no. of apps
    
    
    # chart_list.append(num_of_apps)
    # print(app_chart2)
    # for app in app_list: #here we extact sub-apps list and cumulative duration for each sub-apps for each

    chart_list2 = []
    #print(app_name)
    app_wise_df = app_chart2[app_chart2["apps"] == app_name]
    #print("whats this", app_wise_df)
    app_wise_df = app_wise_df.sort_values("Suration", axis=0, ascending=False, na_position='last').reset_index(
        drop=True)
    app_wise_df = app_wise_df[app_wise_df["Suration"] > 2]
    #print(app_wise_df)
    #print(app_wise_df.Window)

    app_wise_df["Duration"] = (app_wise_df["Suration"] / 60).astype('int32')
    #app_wise_df = app_wise_df[app_wise_df["Duration"] > 0]
    sub_list_window = app_wise_df.Window.tolist()
    #print(sub_list_window)
    chart_list2.append(sub_list_window)
    sub_list_duration = app_wise_df["Duration"].tolist()
    chart_list2.append(sub_list_duration)
    chart_list2.append(app_name)
    #chart_list2.append(len(sub_list_window))
    # today = str(date.today())
    # print(type(today))
    # print(today)


    # send "chart2_list" to Chart.js
    print(chart_list2)
    return chart_list2


# send "chart2_list" to Chart.js
def get_chart_data(data, df_date, max_date, min_date ):
    print(data)
    chart_list = []
    if data.get("y") is None:
        app_name = data.get("label")
        #print("getting data of sub app", app_name)
        chart_list1, misc_apps = chart_of_apps(df_date)
        #print("step 1 completed")
        chart_list2 = chart_of_subapps(df_date, misc_apps, app_name)
        #print("step 2 completed")
        chart_list.append(chart_list1)
        #print("step 3 completed")
        chart_list.append(chart_list2)
        #print("step 4 completed")
        chart_list.append(max_date)
        chart_list.append(min_date)

        chart_list.append("2020-05-20")
    else:
        year = data.get("y")

        #print("getting data of", year)
        df_date, max_date, min_date = get_date_specific_log(year)
        #print(df_date)
        app_name = "Miscellaneous"
        #print("Go/Home Button:",year, app_name)
        chart_list1, misc_apps = chart_of_apps(df_date)
        #print("step 1 completed")
        chart_list2 = chart_of_subapps(df_date, misc_apps, app_name)
        #print("step 2 completed")
        chart_list.append(chart_list1)
        #print("step 3 completed",chart_list1)
        chart_list.append(chart_list2)
        #print("step 4 completed",chart_list2)

        chart_list.append(max_date)
        chart_list.append(min_date)
        chart_list.append(year)
        #print(chart_list)
    return chart_list

# Define an flask server app
#print(get_chart_data(3))

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('Awarness.html')


# set a socket to send message
@socketio.on('message')
def message(data):
    print(f"{data}")

    app_name = "Miscellaneous"#llaneous"
    chart_list = []
    df_date, max_date, min_date = get_date_specific_log(date)
    chart_list1, misc_apps = chart_of_apps(df_date)
    chart_list2 = chart_of_subapps(df_date, misc_apps, app_name)
    chart_list.append(chart_list1)
    chart_list.append(chart_list2)
    chart_list.append(max_date)
    chart_list.append(min_date)
    chart_list.append(date)
    data = chart_list
    print(data)
    send(data, broadcast=True)


@app.route('/detail')
def detail():
    return render_template('Awarness_detail.html')


@socketio.on('msg')
def message(data):
    print(data)
    df_date_wise, max_date, min_date  = get_date_specific_log(date)

    data = get_chart_data(data, df_date_wise, max_date, min_date )
    print(data)

    emit('message', data)


if __name__ == '__main__':
    app.run(debug=True)

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
import datetime

import socketio
from flask import Flask, render_template, jsonify, url_for
from flask_socketio import SocketIO, send, emit

# Import the csv generated using the aware utility and converting the time string into date time format
df = pd.read_csv("awl.csv", index_col='Unnamed: 0')
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
df.head(50)

# IMPROVEMENT
# 1. Avoid Use of For Loop
# Create Pivot table which will be  to Graph
# All the application which has been used below say 30 sec will be clubed as Miscleneous application and drop all such rows
# We will also create a list of app "misc_apps", which we are going to drop anyway from the dataframe  so that we can use them for chart 2.
# make a new entry as "misc" in the dataframe and duration will be sum of all these app
# Convert the dataframe into list


# Declearing a list which will be sent to chart.js
chart_list1 = []

# Step1: Pivot table
app_chart1 = pd.pivot_table(df, values="Suration", index=["Application"], aggfunc=np.sum).reset_index()
# Threshold duration to conside if an app needs to be put in mislaneous category
thrashold = 30
# basic declearation for dataframe manupulation
low_threshold = 2
misc = 0
index = 0
misc_apps = []  # declearling enpty list to store apps which will be placed in mislaneous category
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
# print(chart_list1)
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

# Step 1: Catagorise app with small duration into a "misc" app category
index = 0
for app in df["Application"]:
    if (app in misc_apps):  # misc_apps is list of application/windows which were used for less than threshold time
        df["Application"][
            index] = "Miscellaneous"  # in the  -Application- Column we replce values with "misc" to catagorise
    index = index + 1
# Step 2: Create a pivot table
app_chart2 = pd.pivot_table(df, values="Suration", index=["Window"],
                            aggfunc=np.sum).reset_index()  # , columns=["Application"]
# Step 3: Add another column having application name, do se we will use a dictionaly to map sub-apps to app
df_dict = dict(zip(df.Window, df.Application))
app_chart2['apps'] = app_chart2['Window'].map(df_dict)  # "app_chart2" is the required dataframe

# Step 4: Convert Datafrme to list and Sublist "chart2_list"
app_list = app_chart2.apps.unique()  # it is list of apps
# chart2_list = app_list.tolist()
# chart_list.append(chart2_list)
num_of_apps = [len(app_list)]  # total no. of apps


# chart_list.append(num_of_apps)
# print(app_chart2)
# for app in app_list: #here we extact sub-apps list and cumulative duration for each sub-apps for each
def chart_of_app(app_name):
    chart_list2 = []
    app_wise_df = app_chart2[app_chart2["apps"] == app_name]
    # print(app_wise_df)
    app_wise_df = app_wise_df.sort_values("Suration", axis=0, ascending=False, na_position='last').reset_index(
        drop=True)
    app_wise_df = app_wise_df[app_wise_df["Suration"] > 2]
    #print(app_wise_df)

    sub_list_window = app_wise_df.Window.tolist()
    chart_list2.append(sub_list_window)
    app_wise_df["Duration"] = (app_wise_df["Suration"] / 60).astype('int32')
    app_wise_df = app_wise_df[app_wise_df["Duration"] > 0]
    sub_list_Duration = app_wise_df["Duration"].tolist()
    chart_list2.append(sub_list_Duration)
    chart_list2.append(app_name)
    chart_list2.append(len(sub_list_window))
    # send "chart2_list" to Chart.js
    # print(chart_list2)
    return chart_list2


# send "chart2_list" to Chart.js
def get_chart_data(app_no):
    chart_list = []
    chart_list2 = chart_of_app(app_no)
    chart_list.append(chart_list1)
    chart_list.append(chart_list2)
    return chart_list


# Define an flask server app
print(get_chart_data(3))

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('Awarness.html')


# set a socket to send message
@socketio.on('message')
def message(data):
    print(f"/n/n{data}/n/n")

    data = get_chart_data(" Google Chrome")
    send(data, broadcast=True)


@app.route('/detail')
def detail():
    return render_template('Awarness_detail.html')


@socketio.on('msg')
def message(data):
    print(data)
    data["label"]
    data = get_chart_data(data["label"])

    emit('message', data)


if __name__ == '__main__':
    app.run(debug=True)

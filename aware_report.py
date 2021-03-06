#take 3 days log,
#Print
# Self-Efficacy influences the choices we make,  the efforts we put forth and how we feel.
# -somewhere on internet

# Keeping this as theme, I and Rahul have wrote a small software Aware. We hoped it would serve as a tool to help us calibrate our self-efficacy. We have been using if for sometime know, and we thought some of you might also find it useful .
#
# Hence we have packaged it and made it available as freeware.  This software logs data from your PC and produces a meaningful report. We have made the source code available so that you are sure that your  data is safe.
#
# You may know more about Aware and Download it from the below github Link. Do let us know for feedback on github (or here). You may also PM us you mail id, we will inform if there is any update in future


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
import time
import random
import threading

import win32gui, pandas as pd
import datetime
import os


import socketio
from flask import Flask, render_template, jsonify, url_for
from flask_socketio import SocketIO, send, emit
from engineio.async_drivers import gevent #do not delet this this is required for packaging

today = str(date.today())

date = today
df_date  = pd.DataFrame()

max_date = "2020-05-25"
min_date = "2020-05-25"
#print("hi")

def log_windows():
    def delete_old_log(df, latest_log):
        # print(df)
        index_list = []
        for i in range(len(df)):
            check_log = datetime.datetime.strptime(df["Time Stamp"][i], '%Y-%m-%d %H:%M:%S.%f').date()
            date_diff = (latest_log - check_log).days
            if (date_diff > 4):
                index_list.append(i)
        df.drop(df.index[index_list], axis=0, inplace=True)
        return df
    print("hello")
    aw = win32gui
    infinity = 0
    TS = datetime.datetime.now()
    AWR = "Dummy"
    i = 0
    duration = 0
    AWRF = "abc"
    if os.path.exists('C:/Aware/awl.csv'):
        awl = pd.read_csv('C:/Aware/awl.csv', index_col="Unnamed: 0")
    else:
        columns = ["Time Stamp", "Window", "Suration"]
        awl = pd.DataFrame(columns=columns)
    #awl = awl[awl['Window'] != 'abc']
    while True:
        time.sleep(1)
        AWR = aw.GetWindowText(aw.GetForegroundWindow())

        while AWR != AWRF:
            # print(i)
            TS_str = str(TS)
            to_append = [TS_str, AWRF, i]
            #print(to_append)
            TS = datetime.datetime.now()
            # print(TS_str)
            i = 0
            AWRF = AWR
            awl_length = len(awl)
            awl.loc[awl_length] = to_append
            awl.to_csv('C:/Aware/awl.csv')


            df = pd.read_csv('C:/Aware/awl.csv', index_col='Unnamed: 0')

            first_log = datetime.datetime.strptime(df["Time Stamp"][0], '%Y-%m-%d %H:%M:%S.%f').date()
            latest_log = datetime.datetime.strptime(df['Time Stamp'][df.last_valid_index()],
                                                    '%Y-%m-%d %H:%M:%S.%f').date()
            date_diff = (latest_log - first_log).days
            #print(df)
            if (date_diff > 4):
                df = delete_old_log(df, latest_log)
                df= df.reset_index(drop=True)
                df.to_csv('C:/Aware/awl.csv')
        i = i + 1

loging = threading.Thread(target=log_windows)
loging.start()




def generate_colors(app_count):
    colors = []
    for color in range(app_count):
        color = "%06x" % random.randint(0, 0xFFFFFF)
        color = "#"+color
        colors.append(color)
    return colors

def get_date_specific_log(date):
    # Import the csv generated using the aware utility and converting the time string into date time format
    df = pd.read_csv('C:/Aware/awl.csv', index_col='Unnamed: 0')  # C:/Users/manis/Desktop/
    print("date_specific lof", df)
    #print("THis is Data", date)
    # drop the first row which is used as a marker and to find the time difference between application

    # Fill all the empty cell with Ideal value

    #print("THis is Data", date)
    # Step 2: CHART 1
    # Create a datafrme which cab be used to plot chart, in same way way as we do in excel. Alternative suggesion are welcome
    # Convert Datasheet into list

    # Filter out the Application name from the window and place them in new window
    # step 1: split the window name to extract application name i.1. the last string after a  "-"
    # Step 2: store the application name in the newly created Column -Application-
    df['Time Stamp'] = df['Time Stamp'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
    dp = pd.DataFrame(df['Time Stamp'].diff())
    dp = dp.drop(0).reset_index(drop=True)

    dp.rename(columns={"Time Stamp": "Duration"}, inplace=True)
    df = df.join(dp)
    df.dropna(subset=["Duration"], inplace=True)
    # df.reset_index(inplace=True)
    df['Duration'] = df['Duration'].apply(lambda x: int(x.seconds))
    df.rename(columns={"Duration": "Suration", "Suration": "Dur"}, inplace=True)
    df['Time Stamp'] = df['Time Stamp'].apply(lambda x: str(x))


    df.fillna('Ideal', inplace=True)
    print(df)



    print(type(df["Time Stamp"][0]))
    df["Application"] = 0  # new column created

    index = 0
    for window in df["Window"]:
        app = window.split("-")  # Step 1
        app = app[-1]
        df.loc[index, "Application"] = app  # step2
        index = index + 1
    print("added application", df)
    mx_date = datetime.datetime.strptime(df["Time Stamp"][0], '%Y-%m-%d %H:%M:%S.%f').date()
    max_date = str(mx_date)

    mn_date = datetime.datetime.strptime(df['Time Stamp'][df.last_valid_index()], '%Y-%m-%d %H:%M:%S.%f').date()
    min_date = str(mn_date)

    df = df[df['Time Stamp'].map(lambda x: date in x)]
    print("final",df)
    df_date = df
    # print(df_date)
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
    print("App Function", app_chart1)
    # Threshold duration to conside if an app needs to be put in mislaneous category
    thrashold = 300
    # basic declearation for dataframe manupulation
    low_threshold = 5
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
    app_count = len(app_chart1)
    chart_list1.append(app_count)
    # print(chart_list1)
    return chart_list1, misc_apps, app_count
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
def chart_of_subapps(df, misc_apps, app_name):
    # Step 1: Catagorise app with small duration into a "misc" app category
    index = 0
    for app in df["Application"]:
        if (app in misc_apps):  # misc_apps is list of application/windows which were used for less than threshold time
            df.loc[
                index, "Application"] = "Miscellaneous"  # in the  -Application- Column we replce values with "misc" to catagorise

        index = index + 1
    # Step 2: Create a pivot table
    app_chart2 = pd.pivot_table(df, values="Suration", index=["Window"],
                                aggfunc=np.sum).reset_index()  # , columns=["Application"]
    # print(app_chart2)
    # Step 3: Add another column having application name, do se we will use a dictionaly to map sub-apps to app
    df_dict = dict(zip(df.Window, df.Application))
    app_chart2['apps'] = app_chart2['Window'].map(df_dict)  # "app_chart2" is the required dataframe
    # print(app_chart2)
    # Step 4: Convert Datafrme to list and Sublist "chart2_list"
    app_list = app_chart2.apps.unique()  # it is list of apps
    # chart2_list = app_list.tolist()
    # chart_list.append(chart2_list)
    num_of_apps = [len(app_list)]  # total no. of apps

    # chart_list.append(num_of_apps)
    # print(app_chart2)
    # for app in app_list: #here we extact sub-apps list and cumulative duration for each sub-apps for each

    chart_list2 = []
    # print(app_name)
    app_wise_df = app_chart2[app_chart2["apps"] == app_name]
    # print("whats this", app_wise_df)
    app_wise_df = app_wise_df.sort_values("Suration", axis=0, ascending=False, na_position='last').reset_index(
        drop=True)
    app_wise_df = app_wise_df[app_wise_df["Suration"] > 2]
    # print(app_wise_df)
    # print(app_wise_df.Window)

    app_wise_df["Duration"] = (app_wise_df["Suration"] / 60).astype('int32')
    # app_wise_df = app_wise_df[app_wise_df["Duration"] > 0]
    sub_list_window = app_wise_df.Window.tolist()
    # print(sub_list_window)
    chart_list2.append(sub_list_window)
    sub_list_duration = app_wise_df["Duration"].tolist()
    chart_list2.append(sub_list_duration)
    chart_list2.append(app_name)
    chart_list2.append(len(sub_list_window))
    # today = str(date.today())
    # print(type(today))
    # print(today)

    # send "chart2_list" to Chart.js
    # print(chart_list2)
    return chart_list2


# send "chart2_list" to Chart.js
def get_chart_data(data):
    # print(data)
    global date
    global df_date
    global max_date
    global min_date
    chart_list = []
    if data.get("y") is None:

        #df_date, max_date, min_date = get_date_specific_log(date)
        app_name = data.get("label")
        # print("getting data of sub app", app_name)
        chart_list1, misc_apps, app_count = chart_of_apps(df_date)
        # print("step 1 completed")
        chart_list2 = chart_of_subapps(df_date, misc_apps, app_name)
        # print("step 2 completed")
        chart_list.append(chart_list1)
        # print("step 3 completed")
        chart_list.append(chart_list2)
        # print("step 4 completed")
        chart_list.append(max_date)
        chart_list.append(min_date)


        chart_list.append(date)
        chart_list.append(app_count)
    else:
        date = data.get("y")
        year = date
        #print(year)
        # print("getting data of", year)
        df_date, max_date, min_date = get_date_specific_log(year)
        # print(df_date)
        app_name = "Miscellaneous"
        # print("Go/Home Button:",year, app_name)
        chart_list1, misc_apps, app_count = chart_of_apps(df_date)
        # print("step 1 completed")
        chart_list2 = chart_of_subapps(df_date, misc_apps, app_name)
        # print("step 2 completed")
        chart_list.append(chart_list1)
        # print("step 3 completed",chart_list1)
        chart_list.append(chart_list2)
        # print("step 4 completed",chart_list2)

        chart_list.append(max_date)
        chart_list.append(min_date)
        chart_list.append(year)
        chart_list.append(app_count)
        # print(chart_list)
    return chart_list


# Define an flask server app
#
# print(get_chart_data(3))

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('Awarness.html')


# set a socket to send message
@socketio.on('message')
def message(data):
    #print(f"{data}")
    #print(date)
    app_name = "Miscellaneous"  # llaneous"
    chart_list = []
    global df_date
    global min_date
    global max_data
    df_date, max_date, min_date = get_date_specific_log(date)
    chart_list1, misc_apps, app_count = chart_of_apps(df_date)
    chart_list2 = chart_of_subapps(df_date, misc_apps, app_name)
    chart_list.append(chart_list1)
    chart_list.append(chart_list2)
    chart_list.append(max_date)
    chart_list.append(min_date)
    chart_list.append(date)
    chart_list.append(app_count)
    data = chart_list
    #print(data)
    send(data, broadcast=True)

print("hey")
@app.route('/detail')
def detail():
    return render_template('Awarness_detail.html')


@socketio.on('msg')
def message(data):
    data = get_chart_data(data)
    # print(data)
    time.sleep(0.2)
    print(date)
    emit('message', data)


if __name__ == '__main__':
    socketio.run(app, debug = False, port =5000)












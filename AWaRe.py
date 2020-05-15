from time import sleep
import win32gui, pandas as pd
import datetime
datetime.datetime.now()
aw = win32gui
infinity = 0
TS = datetime.datetime.now()
AWR = "Dummy"
i = 0
duration = 0
AWRF = "abc"
columns = ["Time Stamp", "Window", "Suration"]
awl = pd.DataFrame(columns=columns)
awl_temp = pd.DataFrame(columns=columns)
while True:
    sleep(1)
    AWR = aw.GetWindowText(aw.GetForegroundWindow())
    while AWR != AWRF:
        #print(i)
        TS_str = str(TS)
        to_append = [TS_str, AWRF, i]
        #print(AWRF)
        TS = datetime.datetime.now()
        #print(TS_str)
        i = 0
        AWRF = AWR
        awl_length = len(awl)
        awl.loc[awl_length] = to_append
        awl.to_csv("awl.csv")
    i = i + 1
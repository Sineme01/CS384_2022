# importing the libraries.
# Here I have imported Pandas library for reading csv files and creating dataFrames.
from platform import python_version
import pandas as pd


def octact_identification(mod=5000):
    # Here we created our dataFrame and named it matrix.
    matrix = pd.read_csv("octant_input.csv")
    # Here using pandas library i have calculated mean of u,v,and w and stored it into a variable.
    uavg = matrix['U'].mean()
    vavg = matrix['V'].mean()
    wavg = matrix['W'].mean()
    # Here a list is created to store average values of u,v and w.
    list1 = [uavg]
    list2 = [vavg]
    list3 = [wavg]
    for i in range(len(matrix['Time'])-1):
        list1.append(None)
        list2.append(None)
        list3.append(None)

    # This is our output data Frame.
    submission = {"Time": matrix['Time'], "U": matrix["U"], "V": matrix["V"],
                  "W": matrix["W"], "U Avg": list1, "V Avg": list2, "W Avg": list3}

    # Here we have made list of u-uavg, v-vavg, w-wavg.
    u1 = [i-uavg for i in matrix['U']]
    v1 = [i-vavg for i in matrix['V']]
    w1 = [i-wavg for i in matrix['W']]
    col = pd.DataFrame(submission)
    # Here we are adding three columns in our data frmae for depicting three variables.
    col["U'=U-Uavg"] = u1
    col["V'=V-Vavg"] = v1
    col["W'=W-Wavg"] = w1

    OctantValue = []
    aa = col["U'=U-Uavg"].to_list()
    bb = col["V'=V-Vavg"].to_list()
    cc = col["W'=W-Wavg"].to_list()
    OctantValue = []
    d = {'+++': "+1", "++-": "-1", "-++": "+2", "-+-": "-2",
         "--+": "+3", "---": "-3", "+-+": "+4", "+--": "-4"}
    # loop for counting total octant values
    for i in range(len(aa)):
        x = ""
        if (aa[i] < 0):
            x += '-'
        else:
            x += '+'
        if (bb[i] < 0):
            x += '-'
        else:
            x += '+'
        if (cc[i] < 0):
            x += '-'
        else:
            x += '+'
        OctantValue.append(d[x])
    col["Octant"] = OctantValue

    data = {"": [None], "OctantID": "Overall Cost", 1: [OctantValue.count('+1')], -1: [OctantValue.count('-1')], 2: [OctantValue.count('+2')], -2: [OctantValue.count('-2')],
            3: [OctantValue.count('+3')], -3: [OctantValue.count('-3')], 4: [OctantValue.count('+4')], -4: [OctantValue.count('-4')]}
    # making another dataFrame for our final output.
    h = pd.DataFrame(data)
    t = mod
    new_row = {'': "User Input", "OctantID": "Mod"+" "+str(t)}
    h = h.append(new_row, ignore_index=True)
    length = len(matrix['Time'])

    for i in range(0, length, t):
        if (i+t-1 >= length):
            x = str(i)+"-"+str(29745)
        else:
            x = str(i)+"-"+str(i+t-1)

        j = {"OctantID": x, 1: OctantValue[i:i+t].count('+1'), -1: OctantValue[i:i+t].count('-1'), 2: OctantValue[i:i+t].count('+2'),
             -2: OctantValue[i:i+t].count('-2'), 3: OctantValue[i:i+t].count('+3'), -3: OctantValue[i:i+t].count('-3'),
             4: OctantValue[i:i+t].count('+4'), -4: OctantValue[i:i+t].count('-4')}
        h = h.append(j, ignore_index=True)
    Frames = [col, h]
    # Appending both the  dataFrames in single one.
    final = pd.concat(Frames, axis=1)
    final.to_csv("octant_output.csv", index=False)

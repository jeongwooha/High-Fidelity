import csv
import math
from collections import defaultdict
import numpy as np


###
# You must edit this part to get the correct data
filename = '20170302output.csv'
user_id_1 = '357a'
user_id_2 = '357b'


### Constants

# Column indexes for specific item in the csv file
TIME = 5 # column index for time in CSV
USER_ID = 47 # column index for user_id in CSV

AVATAR_POSITION_X = 11
AVATAR_POSITION_Z = 10

RIGHT_HAND_POSITION_X = 36
RIGHT_HAND_POSITION_Y = 37
RIGHT_HAND_POSITION_Z = 34
LEFT_HAND_POSITION_X = 18
LEFT_HAND_POSITION_Y = 16
LEFT_HAND_POSITION_Z = 14

RIGHT_CONTROLLER_POSITION_X = 32
RIGHT_CONTROLLER_POSITION_Y = 29
RIGHT_CONTROLLER_POSITION_Z = 30
LEFT_CONTROLLER_POSITION_X = 0
LEFT_CONTROLLER_POSITION_Y = 2
LEFT_CONTROLLER_POSITION_Z = 12

# When truncating UNIX timestamp to decmial points
UP_TO_FIRST_DECIMAL = 12
UP_TO_SECOND_DECIMAL = 13


# returns the start and end time of interaction between the two participants
def getInteractionInterval():
    interval = []

    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            time = row[TIME][:UP_TO_FIRST_DECIMAL]
            userid = row[USER_ID]
            if time == 'time': continue

            # if userid has timestamp on it
            if userid == user_id_1 + 'timestamp':
                print(userid)
                interval.append(time)

        # you should only have two timestamp values
        if len(interval) == 2:
            interval.sort()
            print 'valid interval'
            print 'interval', interval[0], interval[1]
        else:
            print 'invalid interval'
            return

        return (interval[0], interval[1])

# returns 2 arrays of data for both participants given the interval
def getDataWithinInterval():
    # get the interaction interval
    (start_interaction, end_interaction) = getInteractionInterval()

    ppt1 = []
    ppt2 = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)

        # for each participant, add the data if it is in between the timestamp interval
        for row in reader:
            time = row[TIME][:UP_TO_FIRST_DECIMAL]
            if time == 'time':
                print(row)
                continue # ignore the first row
            # add data that are only in between the interaction timestamp
            if float(time) >= float(start_interaction) and float(time) <= float(end_interaction):
                if row[USER_ID] == user_id_1:
                    #time_1.append(float(time))
                    ppt1.append(row) # add the batch
                if row[USER_ID] == user_id_2:
                    #time_2.append(float(time))
                    ppt2.append(row) # add the batch

        print 'number of data within the interval', len(ppt1), len(ppt2)
        return (ppt1, ppt2)

# returns 2 arrays of data for both participants with the same timestamp
def matchDataByTime():
    # get data within the interval
    (ppt1, ppt2) = getDataWithinInterval()

    ppt1_matched = []
    ppt2_matched = []
    count = 0

    for i in range(len(ppt1)):
        for j in range(len(ppt2)):
            time1 = ppt1[i][TIME][:UP_TO_FIRST_DECIMAL]
            time2 = ppt2[j][TIME][:UP_TO_FIRST_DECIMAL]
            # if time matches put the batch into a new array
            if time1 == time2:
                count += 1
                ppt1_matched.append(ppt1[i])
                ppt2_matched.append(ppt2[j])

    print 'number of data points with matching timestamp: ', count
    return (ppt1_matched, ppt2_matched)

# calculates the minimum distance given two arrays of data points
def calculateMinDistance(ppt1, ppt2):
    minDistance = float('+inf')
    for i in range(len(ppt1)):
        data1 = ppt1[i] # PPT1
        data2 = ppt2[i] # PPT2

        # Due to different coordinate system in PPT1 and PPT2,
        # we compare x position of PPT2 with -z position of PPT1,
        # and z position of PPT2 with x position of PPT1
        # PPT1(-z, x) and PPT2(x, z)

        ppt1_x = float(ppt1[i][AVATAR_POSITION_X])
        ppt1_z = float(ppt1[i][AVATAR_POSITION_Z])
        ppt2_x = float(ppt2[i][AVATAR_POSITION_X])
        ppt2_z = float(ppt2[i][AVATAR_POSITION_Z])
        distance = math.hypot(ppt2_x + ppt1_z, ppt2_z - ppt1_x)
        if distance < minDistance:
            minDistance = distance

    return minDistance

# calculates the standard deviation of the data points
# right hand positions x,y,z
# left hand positions x,y,z
# right controller positions x,y,z
# left controller positions x,y,z
def calculateSD(data):
    SDList = defaultdict(list)
    right_hand_positions_x = []
    right_hand_positions_y = []
    right_hand_positions_z = []
    left_hand_positions_x = []
    left_hand_positions_y = []
    left_hand_positions_z = []
    right_controller_positions_x = []
    right_controller_positions_y = []
    right_controller_positions_z = []
    left_controller_positions_x = []
    left_controller_positions_y = []
    left_controller_positions_z = []

    # add them to separate arrays
    for i in range(len(data)):
        right_hand_positions_x.append(float(data[i][RIGHT_HAND_POSITION_X]))
        right_hand_positions_y.append(float(data[i][RIGHT_HAND_POSITION_Y]))
        right_hand_positions_z.append(float(data[i][RIGHT_HAND_POSITION_Z]))
        left_hand_positions_x.append(float(data[i][LEFT_HAND_POSITION_X]))
        left_hand_positions_y.append(float(data[i][LEFT_HAND_POSITION_Y]))
        left_hand_positions_z.append(float(data[i][LEFT_HAND_POSITION_Z]))
        right_controller_positions_x.append(float(data[i][RIGHT_CONTROLLER_POSITION_X]))
        right_controller_positions_y.append(float(data[i][RIGHT_CONTROLLER_POSITION_Y]))
        right_controller_positions_z.append(float(data[i][RIGHT_CONTROLLER_POSITION_Z]))
        left_controller_positions_x.append(float(data[i][LEFT_CONTROLLER_POSITION_X]))
        left_controller_positions_y.append(float(data[i][LEFT_CONTROLLER_POSITION_Y]))
        left_controller_positions_z.append(float(data[i][LEFT_CONTROLLER_POSITION_Z]))

    SDList['right_hand_position_x'] = np.std(right_hand_positions_x)
    SDList['right_hand_position_y'] = np.std(right_hand_positions_y)
    SDList['right_hand_position_z'] = np.std(right_hand_positions_z)
    SDList['left_hand_position_x'] = np.std(left_hand_positions_x)
    SDList['left_hand_position_y'] = np.std(left_hand_positions_y)
    SDList['left_hand_position_z'] = np.std(left_hand_positions_z)
    SDList['right_controller_position_x'] = np.std(right_controller_positions_x)
    SDList['right_controller_position_y'] = np.std(right_controller_positions_y)
    SDList['right_controller_position_z'] = np.std(right_controller_positions_z)
    SDList['left_controller_position_x'] = np.std(left_controller_positions_x)
    SDList['left_controller_position_y'] = np.std(left_controller_positions_y)
    SDList['left_controller_position_z'] = np.std(left_controller_positions_z)

    return SDList

# Main function to run synchrony algorithm
def synchronyAlgorithm():
    # get arrays of data with matched timestamp
    (ppt1, ppt2) = matchDataByTime()
    print(len(ppt1), len(ppt2))

    minDistance = calculateMinDistance(ppt1, ppt2)
    print('minDistance', minDistance)

    ppt1_SDList = calculateSD(ppt1)
    ppt2_SDList = calculateSD(ppt2)
    print ppt1_SDList
    print ppt2_SDList


synchronyAlgorithm()

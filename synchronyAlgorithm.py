import csv
import math
from collections import defaultdict
import numpy as np
from scipy.stats.stats import pearsonr

###
# To get the newest csv output,
# node dynamoDBtoCSV.js -t study_stats > [today's date]output.csv


### 359ab, synchrony12, normal12, random12
# You must edit this part to get the correct data
filename = '20170426output.csv'
user_id_1 = '358a'
user_id_2 = '358b'


### Constants

# Column indexes for specific item in the csv file
TIME = 5 # column index for time in CSV
USER_ID = 47 # column index for user_id in CSV

AVATAR_POSITION_X = 11
AVATAR_POSITION_Z = 10

HEAD_POSITION_X = 4
HEAD_POSITION_Y = 3
HEAD_POSITION_Z = 1

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

            # We are using userid1 because RA is pressing 'q' button in PPT1
            # if userid1 has timestamp on it
            if userid == user_id_1 + 'timestamp':
                print(userid)
                print time
                interval.append(time)

        # you should only have two timestamp values
        if len(interval) == 2:
            interval.sort()
            print 'valid interval'
            print 'interval', interval[0], interval[1]
        else:
            print len(interval)
            print 'invalid interval'
            return

        return (interval[0], interval[1])

# returns 2 arrays of data for both participants given the interval
def getDataWithinInterval():
    # get the interaction interval
    (start_interaction, end_interaction) = getInteractionInterval()
    #(start_interaction, end_interaction) = (1487886092.1, 1487886904.2) for 354ab
    
    # for normal12
    #tart_interaction = '1491852479.4'
    #end_interaction = '1491852738.9'


    ppt1 = []
    ppt2 = []
    unique = []
    u = []
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
                #print float(time)
                #if float(time) not in u:
                u.append(float(time))
                unique.append(float(time))
                if row[USER_ID] == user_id_1:
                    #time_1.append(float(time))
                    ppt1.append(row) # add the batch
                if row[USER_ID] == user_id_2:
                    #time_2.append(float(time))
                    ppt2.append(row) # add the batch

        #sorted(ppt1, key=lambda time: )

        unique_list = list(set(unique))
        print 'nunique', len(unique_list)
        #print sorted(unique_list)
        print 'nu', len(u)
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
        time1 = ppt1[i][TIME][:UP_TO_FIRST_DECIMAL]
        for j in range(len(ppt2)):
            time2 = ppt2[j][TIME][:UP_TO_FIRST_DECIMAL]
            # if time matches put the batch into a new array
            if float(time1) == float(time2):
                #print time1, time2
                count += 1
                ppt1_matched.append(ppt1[i])
                ppt2_matched.append(ppt2[j])

    print 'number of data points with matching timestamp: ', count

    # sort data by time
    ppt1_matched = sorted(ppt1_matched, key=lambda data: data[TIME])
    ppt2_matched = sorted(ppt2_matched, key=lambda data: data[TIME])
    # for i in range(len(ppt1_matched)):
        # print ppt1_matched[i][TIME], ppt2_matched[i][TIME]

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
        # distance = math.hypot(ppt2_x + ppt1_z, ppt2_z - ppt1_x)

        # avatar positions x,y,z are relative to the virtual environment,
        # thus no need to adjust for the real coordinate
        distance = math.hypot(ppt1_x - ppt2_x, ppt1_z - ppt2_z)
        if distance < minDistance:
            minDistance = distance

    return minDistance

# creates a dictionary that contains all the data as value of data type key
def createDataDict(data):

    # dictionary where key is data type and value is the array of data
    dataDict = defaultdict(list)

    head_positions_x = []
    head_positions_y = []
    head_positions_z = []

    right_hand_positions_x = []
    right_hand_positions_y = []
    right_hand_positions_z = []

    left_hand_positions_x = []
    left_hand_positions_y = []
    left_hand_positions_z = []
    # right_controller_positions_x = []
    # right_controller_positions_y = []
    # right_controller_positions_z = []
    # left_controller_positions_x = []
    # left_controller_positions_y = []
    # left_controller_positions_z = []

    for i in range(len(data)):
        # head positions
        head_positions_x.append(float(data[i][HEAD_POSITION_X]))
        head_positions_y.append(float(data[i][HEAD_POSITION_Y]))
        head_positions_z.append(float(data[i][HEAD_POSITION_Z]))

        # right hand positions
        right_hand_positions_x.append(float(data[i][RIGHT_HAND_POSITION_X]))
        right_hand_positions_y.append(float(data[i][RIGHT_HAND_POSITION_Y]))
        right_hand_positions_z.append(float(data[i][RIGHT_HAND_POSITION_Z]))

        # left hand positions
        left_hand_positions_x.append(float(data[i][LEFT_HAND_POSITION_X]))
        left_hand_positions_y.append(float(data[i][LEFT_HAND_POSITION_Y]))
        left_hand_positions_z.append(float(data[i][LEFT_HAND_POSITION_Z]))
        # right_controller_positions_x.append(float(data[i][RIGHT_CONTROLLER_POSITION_X]))
        # right_controller_positions_y.append(float(data[i][RIGHT_CONTROLLER_POSITION_Y]))
        # right_controller_positions_z.append(float(data[i][RIGHT_CONTROLLER_POSITION_Z]))
        # left_controller_positions_x.append(float(data[i][LEFT_CONTROLLER_POSITION_X]))
        # left_controller_positions_y.append(float(data[i][LEFT_CONTROLLER_POSITION_Y]))
        # left_controller_positions_z.append(float(data[i][LEFT_CONTROLLER_POSITION_Z]))

    dataDict['head_position_x'] = head_positions_x
    dataDict['head_position_y'] = head_positions_y
    dataDict['head_position_z'] = head_positions_z
    dataDict['right_hand_position_x'] = right_hand_positions_x
    dataDict['right_hand_position_y'] = right_hand_positions_y
    dataDict['right_hand_position_z'] = right_hand_positions_z
    dataDict['left_hand_position_x'] = left_hand_positions_x
    dataDict['left_hand_position_y'] = left_hand_positions_y
    dataDict['left_hand_position_z'] = left_hand_positions_z
    # dataDict['right_controller_position_x'] = right_controller_positions_x
    # dataDict['right_controller_position_y'] = right_controller_positions_y
    # dataDict['right_controller_position_z'] = right_controller_positions_z
    # dataDict['left_controller_position_x'] = left_controller_positions_x
    # dataDict['left_controller_position_y'] = left_controller_positions_y
    # dataDict['left_controller_position_z'] = left_controller_positions_z

    return dataDict

# calculates the standard deviation of the data points
# right hand positions x,y,z
# left hand positions x,y,z
# right controller positions x,y,z
# left controller positions x,y,z
def calculateSD(dataDict):
    SDList = defaultdict(list)

    for k,v in dataDict.iteritems():
        SDList[k] = np.std(v)

    return SDList

# calculates the rate of movement
# since the absolute position of the two participants
# are different, we must compare the change in position for each data
# instead of the absolute positions.
def calculateRate(dataDict):
    rateDict = defaultdict(list)

    for k,v in dataDict.iteritems():
        rateList = []
        for i in range(len(v)-1):
            currVal = v[i]
            nextVal = v[i+1]
            rateList.append(nextVal - currVal) # calculate the rate
        rateDict[k] = rateList

    return rateDict

# calculates the Pearson's correlation coefficient between data for the two participants
# i.e., compare participant 1's right_hand_position_x and
# participant 2's right_hand_position_x
# Returns a dictionary with the calculated data
# interval is the timestamp interval of which we want to compute the correlation
# offset is the time offset to the interval to measure if there was any delayed synchrony

# ** important **
# We must comapre ppt1's -z with ppt2's x
# ppt1's x with ppt2's z
# ppt1's y with ppyt2'y

def calculateCorrelations(ppt1, ppt2, interval, offset):
    correlationList = defaultdict(list)

    nInterval = len(ppt1['right_hand_position_x']) / interval + 1
    # they are in timestamp order
    for k,_ in ppt1.iteritems():
        # only interested in the Pearson's correlation coefficient,
        # not the 2-tailed p-value, so return the first index
        # correlationList[k] = pearsonr(ppt1[k], ppt2[k])[0]

        # nInterval = len(ppt1[k]) / interval + 1
        # print nInterval

        start = 0
        end = interval - 1
        for i in range(nInterval - 1):
            #if k != 'right_hand_position_x': continue
            print k, i, start, end, nInterval
            if i == nInterval - 2:
                print "last"
                # Last

                print pearsonr(ppt1[k][start:], ppt2['left_hand_position_x'][start:])[0]
                print pearsonr(ppt1[k][start:], ppt2['right_hand_position_x'][start:])[0]
            else:
                # add offset
                if k == 'right_hand_position_x':
                    #ppt1's x to ppt2's z
                    print pearsonr(ppt1[k][start:end], ppt2['left_hand_position_z'][start+offset:end+offset])[0]
                    print pearsonr(ppt1[k][start:end], ppt2['right_hand_position_z'][start+offset:end+offset])[0]
                if k == 'right_hand_position_y':
                    print pearsonr(ppt1[k][start:end], ppt2['left_hand_position_y'][start+offset:end+offset])[0]
                    print pearsonr(ppt1[k][start:end], ppt2['right_hand_position_y'][start+offset:end+offset])[0]
                if k == 'right_hand_position_z':
                    # ppt1's -z to ppt2's x
                    print pearsonr([ -i for i in ppt1[k][start:end] ], [ -i for i in ppt2['left_hand_position_x'][start+offset:end+offset] ])[0]
                    print pearsonr([ -i for i in ppt1[k][start:end] ], [ -i for i in ppt2['right_hand_position_x'][start+offset:end+offset] ])[0]
                if k == 'left_hand_position_x':
                    # ppt1's x to ppt2'z
                    print pearsonr(ppt1[k][start:end], ppt2['left_hand_position_z'][start+offset:end+offset])[0]
                    print pearsonr(ppt1[k][start:end], ppt2['right_hand_position_z'][start+offset:end+offset])[0]
                if k == 'left_hand_position_y':
                    print pearsonr(ppt1[k][start:end], ppt2['left_hand_position_y'][start+offset:end+offset])[0]
                    print pearsonr(ppt1[k][start:end], ppt2['right_hand_position_y'][start+offset:end+offset])[0]
                if k == 'left_hand_position_z':
                    # ppt1's -z to ppt2's x
                    print pearsonr([ -i for i in ppt1[k][start:end] ], ppt2['left_hand_position_x'][start+offset:end+offset])[0]
                    print pearsonr([ -i for i in ppt1[k][start:end] ], ppt2['right_hand_position_x'][start+offset:end+offset])[0]
                start = end + 1
                end = start + interval - 1


        '''
        # find correlations for all combinations
        # of right hand, left hand, and head
        if k == 'right_hand_position_x':
            #correlationList[k + '_to_left_hand_position_x'] = pearsonr(ppt1[k], ppt2['left_hand_position_x'])[0]
            correlationList[k + '_to_right_hand_position_x'] = pearsonr(ppt1[k], ppt2['right_hand_position_x'])[0]
            correlationList[k + '_to_head_position_x'] = pearsonr(ppt1[k], ppt2['head_position_x'])[0]
        if k == 'right_hand_position_y':
            correlationList[k + '_to_left_hand_position_y'] = pearsonr(ppt1[k], ppt2['left_hand_position_y'])[0]
            correlationList[k + '_to_right_hand_position_y'] = pearsonr(ppt1[k], ppt2['right_hand_position_y'])[0]
            #correlationList[k + '_to_head_position_y'] = pearsonr(ppt1[k], ppt2['head_position_y'])[0]
        if k == 'right_hand_position_z':
            correlationList[k + '_to_left_hand_position_z'] = pearsonr(ppt1[k], ppt2['left_hand_position_z'])[0]
            correlationList[k + '_to_right_hand_position_z'] = pearsonr(ppt1[k], ppt2['right_hand_position_z'])[0]
            #correlationList[k + '_to_head_position_z'] = pearsonr(ppt1[k], ppt2['head_position_z'])[0]
        if k == 'left_hand_position_x':
            correlationList[k + '_to_left_hand_position_x'] = pearsonr(ppt1[k], ppt2['left_hand_position_x'])[0]
            correlationList[k + '_to_right_hand_position_x'] = pearsonr(ppt1[k], ppt2['right_hand_position_x'])[0]
            #correlationList[k + '_to_head_position_x'] = pearsonr(ppt1[k], ppt2['head_position_x'])[0]
        if k == 'left_hand_position_y':
            correlationList[k + '_to_left_hand_position_y'] = pearsonr(ppt1[k], ppt2['left_hand_position_y'])[0]
            correlationList[k + '_to_right_hand_position_y'] = pearsonr(ppt1[k], ppt2['right_hand_position_y'])[0]
            #correlationList[k + '_to_head_position_y'] = pearsonr(ppt1[k], ppt2['head_position_y'])[0]
        if k == 'left_hand_position_z':
            correlationList[k + '_to_left_hand_position_z'] = pearsonr(ppt1[k], ppt2['left_hand_position_z'])[0]
            correlationList[k + '_to_right_hand_position_z'] = pearsonr(ppt1[k], ppt2['right_hand_position_z'])[0]
            #correlationList[k + '_to_head_position_z'] = pearsonr(ppt1[k], ppt2['head_position_z'])[0]
        '''

    return correlationList

# Main function to run synchrony algorithm
def synchronyAlgorithm():
    # get arrays of data with matched timestamp in order
    (ppt1, ppt2) = matchDataByTime()
    print(len(ppt1), len(ppt2))

    # Minimum Distance
    minDistance = calculateMinDistance(ppt1, ppt2)
    print '---------------------------'
    print '---Minimum Distance'
    print('minDistance', minDistance)
    print '---------------------------'

    # Get data dictionary for each participant
    ppt1DataDict = createDataDict(ppt1)
    ppt2DataDict = createDataDict(ppt2)

    # Standard Deviation
    ppt1SDList = calculateSD(ppt1DataDict)
    ppt2SDList = calculateSD(ppt2DataDict)
    print '---------------------------'
    print '---Standard Deviation'
    print '---PPT1'
    print ppt1SDList
    print '---PPT2'
    print ppt2SDList
    print '---------------------------'

    # Get rate data dictionary
    ppt1RateDict = calculateRate(ppt1DataDict)
    ppt2RateDict = calculateRate(ppt2DataDict)

    # Correlations
    correlationList = calculateCorrelations(ppt1RateDict, ppt2RateDict, 100, 0)
    print '---------------------------'
    print '---Pearson\'s correlation coefficients'
    print '---In terms of PPT1: meaning PPT1\'s right hand <=> PPT2\'s left hand'
    print correlationList
    print '---------------------------'





synchronyAlgorithm()

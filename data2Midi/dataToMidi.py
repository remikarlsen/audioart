from miditime.miditime import MIDITime
import datetime
import sys
import numpy as np
from sklearn.preprocessing import MaxAbsScaler

DEBUG_MODE=False
bpm=75
dataSource="BMData.csv"
midiFileName="dataart" + str(bpm) + ".mid"
octaveRange=3
secondsPerYear=60
baseOctave=5
upper_max=100 #All data values above 100 is set to 100
lower_min=1

# Instantiate the class with a tempo (120bpm is the default) and an output file destination.
mymidi = MIDITime(bpm, midiFileName, secondsPerYear, baseOctave, octaveRange)

def run(DEBUGMODE):
    data = []
    if DEBUGMODE==True:
        data = createDebugData()
        startTime, dataTimed = createMiditimeStructure(data)
        createNoteList(startTime, dataTimed)
    else:
        keyArr, varArr = loadData()
        data = createScaledData(keyArr, varArr)
    startTime, dataTimed = createMiditimeStructure(data)
    createNoteList(startTime, dataTimed)

def loadData():
    keyArr=[]
    varArr=[]
    with open(dataSource) as myfile:
        for line in myfile:
            name, var = line.partition(",")[::2]
            var = int(var)
            if var > upper_max:
                var = upper_max
            if var < lower_min:
                var = lower_min
            keyArr.append(name)
            varArr.append(var)
    varArr = [float(i) for i in varArr]
    return keyArr, varArr

def scaleData(varArr):
    npArr = np.array(varArr)
    npArr = npArr.reshape(-1,1)
    ma_scaler = MaxAbsScaler()
    scaledData = ma_scaler.fit_transform(npArr)
    scaledData = scaledData.flatten()
    return scaledData

def createScaledData(keyArr, varArr):
    tmpData = []
    scaledData=scaleData(varArr)
    for idx, val in enumerate(keyArr):
        d = {'event_date':datetime.datetime.strptime(val, '%Y-%m-%d'), 'magnitude':scaledData[idx]}
        tmpData.append(d)
    return tmpData

def createMiditimeStructure(data):
    data_epoched = [{'days_since_epoch': mymidi.days_since_epoch(d['event_date']), 'magnitude': d['magnitude']} for d in data]
    data_timed = [{'beat': mymidi.beat(d['days_since_epoch']), 'magnitude': d['magnitude']} for d in data_epoched]
    start_time = data_timed[0]['beat']
    return start_time, data_timed

def mag_to_pitch_tuned(magnitude):
    # Where does this data point sit in the domain of your data? (I.E. the min magnitude is 3, the max in 5.6). In this case the optional 'True' means the scale is reversed, so the highest value will return the lowest percentage.
    scale_pct = mymidi.linear_scale_pct(0, 1, magnitude)
    # Another option: Linear scale, reverse order
    # scale_pct = mymidi.linear_scale_pct(3, 5.7, magnitude, True)
    # Another option: Logarithmic scale, reverse order
    # scale_pct = mymidi.log_scale_pct(3, 5.7, magnitude, True)

    # Pick a range of notes. This allows you to play in a key.
    c_major = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    c_minor = ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb', 'C']

    #Find the note that matches your data point
    note = mymidi.scale_to_note(scale_pct, c_major)

    #Translate that note to a MIDI pitch
    midi_pitch = mymidi.note_to_midi_pitch(note)

    return midi_pitch

def createNoteList(start_time, data_timed):
    note_list = []
    for d in data_timed:
        note_list.append([
            d['beat'] - start_time,
            mag_to_pitch_tuned(d['magnitude']),
            100,  # velocity
            1  # duration, in beats
        ])
    # Add a track with those notes
    mymidi.add_track(note_list)
    # Output the .mid file
    mymidi.save_midi()

def createDebugData():
    test_data = [
        {'event_date': datetime.datetime.strptime('2016-01-01', '%Y-%m-%d'), 'magnitude': 0.1},
        {'event_date': datetime.datetime.strptime('2016-01-02', '%Y-%m-%d'), 'magnitude': 0.32455},
        {'event_date': datetime.datetime.strptime('2016-01-03', '%Y-%m-%d'), 'magnitude': 0.54888},
        {'event_date': datetime.datetime.strptime('2016-01-04', '%Y-%m-%d'), 'magnitude': 0.755644},
        {'event_date': datetime.datetime.strptime('2016-01-05', '%Y-%m-%d'), 'magnitude': 0.853344},
        {'event_date': datetime.datetime.strptime('2016-01-06', '%Y-%m-%d'), 'magnitude': 0.943344},
        {'event_date': datetime.datetime.strptime('2016-01-07', '%Y-%m-%d'), 'magnitude': 0.973344},
        {'event_date': datetime.datetime.strptime('2016-01-08', '%Y-%m-%d'), 'magnitude': 1.}
        ]
    return test_data

run(DEBUG_MODE)

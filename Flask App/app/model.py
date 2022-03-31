import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy import signal
from scipy.io import wavfile
import pylab
import matplotlib.mlab as ml
from scipy.fftpack import fft
#import pyaudio
import struct
import pickle
from sys import byteorder
from array import array
from struct import pack

#%matplotlib tk

with open("app/hashtable.pkl", "rb") as input_file:
    hashtable = pickle.load( input_file)
with open("app/songid.pkl", "rb") as input_file:
    song_dict = pickle.load(input_file)

file = open('app/songs.txt','r')#list of song files ----> use      ls >allsongs
allsongs = file.readlines()
allsongs = [a[:-1] for a in allsongs]
numOfSongs = len(allsongs)

DEFAULT_FS = 44100
DEFAULT_WINDOW_SIZE = 4096
DEFAULT_OVERLAP_RATIO = 0.5
DEFAULT_FAN_VALUE = 15
DEFAULT_AMP_MIN = 10

def graph_spectrogram(sound_info, frame_rate):
    pylab.figure(num=None, figsize=(19, 12))
    pylab.subplot(111)
    pylab.specgram(sound_info, Fs=frame_rate)
    pylab.savefig('spectrogram.png')

"""
Function that converts a byte string into a numpy array
"""
def _wav2array(nchannels, sampwidth, data):
    num_samples, remainder = divmod(len(data), sampwidth * nchannels)
    if remainder > 0:
        raise ValueError('The length of data is not a multiple of '
                         'sampwidth * num_channels.')
    if sampwidth > 4:
        raise ValueError("sampwidth must not be greater than 4.")

    if sampwidth == 3:
        a = np.empty((num_samples, nchannels, 4), dtype=np.uint8)
        raw_bytes = np.fromstring(data, dtype=np.uint8)
        a[:, :, :sampwidth] = raw_bytes.reshape(-1, nchannels, sampwidth)
        a[:, :, sampwidth:] = (a[:, :, sampwidth - 1:sampwidth] >> 7) * 255
        result = a.view('<i4').reshape(a.shape[:-1])
    else:
        dt_char = 'u' if sampwidth == 1 else 'i'
        a = np.fromstring(data, dtype='<%s%d' % (dt_char, sampwidth))
        result = a.reshape(-1, nchannels)
    return result

"""
Function to convert stereo to mono
"""

def stereo2mono(audiodata, nchannels):
#     if nchannels==1:
#         return audiodata.astype(int)
    audiodata = audiodata.astype(float)
    d = audiodata.sum(axis=1) / 2
    return d.astype(int)

"""
Class containing details of the wav file that has been read.
Sample use:
    song_x = song("abc.wav")
"""
class song:
    def __init__(self, file, songid):
        wav = wave.open(file)
        self.song_id = songid
        self.title = file.split("/")[-1]
        self.rate = wav.getframerate()
        self.nchannels = wav.getnchannels()
        self.sampwidth = wav.getsampwidth()
        self.nframes = wav.getnframes()
        self.data = wav.readframes(self.nframes)
        self.array = stereo2mono(_wav2array(self.nchannels, self.sampwidth, self.data), self.nchannels)
        wav.close()
    def spectrogram(self):
        self.specgram, self.frequencies, self.times = ml.specgram(self.array, Fs=self.rate, NFFT = 4096, window = ml.window_hanning, noverlap = int(4096 * 0.5), mode='magnitude')
        self.specgram = 10*np.log10(self.specgram)
        self.specgram[self.specgram==-np.inf] = 0
#         self.specgram = (1/20)*(np.exp(self.specgram))
#         self.specgram[self.specgram<100000000000000000] = 100000000000000000
#         self.specgram[self.specgram>10000000000000000000] = 10000000000000000000
#         fig, ax = plt.subplots()
#         ax.imshow(self.specgram, aspect='auto')
#         ax.set_xlabel('Time')
#         ax.set_ylabel('Frequency')
#         ax.set_title("Spectrogram of "+self.title)
#         plt.gca().invert_yaxis()
#         plt.show()
    def find_key(self):
        self.spectrogram()
        all_times = self.specgram.transpose()
        #self.all_times = all_times
        bands = []
        count = 0
        for a in all_times:
            l = []
            x = max(a[0:10])
            l.append((x, [list(a[0:10]).index(x),self.times[count]]))
            x = max(a[10:20])
            l.append((x, [list(a[10:20]).index(x)+10,self.times[count]]))
            x = max(a[20:40])
            l.append((x, [list(a[20:40]).index(x)+20,self.times[count]]))
            x = max(a[40:80])
            l.append((x, [list(a[40:80]).index(x)+40,self.times[count]]))
            x = max(a[80:160])
            l.append((x, [list(a[80:160]).index(x)+80,self.times[count]]))
            x = max(a[160:510])
            l.append((x, [list(a[160:510]).index(x)+160,self.times[count]]))
            bands.append(l)
            count+=1
        l = []
        #print('length',len(bands))
        for a in bands:
            for b in a:
                l.append(b[0])
        #l has all the amplitudes in bands
        mean = .1*np.mean(l)
        new_bands = []
        for i in range(0, len(bands)):
            a = bands[i]
            m = [t[1] for t in a if t[0]>mean]
            if len(m)!=0:
                new_bands.append(m)
        self.bands = new_bands
    def cal_address(self):
        new_bands = []
        for ele in self.bands:
            for sub in ele:
                new_bands.append(sub)
        self.addresses = {}
        target_zone = 0
        for i in range(3,len(new_bands)-4):
            anchor_point = new_bands[i-3]
            for ele in new_bands[i:i+5]:
                diff = float("%.2f"%(ele[1] - anchor_point[1]))
                val =  float("%.2f"%(anchor_point[1]))
                if (anchor_point[0],ele[0],diff) not in self.addresses.keys():
                    self.addresses[anchor_point[0],ele[0],diff] = []
                self.addresses[anchor_point[0],ele[0],diff].append([val,target_zone])
            target_zone+=1
        print(target_zone)
    def search(self):
        #search
        matched_couples = []
        for key in self.addresses:
            if key in hashtable.keys():
                matched_couples.append(hashtable[key])
        
        count = [0 for i in range(numOfSongs)]
        target_zone_keys = {}
        for ele in matched_couples:
            for subele in ele:
                count[subele[1]]+=1
                tup = (subele[1],subele[2])
                if tup not in target_zone_keys.keys():
                    target_zone_keys[tup] = 0
                target_zone_keys[tup]+=1
        
        matched_target_zone = [0 for i in range(numOfSongs)]
        for key in target_zone_keys:
            if target_zone_keys[key]==5:
                matched_target_zone[key[0]]+=1
        print('matched target zone ',matched_target_zone)
        return matched_target_zone.index(max(matched_target_zone))

def predict(filepath):
    # chunk = 4096
    # channels = 1
    # rate = 44100
    # record_seconds = 20
    # NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
    # FRAME_MAX_VALUE = 2 ** 15 - 1

    #read file contents
    #write file contents to output.wav
    total = song(filepath, 0)
    total.find_key()
    total.cal_address()
    idx = total.search()

    #print('Predicted Song {}'.format(allsongs[idx]))

    remove_wav = (allsongs[idx]).replace('.wav', '')
    predicted_song = remove_wav.replace(' ', '%20')
    # print(predicted_song)

    youtube_link = "https://www.youtube.com/results?search_query="
    youtube_song_link = "".join((youtube_link, predicted_song, "%20guitar%20lesson"))
    # print("Youtube Lesson - " + youtube_song_link +"%20guitar%20lesson")

    guitar_tab_link = "https://www.ultimate-guitar.com/search.php?search_type=title&value="
    guitar_tab_song_link = "".join((guitar_tab_link, predicted_song))
    # print("Guitar Tab - " + guitar_tab_song_link)

    return {
        "prediction" : remove_wav,
        "youTube" : youtube_song_link,
        "guitar" : guitar_tab_song_link
    }

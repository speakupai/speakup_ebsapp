# python3

''' create librosa spectorgram '''

import librosa
from librosa.feature import melspectrogram
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os

from numpy.core.fromnumeric import size

def create_spectrogram(audio_file, value):
   snd, sr = librosa.load(audio_file, sr=16000) 
   spect = melspectrogram(y=snd, sr=sr)
   fig, ax = plt.subplots()
   S_dB = librosa.power_to_db(spect, ref=np.max)
   img = librosa.display.specshow(S_dB, x_axis='time',
                        y_axis='mel', sr=sr,
                        fmax=8000, ax=ax)
   fig.colorbar(img, ax=ax, format='%+2.0f dB')
   ax.set(title='Mel-frequency spectrogram')
   save_path = './static/spect'+value+'.png'
   #save_path = './static/spect.png'
   plt.savefig(save_path)

   return save_path
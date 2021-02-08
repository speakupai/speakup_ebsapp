# python3

''' create librosa spectorgram '''

import librosa
from librosa.feature import melspectrogram
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
import time

save_folder = '/home/taimur/Documents/Online Courses/Fourth Brain/Projects/Audio_super_res/ml_deployment/static'

def spect_stream(audio_orig, audio_clean):
   # find duration
   clip_len_orig = librosa.get_duration(filename = audio_orig, sr=16000)
   clip_len_clean = librosa.get_duration(filename = audio_clean, sr=16000)
   
   # load audio
   for sub_clip in range(0, int(clip_len_orig), 10):
      # load subsample of the file
      snd_orig, sr_orig = librosa.load(audio_orig, sr=16000, offset=sub_clip, duration=10)
      snd_clean, sr_clean = librosa.load(audio_clean, sr=16000, offset=sub_clip, duration=10)

      # create spectrogram
      spect_orig = melspectrogram(y=snd_orig, sr=sr_orig)
      spect_clean = melspectrogram(y=snd_clean, sr=sr_clean)
      fig, ax = plt.subplots()
      S_dB_orig = librosa.power_to_db(spect_orig, ref=np.max)
      img_orig = librosa.display.specshow(S_dB_orig, x_axis='time',
                                     y_axis='mel', sr=sr_orig,
                                     fmax=8000, ax=ax)
      S_dB_clean = librosa.power_to_db(spect_clean, ref=np.max)
      img_clean = librosa.display.specshow(S_dB_clean, x_axis='time',
                                     y_axis='mel', sr=sr_clean,
                                     fmax=8000, ax=ax)
      fig.colorbar(img_orig, ax=ax, format='%+2.0f dB')
      ax.set(title='Mel-frequency spectrogram')

      fig.savefig(os.path.join(save_folder, 'orig.png'), format='png')
      plt.show()
      time.sleep(5.0)

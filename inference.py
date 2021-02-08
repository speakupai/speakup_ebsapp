import os

import librosa
import numpy as np
import soundfile as sf
import torch
from torch.cuda.amp import autocast

from utils import core, data
from models.hifi_gan import Generator
from models.wavenet import WaveNet

from utils.hparams import hparams as hp


def inference(audio_clip):
    original_file = audio_clip
    save_dir = '/home/taimur/Documents/Online Courses/Fourth Brain/Projects/Audio_super_res/ml_deployment/uploads'
    checkpoint_path = '/home/taimur/Documents/Online Courses/Fourth Brain/Projects/Audio_super_res/ml_deployment/saved_model/latest_checkpoint.pt'
    #default_inf_device = 'cpu',

    #choices=['cpu'] + [f'cuda:{d}' for d in range(torch.cuda.device_count())], type=str,

    # Load checkpoint
    checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))

    # Initializing model, optimizer, criterion and scaler
    model = Generator(wavenet=WaveNet())
    model.to('cpu')
    model.load_state_dict(checkpoint['generator_state_dict'])
    model.eval()

    if os.path.isdir(original_file):
        inference_files = core.dir_walk(original_file, ('.wav', '.mp3', '.ogg'))
    elif os.path.isfile(original_file):
        inference_files = [original_file]
    else:
        raise Exception('input must be .wav file or dir containing audio files.')

    with torch.no_grad():
        for file in inference_files:
            filename = os.path.splitext(os.path.split(file)[1])[0]
            x, _ = librosa.load(file, sr=hp.dsp.sample_rate, mono=True)
            target_length = len(x)
            x = torch.tensor(x).to('cpu')
            x = data.preprocess_inference_data(x,
                                            hp.inference.batched,
                                            hp.inference.batch_size,
                                            hp.inference.sequence_length,
                                            hp.dsp.sample_rate)

            with autocast(enabled=hp.training.mixed_precision):
                y = [model.inference(x_batch) for x_batch in x]
            y = data.postprocess_inference_data(y, hp.inference.batched, hp.dsp.sample_rate)
            y = y[:target_length].detach().cpu().numpy()
            sf.write(os.path.join(save_dir, f'{filename}_denoised.wav'), y.astype(np.float32),
                samplerate=hp.dsp.sample_rate)
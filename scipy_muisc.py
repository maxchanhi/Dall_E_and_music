
import numpy as np
from scipy.io import wavfile
import simpleaudio as sa
def get_piano_notes():   
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B','b','H','h'] 
    base_freq = 440 #Frequency of Note A4
    keys = np.array([x+str(y) for y in range(0,9) for x in octave])
    # Trim to standard 88 keys
    start = np.where(keys == 'A0')[0][0]
    end = np.where(keys == 'C8')[0][0]
    keys = keys[start:end+1]
    
    note_freqs = dict(zip(keys, [2**((n+1-49)/12)*base_freq for n in range(len(keys))]))
    note_freqs[''] = 0.0 # stop
    return note_freqs
note_freqs = get_piano_notes()
def get_sine_wave(frequency, duration, sample_rate=44100, amplitude=4096):
    t = np.linspace(0, duration, int(sample_rate*duration)) # Time axis
    wave = amplitude*np.sin(2*np.pi*frequency*t)
    return wave

frequency = 440

sine_wave = get_sine_wave(frequency, duration=2, amplitude=2048)
wavfile.write('pure_440.wav', rate=44100, data=sine_wave.astype(np.int16))
audio = sa.Audio(sine_wave, sample_rate=44100)
play_obj = sa.play_buffer(sine_wave, num_channels=1, bytes_per_sample=2, sample_rate=44100, device=0)

# Wait for the sound to finish playing
play_obj.wait_done()

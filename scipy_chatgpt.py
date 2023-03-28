import simpleaudio as sa
import numpy as np
import time 


def get_piano_notes():
    notes = []
    b_freq = 32.70
    for k in range(88):
        b_freq *= 2 ** (1 / 15)
        notes.append(b_freq)
    return notes

def get_sine_wave(frequency, duration, sample_rate=44100, amplitude=4096, num_overtones=0, overtone_decay=2.0, fade_in_duration=0.1, fade_out_duration=0.1):
    t = np.linspace(0, duration, int(sample_rate*duration)) # Time axis
    fundamental_wave = amplitude*np.sin(2*np.pi*frequency*t)

    if num_overtones > 0:
        overtones = np.zeros_like(fundamental_wave)
        for i in range(1, num_overtones+1):
            overtone_frequency = (i+1)*frequency
            overtone_amplitude = amplitude / (i+1)**overtone_decay
            overtone = overtone_amplitude*np.sin(2*np.pi*overtone_frequency*t)
            overtones += overtone
        wave = fundamental_wave + overtones
    else:
        wave = fundamental_wave
    
    fade_in_samples = int(fade_in_duration * sample_rate)
    fade_in = np.linspace(0, 1, fade_in_samples)
    wave[:fade_in_samples] *= fade_in
    
    fade_out_samples = int(fade_out_duration * sample_rate)
    fade_out = np.linspace(1, 0, fade_out_samples)
    wave[-fade_out_samples:] *= fade_out
    
    return wave

def map_rgb_to_key_number(value):
    notes = np.where(value > 87, value/3, value)
    return notes.astype(int)


def play_frequencies(freq_array):
    sample_rate = 44100
    for freq in freq_array:
        sine_wave = get_sine_wave(freq, duration=0.5, sample_rate=44100, amplitude = 2048*4, num_overtones=5, overtone_decay=2.0, fade_in_duration=0.1, fade_out_duration=0.1)
        play_obj = sa.play_buffer(sine_wave.astype(np.int16), 1, 2, sample_rate)
        play_obj.wait_done()
        time.sleep(0.5) # wait for 2 seconds before playing the next frequency

def play_frequencies_nonblocking(freq_array):
    sample_rate = 44100
    duration = 2
    amplitude = 2048*2
    num_overtones = 5
    overtone_decay = 3.0
    fade_out_duration = 0.2

    for freq in freq_array:
        sine_wave = get_sine_wave(freq, duration, sample_rate, amplitude, num_overtones, overtone_decay, fade_out_duration)
        play_obj = sa.play_buffer(sine_wave.astype(np.int16), 1, 2, sample_rate)
        while play_obj.is_playing():
            time.sleep(0.1)

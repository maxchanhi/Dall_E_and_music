import requests
from io import BytesIO
from PIL import Image
import numpy as np
import simpleaudio as sa
from scipy import signal
import streamlit as st
APIKEY= ''

DALLE_API_ENDPOINT = "https://api.openai.com/v1/images/generations"
def generate_image(prompt):
    # Define the request payload
    payload = {
        "model": "image-alpha-001",
        "prompt": prompt,
        "num_images": 1,
        "size": "256x256",
        "response_format": "url"
    }
    # Send the request to the DALL-E API endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {APIKEY}"
    }
    response = requests.post(DALLE_API_ENDPOINT, json=payload, headers=headers)
    response.raise_for_status()
    # Parse the response and decode the image
    image_url = response.json()["data"][0]["url"]
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    return image

def analyze_colors(image):
    # Convert the image to RGB mode if it's not already in RGB mode
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Get the dimensions of the image
    width, height = image.size
    
    # Get the RGB values for each pixel in the image
    pixels = image.load()
    colors = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            colors[y, x, :] = pixels[x, y]
    
    # Return the matrix of RGB values
    return colors
playback_object = None

def generate_sound(matrix, stop_event):
    global playback_object

    # Define some parameters
    sample_rate = 44100  # Samples per second
    duration = 5.0  # Seconds
    fade_time = 0.05  # Seconds
    nyq_rate = sample_rate / 2  # Nyquist frequency

    # Define a high-pass filter with a cutoff frequency of 3000 Hz
    b, a = signal.butter(4, 4000 / nyq_rate, btype="lowpass")

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if stop_event.is_set():
                return
            freq = matrix[i, j]
            # Convert the frequency to a sound signal
            num_samples = int(duration * sample_rate)
            fade_samples = int(fade_time * sample_rate)

            t = np.linspace(0, duration, num_samples, endpoint=False).reshape(-1, 1)
            f = np.array([freq * 4]).reshape(1, -1)
            signal_unfiltered = np.sin(2 * np.pi * f * t)
            signal_unfiltered = signal_unfiltered * np.ones((num_samples, 3))  # Broadcast signal to have shape (num_samples, 3)
            signal_unfiltered /= np.max(signal_unfiltered)  # Normalize the signal

            fade_shape = (fade_samples, 1)
            fade_in = np.linspace(0, 1, fade_samples).reshape(fade_shape)
            fade_out = np.linspace(1, 0, fade_samples).reshape(fade_shape)

            signal_unfiltered[:fade_samples] *= fade_in
            signal_unfiltered[-fade_samples:] *= fade_out

            # Apply the high-pass filter
            signal_filtered = signal.lfilter(b, a, signal_unfiltered.flatten(), axis=0)

            # Convert the filtered signal to bytes and play it
            signal_int = np.int16(signal_filtered * 32767)
            signal_bytes = signal_int.tobytes()
            playback_object = sa.play_buffer(signal_bytes, 1, 2, sample_rate)
    
    return playback_object  # Return the playback object after it has been assigned a value

def remove_ellipsis(matrix):
    # First, convert the matrix to a flattened array
    flattened = np.ravel(matrix)

    # Remove all slices and ellipsis
    flattened = flattened[flattened != np.newaxis]
    flattened = flattened[flattened != np.newaxis]

    # Reshape the array back into a matrix
    new_shape = [i for i in matrix.shape if i != 1]
    return flattened.reshape(*new_shape)

import streamlit as st
from functions import generate_image,analyze_colors,remove_ellipsis
from scipy_chatgpt import get_piano_notes,play_frequencies,map_rgb_to_key_number
import simpleaudio as sa
st.title("DALL-E Image Generation and Music V2")
stop_sound=st.button("Stop", key="s")
prompt_input = st.text_input("Enter a prompt about pollution:", key="widget_id")
if prompt_input:
    image = generate_image(prompt_input)
    st.image(image)
    colors = analyze_colors(image)
    freq_matrix = remove_ellipsis(colors)
    melody = []
    for i, row in enumerate(freq_matrix):
        for j, freq in enumerate(row):
            note = get_piano_notes()[map_rgb_to_key_number(row[j][0])]
            melody.append(note)
    play_frequencies(melody)
    
if stop_sound:
    melody = []
    sa.stop_all()

#65536
        


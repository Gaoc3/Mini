 
# # Define the decorator
# import asyncio
# from functools import wraps
# import posixpath
# import requests
# #_________________________________________________________________________________________________
# def auto_async_run(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         if asyncio.iscoroutinefunction(func):
#             return asyncio.run(func(*args, **kwargs))
#         else:
#             return func(*args, **kwargs)
#     return wrapper

# # Example of an async function
# @auto_async_run
# async def async_function():
#     await asyncio.sleep(1)
#     print("Async function executed")

# # Example of a normal function
# @auto_async_run
# def normal_function():
#     print("Normal function executed")

# # Test the functions
# async_function()
# normal_function()



# Initialize theme button state
import os
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.mention import mention
from streamlit import expander
from time import sleep
import json, yt_dlp, re
from dataYT import *
import random
import string
# دالة لتحميل الثيم الأخير المخزن
THEME_FILE = "theme.json"
""
# دالة لحفظ الثيم في ملف JSON
def save_theme(theme_name):
    with open(THEME_FILE, "w") as file:
        json.dump({"theme": theme_name}, file,indent=4)
        

def load_theme():
    try:
        with open(THEME_FILE, "r") as file:
            data = json.load(file)
            return data['theme']  
    except FileNotFoundError:
        return None
# دالة لتحميل CSS
@st.cache_data
def load_css(file_name="style.css"):
    with open(file_name) as f:
        css = f.read()
    return css

css = load_css()
ms = st.session_state
def extract_video_id(url):
    pattern = r'(?:youtu\.be/|(?:www\.|m\.)?youtube\.com/watch\?v=)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None
# التحقق من وجود "themes" في session state
if "themes" not in ms:

    last_theme = load_theme() if load_theme is not None else 'light'
    ms.themes = {
        "current_theme": last_theme,
        "refreshed": True,
        "light": {
                "theme.base": "light",
                "theme.backgroundColor": "#E0E0E0",
                "theme.primaryColor": "#ec1919",
                "theme.secondaryBackgroundColor": "#cdcfe0",
                "theme.textColor": "#0a1464",
                  
                 },
        "dark":  {
                "theme.base": "dark",
                "theme.backgroundColor": "#141444",
                "theme.primaryColor": "#1D1DEB",
                "theme.secondaryBackgroundColor": "#04112D",
                "theme.textColor": "#F7E1E1",
                  
                 },
    }

# تطبيق الثيم المخزن عند بدء التطبيق
def apply_theme():
    current_theme_dict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
    for vkey, vval in current_theme_dict.items():
        st._config.set_option(vkey, vval)

apply_theme()  # تطبيق الثيم عند بدء التطبيق



def ChangeTheme():
    previous_theme = ms.themes["current_theme"]
    if previous_theme == "dark":
        ms.themes["current_theme"] = "light"
    else:
        ms.themes["current_theme"] = "dark"
        
    apply_theme()
    
    save_theme(ms.themes["current_theme"])
    
    ms.themes["refreshed"] = False
with stylable_container(
        css_styles=load_css(),
        key="button",
    ):
    st.button(label='', on_click=ChangeTheme, type="primary")
st.title('YT Downloader')  
with st.form(key='form_submit'):
  input_txt = st.text_input(label="url input",placeholder="Enter a url to download from it.",label_visibility="hidden")
  search = st.form_submit_button('search',use_container_width=True,type='primary')
if search:
    video_id = extract_video_id(input_txt)
    st.session_state.video_id = video_id
    with st.spinner('Loading...'):
      sleep(2)
    info = send_request(video_id,360)
    st.image(info['info']['image'],caption=info['title'],use_column_width='always',output_format='auto')
    resolutions = extract_quality(get_res(video_id))
    keys = {}
    for res in resolutions:
      print(res)
      req_id = send_request(video_id,res)['id']
      progress = get_progress(req_id)
      
      while True:
        progress = get_progress(req_id)
        if progress['text'] == 'Finished':
          url = get_progress(req_id)['download_url']
          byte = get_bytes(url)
          key = ''.join(random.sample(string.ascii_letters + string.digits, k=5))
          keys[f'{key}_{res}'] = byte
          break
    for key, byte in keys.items():
      with expander(f'{res}p'):
        res = key.split('_')[1]
        key = key.split('_')[0]
        st.download_button(label='Download',data=byte,file_name=f"{info['title']}.mp4",mime="application/octet-stream",use_container_width=True,key=key,type='primary')

      
      
      

    
# st.json(ms.themes)
if ms.themes["refreshed"] == False:
    ms.themes["refreshed"] = True
    st.rerun()
with open('element.html','r')as ht:
    components.html(ht.read())

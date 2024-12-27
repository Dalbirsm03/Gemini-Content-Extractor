import PIL
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
from PIL import Image
import os
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
prompt = ''' as an expert in transcripting youtube videos , give a accurate summary of urls which is provided . the summary hsould be in 200 to 300 words . A expert like you is required for this task '''
def is_youtube_link(text):
  if ("youtube.com" in text.lower()) or ("youtu.be" in text.lower()):
    if ("watch?v=" in text.lower()):
      return True
  else:
    return False

# For extracting Transcribe
def extract_transcribe_text(youtube_video_url):
    try:    
        video_id = youtube_video_url.split("=")[1]
        transcrpit_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = '' # Append from list to paragraph
        for i in transcrpit_text:
            transcript += " " + i['text']
        return transcript
    except Exception as e:
        raise e

def generate_gemini_transcribe(transcrpit_text , prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt+transcrpit_text)
    return response.text


# Text and Image input
def get_gemini_response(input, image):
  model = genai.GenerativeModel('gemini-1.5-flash')
  if input != "" and image is not None:
    response = model.generate_content([input, image])
  elif image is not None:
    response = model.generate_content(image)
  elif input != "": 
    response = model.generate_content(input)
  return response.text

st.title("GEMINI APP")

user_input = st.text_input("Enter Text or Youtube Link")
upload_file = st.file_uploader("Upload an Image (Optional)", type=["jpg", "png", "jpeg"])
submit = st.button("Enter")
if submit:
  if is_youtube_link(user_input):
    transcript_text = extract_transcribe_text(user_input)
    if transcript_text:
        summary=generate_gemini_transcribe(transcript_text,prompt)
        st.markdown("Detailed Notes:")
        st.write(summary)
  else:
    if upload_file is not None:
      image = Image.open(upload_file)
    else:
      image = None
    response = get_gemini_response(user_input, image)
    st.subheader('The Response is ...')
    st.write(response)
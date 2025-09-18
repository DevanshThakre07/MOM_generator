import google.generativeai as genai
import os
# import cv2
from PIL import Image
import streamlit as st
from pdfextractor import text_extractor_pdf
from docxextractor import text_extractor_docx
from imageextractor import img_extractor
st.sidebar.title(':orange[upload you mom notes here: ]')
st.sidebar.subheader('Only upload images,pdf and docs ')
user_file = st.sidebar.file_uploader('Upload here',type = ['pdf','docx','png','jpg','jpeg'])
if user_file:
    if user_file.type == 'application/pdf':
        user_text = text_extractor_pdf(user_file)
    elif user_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        user_text= text_extractor_docx(user_file)
    elif user_file.type in ['image/jpg','image/jpeg','image/png']:
        user_text= img_extractor(user_file)
    else:
        st.write('Upload correct file format')
# if user_file:
#     st.header(':blue[Your result]')
#     st.write(user_text)

st.title(':green[Minutes of Meeting]: AI assisted MOM generator is a standardized for from meeting notes')
tips = '''Tips to use this app:
* Upload your meeting in side bar (img, pdf or docx)
* Click on generate MOM and get the standardized MOM's'''
st.write(tips)

if st.button('Generate MoM'):
  if user_text is None:
    st.error('Text is not generated')

  else:
    with st.spinner('Processing your dara...'):
       prompt = f'''Assume you are expert in creating Minutes of meeting, user has privided notes of a meeting in text format.
    using this data you need to create a standardized minutes of meeting for the user. 

    keep the format strictly as mentioned below.
    output must follow world/docx format, strictly 
    title : Title of Meeting
    Heading : Meeting Agenda
    Subheading : Name of Attendees (if attendees name is not there keep it NA)
    subheading : date of meeting and place of meeting(pplace means name of conference room if not provided keep t online )
    Body : the body must follow the following sequence of points.
    * Key points discussed
    * highlight any decision that has finalized
    * mention actionable items
    * any additional notes.
    * any deadline that has been discussed
    * any next meeting date that has been discussed.
    * 2-3 lines of summary
    * use bullet points and highlight or bold the keywords such that context is clear.


    the data provided by user is as follows{user_text}
    '''
    key = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    response = model.generate_content(prompt)
    output = response.text
    st.write(output)

    st.download_button(label='click to downlode',data=response.text,file_name='MoM.txt',
                       mime='text/plain')
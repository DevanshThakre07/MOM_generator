import google.generativeai as genai
import os
import cv2
from PIL import Image
import numpy as np

def img_extractor(img_path):
    file_by = np.asarray(bytearray(img_path.read()),dtype=np.uint8)
    image = cv2.imdecode(file_by,cv2.IMREAD_COLOR)
    # image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # to convert to RGB 
    image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # to grey
    _,image_bw = cv2.threshold(image_grey, 150,255, cv2.THRESH_BINARY) # to convert to black and white
    final_img = Image.fromarray(image_bw)

    key = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    prompt = ''' You act as an OCR application on the given image and text and extract the text 
    from it. give only the text as output, do not give any other explanation or description.

    '''

    response = model.generate_content([prompt,final_img])
    output = response.text
    return output
import os
import json
import google.generativeai as genai

# getting the working dir
working_dir = os.path.dirname(os.path.abspath(__file__))


config_file_path = f"{working_dir}/config.json"
config_data = json.load(open(config_file_path))

# loading api key
# GOOGLE_API_KEY = config_data['GOOGLE_API_KEY']
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
print(GOOGLE_API_KEY)

# config
genai.configure(api_key=GOOGLE_API_KEY,transport='rest')

# load gemini pro model
def load_gemini_pro_model():
    gemini_pro_model =genai.GenerativeModel('gemini-pro')
    return gemini_pro_model

# image captioning
def gemini_pro_vision_res(prompt, image):
    gemini_pro_vision_model = genai.GenerativeModel('gemini-pro-vision')
    res = gemini_pro_vision_model.generate_content([prompt, image])
    result   = res.text
    return result

# embed text
def embedding_model_res(input_text: str):
    embedding_model = "models/embedding-001"
    embedding = genai.embed_content(model=embedding_model, content=input_text, task_type='retrieval_document')

    embedding_list = embedding['embedding']
    return embedding_list

# function to get a response from gemini pro
def gemini_pro_res(prompt):
    gemini_pro_model = load_gemini_pro_model()
    res = gemini_pro_model.generate_content(prompt)
    result  = res.text
    return result
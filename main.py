import os
import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utils import load_gemini_pro_model, gemini_pro_vision_res,embedding_model_res, gemini_pro_res
from PIL import Image

# get the current working dir
working_dir  = os.path.dirname(os.path.abspath(__file__))
print(working_dir)

# page config
st.set_page_config(
    page_title="Gemini AI",
    page_icon="✨",
    layout="centered",
)

# using boostrap icons
with st.sidebar:
    selected = option_menu("Gemini AI", ["ChatBot", "Image Captioning", "Embede Text", "Ask me anything"], menu_icon="robot", icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'], default_index=0)


# translate role b/w streamlit and gemini-pro
def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return 'assistant'
    else : 
        return user_role

if selected == "ChatBot":
    model =  load_gemini_pro_model();

    # initialize chat sessions in streamlit if not already
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
    
    # page title
    st.title("🤖 ChatBot")

    # display th chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    
    # input field
    user_prompt = st.chat_input("Ask Gemini Pro...")
    if user_prompt:
        # display the user prompt
        st.chat_message("user").markdown(user_prompt)

        # send the user prompt to the model
        gemini_res = st.session_state.chat_session.send_message(user_prompt)

        # display the response
        with st.chat_message('assistant'):
            st.markdown(gemini_res.text)

# image captioning
if selected == "Image Captioning":
    st.title("📸 Image Captioning")
    image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if st.button("Generate Caption"):
        image_ = Image.open(image)
        col1, col2 = st.columns(2)
        with col1:
            resizeImage = image_.resize((800, 500))
            st.image(resizeImage)
        default_prompt = "write a short description of the image"

        # getting response from gemini pro
        caption = gemini_pro_vision_res(default_prompt, image_)

        with col2:
            st.write(caption)

# text embedding
if selected == "Embede Text":
    st.title("🔠 Embed Text")
    input_text = st.text_area(label="", placeholder="Enter the text to embed")

    if st.button("Get Embeddings"):
        # getting response from gemini pro
        embedding = embedding_model_res(input_text)
        st.markdown(embedding)


# ask me anything
if selected == "Ask me anything":
    st.title("🤔 Ask me anything")
    st.write("I am Gemini AI, ask me anything")

    user_prompt = st.text_input("Ask me anything")
    if st.button("Ask"):
        # getting response from gemini pro
        gemini_res = gemini_pro_res(user_prompt)
        st.markdown(gemini_res)
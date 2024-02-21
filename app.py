import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html
import integration as ing
import text_generation as tg
# import test2 as tg
import image_searcher as imgsearch
import reports_detector as rd
from PIL import Image
import os


current_dir = os.getcwd()
folder_path = os.path.join(current_dir,"data")


def initialize_session_state():
    """
    Session State is a way to share variables between reruns, for each user session.
    """

    # st.session_state.setdefault('history', [])
    st.session_state.setdefault('generated', {"data":["Hello Doc! I am here to answers the questions from provided patient reports"],"result_images":[False]})
    st.session_state.setdefault('past', [""])

def display_chat(query_engine,uploaded_files):
    """
    Streamlit related code it creates two containers
    container: To group our chat input form
    reply_container: To group the generated chat response
    """
    #In Streamlit, a container is an invisible element that can hold multiple elements together. 
    #The st.container function allows you to group multiple elements together. 
    #For example, you can use a container to insert multiple elements into your app out of order.
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='chat_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="Ask me questions from uploaded PDFs or Search for Report Images", key='input')
            submit_button = st.form_submit_button(label='Send ⬆️')
        
        #Check if user submit question with user input and generate response of the question
        if submit_button and user_input:
            generate_response(user_input=user_input, query_engine=query_engine, uploaded_files=uploaded_files)
    
    #Display generated response to streamlit web UI
    display_generated_responses(reply_container)


def generate_response(user_input, query_engine, uploaded_files):

    """
    Generate LLM response based on the user question by retrieving data from Vector Database
    Also, stores information to streamlit session states 'past' and 'generated' so that it can
    have memory of previous generation for converstational type of chats (Like chatGPT)
    """

    with st.spinner('Analysing the reports...'):
        prompt_type = ing.identify_prompt_type(user_input)
        if prompt_type=="text":
            response=tg.text_generator(query_engine=query_engine,query=user_input)
            result_images=False
            # history.append((user_input, response))
            st.session_state['past'].append(user_input)
            st.session_state['generated']['data'].append(response)
            st.session_state['generated']['result_images'].append(result_images)
            print(response)

        elif prompt_type=="image":
            resultant_images = imgsearch.image_searcher(user_input,uploaded_files=uploaded_files)
            result_images=True
            st.session_state['past'].append(user_input)
            st.session_state['generated']['data'].append(resultant_images)
            st.session_state['generated']['result_images'].append(result_images)



def display_generated_responses(reply_container):
    """
    Display generated LLM response to Streamlit Web UI

    Args:
    - reply_container: Streamlit container created at previous step
    """
    print(st.session_state['generated'])
    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated']['data'])):
                if i!=0:
                    message(st.session_state["past"][i], is_user=True, key=f"{i}_user", logo="https://openmoji.org/data/color/svg/1F468-1F3FB-200D-2695-FE0F.svg")

                print(st.session_state['generated']['data'][i])
                if st.session_state['generated']['result_images'][i] is True:
                    #message(st.session_state["generated"]['data'][i], key=str(i), allow_html=True, avatar_style="bottts")
                    print("-----------------------")
                    for img_path in st.session_state['generated']['data'][i]:
                        # img=Image.open(img_path)
                        st.image(img_path, caption='Report image', width=200, use_column_width=True)
                else:
                    message(st.session_state["generated"]['data'][i], key=str(i), allow_html=True, logo="https://openmoji.org/data/color/svg/1F916.svg")



def DocAgent_Bot(uploaded_files):
    """
    First function to call when we start streamlit app
    """
    rd.download_files(folder_path=folder_path,uploaded_reports=uploaded_files)

    # Step 1: Initialize session state
    initialize_session_state()

    #Step-2 Create embeddings for text report data
    query_engine = tg.create_storage_embeddings()

    
    st.markdown("<h4 style='text-align:center'>I'm ready to Answer!!!</h4>", unsafe_allow_html=True)
    image = Image.open('DocAgentIMG.jpg')
    st.image(image, width=150)
    
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>

            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


    #Step 3 - Display Chat to Web UI
    display_chat(query_engine,uploaded_files=uploaded_files)


def main():
    st.set_page_config(page_title="File Upload Page")
    
    uploaded_files = None

    # Initialize session state
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = None
    
    #Displays app title
    st.title("🩺DocAgent!")
    

    image = Image.open('doc1.png')
    title_container = st.empty()
    title_container.image(image, width=250)
    title_container.markdown("<h4>Upload Report Files📂</h4>", unsafe_allow_html=True)
    uploaded_files = rd.file_upload_page()
    

    print("files",uploaded_files)
    
    # Update session state with uploaded file
    if uploaded_files is not None and len(uploaded_files)!=0:
        title_container.markdown("<h3>🔄Uploading files and creating embeddings...</h3>", unsafe_allow_html=True)      
        st.session_state.uploaded_files = uploaded_files
        DocAgent_Bot(st.session_state.uploaded_files)
        title_container.empty()


if __name__ == "__main__":
    main()
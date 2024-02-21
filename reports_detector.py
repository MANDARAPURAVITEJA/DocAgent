import os
import streamlit as st



supported_formats = ['pdf','docx','xlsx','txt']

def file_upload_page():

    uploaded_files = st.file_uploader("...",accept_multiple_files=True, type=["jpg", "jpeg", "png","pdf","docx","txt"])
    return uploaded_files


def check_file_format(uploaded_file, allowed_formats):
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]
        if file_extension.lower() in allowed_formats:
            return True
        else:
            return False
    else:
        return False



def download_files(folder_path, uploaded_reports):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # If the folder exists, remove all existing files
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                # Remove the file
                os.remove(file_path)
            except Exception as e:
                print(f"Error: {e}")

    else:
        # If the folder does not exist, create the folder
        os.makedirs(folder_path)

    # Download the new files into the folder
    for filename in uploaded_reports:
        # filename = os.path.basename(url)
        # file_path = os.path.join(folder_path, filename)
        is_docfile = check_file_format(filename,supported_formats)
        try:
            if is_docfile:
                # Download the file
                # response = requests.get(filename);print("response:",response)
                with open(os.path.join(folder_path, filename.name), 'wb') as f:
                    f.write(filename.getbuffer())
                print(f"Downloaded: {filename}")

        except Exception as e:
            print(f"Error downloading {filename}: {e}")



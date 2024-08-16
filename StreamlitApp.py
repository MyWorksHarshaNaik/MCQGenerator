import pandas as pd
import os
import json
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
import streamlit as st
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain

# Load the JSON Response
with open("D:\GenerativeAI\MCQGenerator\Response.json", "r") as f:
    response_json = json.load(f)

# Title of the Web App
st.title("MCQ Generator using Gen AI 🤖")

# Creating a Form
with st.form("user_inputs"):

    # File Uploader
    uploaded_file = st.file_uploader("Choose a file containing a description of your topic (.txt or .pdf): ")

    # Input Fields
    question_count = st.number_input("Number of Questions", min_value=3, value=50)
    subject = st.text_input("Insert Subject Title")
    tone = st.text_input("Complexity Level: ", placeholder="Simple")
    button = st.form_submit_button("Generate MCQs")

    if button and uploaded_file is not None and question_count and subject and tone:
        with st.spinner("Loading... "):
            try:
                data = read_file(uploaded_file)
                response = generate_evaluate_chain(
                    {"text": data, "number": question_count, "subject": subject, "tone": tone, "response_json": response_json})

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("An error occurred. Please try again.")
            else:
                if isinstance(response, dict):
                    quiz = response.get("quiz")
                    quiz = quiz.split('\n', 1)[1]
                    quiz = quiz.replace("'", "\"")
                    # quiz = json.loads(quiz)

                    table_data = get_table_data(quiz)
                    if table_data is not None:
                        df = pd.DataFrame(table_data)
                        df.index = df.index + 1
                        st.table(df)
                        # st.text_area(label="Generated MCQs", value=quiz)
                        st.text_area(label="Review",
                                     value=response.get("review"))

                    else:
                        st.error("Error in Table Data")
                else:
                    st.write(response)
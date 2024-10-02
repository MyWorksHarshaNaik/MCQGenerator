import pandas as pd
import json
import traceback
import streamlit as st
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain

# Load the JSON Response
# response_path = "D:\\GenAI\\MCQGenerator\\Response.json"
response_path = "D:\\GenAI\\MCQGenerator\\Response.json"
try:
    with open(response_path, "r") as f:
        response_json = json.load(f)
except FileNotFoundError:
    st.error(f"Response JSON file not found at {response_path}.")
    response_json = {}
except json.JSONDecodeError:
    st.error(f"Error decoding JSON from file {response_path}.")
    response_json = {}

# Title of the Web App
st.title("MCQ Generator using Gen AI 🤖")

# Convert DataFrame to CSV
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# Creating a Form
with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Choose a file containing a description of your topic (.txt or .pdf):")
    question_count = st.number_input("Number of Questions", min_value=3, value=50)
    subject = st.text_input("Insert Subject Title")
    tone = st.text_input("Complexity Level:", placeholder="Simple")
    button = st.form_submit_button("Generate MCQs")

if button:
    if uploaded_file is None:
        st.error("Please upload a file.")
    elif not subject:
        st.error("Please provide a subject title.")
    elif not tone:
        st.error("Please specify the complexity level.")
    else:
        with st.spinner("Generating MCQs..."):
            try:
                data = read_file(uploaded_file)
                response = generate_evaluate_chain(
                    {"text": data, "number": question_count, "subject": subject, "tone": tone, "response_json": response_json})

                if isinstance(response, dict):
                    quiz = response.get("quiz")
                    if quiz:
                        quiz = quiz.split('\n', 1)[1] if '\n' in quiz else quiz
                        quiz = quiz.replace("'", "\"")

                        table_data = get_table_data(quiz)
                        if table_data:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.session_state.df = df  # Store DataFrame in session state
                            st.session_state.quiz_review = response.get("review", "No review available.")
                            st.table(df)
                        else:
                            st.error("Error in processing table data.")
                    else:
                        st.error("No quiz data found in response.")
                else:
                    st.error("Invalid response format.")
            except Exception as e:
                logging.error("An error occurred while generating MCQs.", exc_info=True)
                st.error("An error occurred. Please try again.")

# Display download button outside the form
if 'df' in st.session_state:
    csv = convert_df(st.session_state.df)
    st.download_button("Download MCQs", csv, "MCQs.csv", "text/csv", key='download-csv')
    st.text_area(label="Review", value=st.session_state.quiz_review)

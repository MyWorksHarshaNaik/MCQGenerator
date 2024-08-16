import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file, get_table_data

# langchain packages
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

# load the environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Defining LLM Model
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GEMINI_API_KEY)

# Defining the Prompt Template and the Chain for the Quiz Generation
TEMPLATE = """
Text : {text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs
###RESPONSE JSON
{response_json}"

"""

quiz_prompt = PromptTemplate(template=TEMPLATE, input_variables=[
                             "text", "number", "subject", "tone", "response_json"])

quiz_chain = LLMChain(llm=llm, prompt=quiz_prompt,
                      output_key="quiz", verbose=True)

# Defining the Prompt Template and the Chain for the Quiz Evaluation
TEMPLATE2 = """
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

evaluation_prompt = PromptTemplate(
    template=TEMPLATE2, input_variables=["subject", "quiz"])


review_chain = LLMChain(llm=llm, prompt=evaluation_prompt,
                        output_key="review", verbose=True)

# Defining the Sequential Chain for Quiz Generation and Evaluation
generate_evaluate_chain = SequentialChain(chains=[quiz_chain, review_chain], input_variables=[
    "text", "number", "subject", "tone", "response_json"], output_variables=["quiz", "review"], verbose=True)
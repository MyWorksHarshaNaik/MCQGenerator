import os
import PyPDF2
import json
import traceback


def read_file(file):

    filename = file.name
    if filename.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in range(pdf_reader.numPages):
                text += page.extract_text()
                return text

        except Exception as e:
            raise Exception(f"Error reading the PDF file")

    elif filename.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        raise Exception(f"File format not supported. Provide PDF or TXT file")


def get_table_data(quiz_str):
    try:
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        for key, value in quiz_dict.items():
            mcq = value["MCQ"]
            options = " || ".join(
                [
                    f"{option} -> {option_value}" for option, option_value in value["Options"].items()
                ])

            correct = value["Correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
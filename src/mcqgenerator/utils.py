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
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extract_text()
            return text

        except Exception as e:
            raise Exception(f"Error reading the PDF file: {e}")

    elif filename.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        raise Exception(f"File format not supported. Provide PDF or TXT file")


# def get_table_data(quiz_str):
#     try:
#         quiz_dict = json.loads(quiz_str)
#         quiz_table_data = []
#         for key, value in quiz_dict.items():
#             mcq = value["MCQ"]
#             options = " || ".join(
#                 [f"{option} -> {option_value}" for option, option_value in value["Options"].items()]
#             )
#             correct = value["Correct"]
#             quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

#         return quiz_table_data

#     except json.JSONDecodeError as e:
#         print(f"JSONDecodeError: {e}")
#         traceback.print_exception(type(e), e, e.__traceback__)
#         return False
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         traceback.print_exception(type(e), e, e.__traceback__)
#         return False

def get_table_data(quiz_str):
    try:
        print(quiz_str)  # Debugging step
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        for key, value in quiz_dict.items():
            mcq = value["MCQ"]
            options = " || ".join(
                [f"{option} -> {option_value}" for option, option_value in value["Options"].items()]
            )
            correct = value["Correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exception(type(e), e, e.__traceback__)
        return False

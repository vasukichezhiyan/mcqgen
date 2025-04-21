import os
import json
import PyPDF2
import traceback
import streamlit as st

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        
        except Exception as e:
            raise Exception("error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read.decode("utf-8")
    
    else:
        raise Exception("unsupported file format only pdf and text file supported")
    
def get_review_table_data(str):
    try:
        review_quiz=json.loads(str)
        review_quiz_table_data=[]

        for key, value in review_quiz.items():
            mcq=value["mcq"]
            options=" || ".join(
                [
                    f"{option}-> {option_value}" for option, option_value in value["options"].items()
                ]
            )
            correct=value["correct"]
            review_quiz_table_data.append({"Question": mcq,"Correct Answer": correct})
        return review_quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e),e,e._traceback_)
        return False

    
def get_table_data(quiz_str):
    try:
        quiz_dict=json.loads(quiz_str)
        quiz_table_data=[]

        for key, value in quiz_dict.items():
            mcq=value["mcq"]
            options='\n'.join(
                [
                    f"{option}-> {option_value}" for option, option_value in value["options"].items()

                ]
            )
            correct=value["correct"]
            quiz_table_data.append({"Question": mcq,"Choices": options})

        return quiz_table_data  


    except Exception as e:
        traceback.print_exception(type(e),e,e._traceback_)
        return False

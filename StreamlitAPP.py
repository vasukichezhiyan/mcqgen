import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data,get_review_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from langchain_community.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

with open('C:\BlueStar\skillassessment_bluestar\Response.json','r') as file:
    RESPONSE_JSON = json.load(file)

st.title("Self Skill Assessment")

with st.form("user_inputs"):    
    
    uploaded_file=st.file_uploader("upload a pdf or text file")    

    subject=st.text_input("Insert Subject",max_chars=20)

    tone=st.text_input("Complexity Level of Questions", max_chars=20 , placeholder="Simple")

    mcq_count=st.number_input("No. of MCQs", min_value=3, max_value=50)

    button=st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try: 
                text=read_file(uploaded_file)
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")

            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Promopt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total cost:{cb.total_cost}")
                if isinstance(response, dict):
                    quiz=response.get("quiz", None)
                    review=response.get("review", None)
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                        else:
                           st.error("Error in the table data")
                    
                else:
                    st.write(response)
                 
    approve_button = st.form_submit_button(label='Show Answer')

if approve_button:
        try: 
            text=read_file(uploaded_file)
            with get_openai_callback() as cb:
                response=generate_evaluate_chain(
                    {
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                    }
                )
        except Exception as e:
            traceback.print_exception(type(e),e,e.__traceback__)
            st.error("Error")

        else:
            print(f"Total Tokens:{cb.total_tokens}")
            print(f"Promopt Tokens:{cb.prompt_tokens}")
            print(f"Completion Tokens:{cb.completion_tokens}")
            print(f"Total cost:{cb.total_cost}")
            if isinstance(response, dict):
                quiz=response.get("quiz", None)
                if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                        else:
                           st.error("Error in the table data")

                if quiz is not None:
                    table_data=get_review_table_data(quiz)
                    if table_data is not None:
                        df=pd.DataFrame(table_data)
                        df.index=df.index+1
                        st.table(df)
                    else:
                        st.error("Error in the table data")
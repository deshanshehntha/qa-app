# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 12:28:10 2024

@author: dswdfb
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import sys
from io import StringIO
import contextlib

# Define a dictionary of questions and answers
qa_dict = {
    "What is Streamlit?": "Streamlit is an open-source Python library used for creating web applications for data science and machine learning projects.",
    "How do you install Streamlit?": "You can install Streamlit using pip: 'pip install streamlit'",
    "What are some advantages of using Streamlit?": "Streamlit offers easy-to-use API, fast prototyping, and simple deployment options.",
    "Can Streamlit handle data visualization?": "Yes, Streamlit integrates well with data visualization libraries like Matplotlib and Plotly."
}

def get_answer(question):
    return qa_dict.get(question, "I'm sorry, I don't have an answer to that question.")

# Define the Streamlit app
def streamlit_app():
    st.title("Simple Q&A App")

    # Create an input field for the user's question
    user_question = st.text_input("Ask a question:")

    # Create a button to submit the question
    if st.button("Get Answer"):
        if user_question:
            answer = get_answer(user_question)
            st.write("Answer:", answer)
        else:
            st.write("Please enter a question.")

    # Display the list of available questions
    st.sidebar.header("Available Questions")
    for question in qa_dict.keys():
        st.sidebar.write(f"- {question}")

# Run the Streamlit app
if __name__ == "__main__":
    # Redirect stdout to capture Streamlit's output
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    # Run the Streamlit app
    with contextlib.redirect_stdout(StringIO()):
        streamlit_app()
    
    # Get the Streamlit app's output
    output = sys.stdout.getvalue()
    
    # Restore stdout
    sys.stdout = old_stdout
    
    # Print the output
    print(output)

# Run the Streamlit app
streamlit_app()

import streamlit as st

# Define a dictionary of questions and answers
qa_dict = {
    "What is Streamlit?": "Streamlit is an open-source Python library used for creating web applications for data science and machine learning projects.",
    "How do you install Streamlit?": "You can install Streamlit using pip: 'pip install streamlit'",
    "What are some advantages of using Streamlit?": "Streamlit offers easy-to-use API, fast prototyping, and simple deployment options.",
    "Can Streamlit handle data visualization?": "Yes, Streamlit integrates well with data visualization libraries like Matplotlib and Plotly."
}

def get_answer(question):
    return qa_dict.get(question, "I'm sorry, I don't have an answer to that question.")

def streamlit_app():
    st.title("Simple Q&A App")

    # Create an input field for the user's question
    user_question = st.text_input("Ask a question:", key="user_question_input")

    # Create a button to submit the question
    if st.button("Get Answer", key="get_answer_button"):
        if user_question:
            answer = get_answer(user_question)
            st.write("Answer:", answer)
        else:
            st.write("Please enter a question.")

    # Display the list of available questions
    st.sidebar.header("Available Questions")
    for i, question in enumerate(qa_dict.keys()):
        st.sidebar.write(f"- {question}", key=f"question_{i}")

if __name__ == "__main__":
    streamlit_app()

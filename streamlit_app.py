import streamlit as st
import pandas as pd

# Define a dictionary of questions and multiple answers
qa_dict = {
    "What is the best way to learn programming?": [
        "Practice coding every day",
        "Take online courses",
        "Read programming books",
        "Work on real-world projects"
    ],
    "How can I improve my problem-solving skills?": [
        "Solve puzzles and brain teasers",
        "Practice algorithmic problems",
        "Analyze and break down complex issues",
        "Collaborate with others on challenging tasks"
    ]
}

# Define the 11 criteria for rating
criteria = [
    "Clarity", "Relevance", "Accuracy", "Completeness", "Practicality",
    "Creativity", "Efficiency", "Scalability", "Accessibility", "Novelty", "Overall Impact"
]

def streamlit_app():
    st.title("Q&A Evaluation App")

    # Initialize session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = list(qa_dict.keys())[0]
    if 'current_answer_index' not in st.session_state:
        st.session_state.current_answer_index = 0
    if 'ratings' not in st.session_state:
        st.session_state.ratings = {q: pd.DataFrame(0, index=answers, columns=criteria) for q, answers in qa_dict.items()}

    # Select a question
    question = st.selectbox("Choose a question:", list(qa_dict.keys()), key="question_select")
    
    # Update current question if changed
    if question != st.session_state.current_question:
        st.session_state.current_question = question
        st.session_state.current_answer_index = 0

    # Display the question and current answer
    st.write(f"**Question:** {question}")
    answers = qa_dict[question]
    current_answer = answers[st.session_state.current_answer_index]
    st.write(f"\n**Answer {st.session_state.current_answer_index + 1} of {len(answers)}:** {current_answer}")

    # Display rating sliders for the current answer
    st.write("\n**Rate this answer:**")
    for criterion in criteria:
        st.session_state.ratings[question].at[current_answer, criterion] = st.slider(
            criterion,
            0, 10, 
            int(st.session_state.ratings[question].at[current_answer, criterion]),
            key=f"slider_{criterion}"
        )

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous Answer", disabled=st.session_state.current_answer_index == 0):
            st.session_state.current_answer_index -= 1
            st.rerun()
    with col2:
        if st.button("Next Answer", disabled=st.session_state.current_answer_index == len(answers) - 1):
            st.session_state.current_answer_index += 1
            st.rerun()

    # Button to calculate and display results
    if st.button("Show Results", key="show_results_button"):
        st.write("\n**Ratings Summary:**")
        st.dataframe(st.session_state.ratings[question])

        # Calculate and display the average rating for each answer
        average_ratings = st.session_state.ratings[question].mean(axis=1)
        st.write("\n**Average Ratings:**")
        st.dataframe(average_ratings)

        # Identify the best answer based on average rating
        best_answer = average_ratings.idxmax()
        st.write(f"\n**Best Answer:** {best_answer}")
        st.write(f"**Average Rating:** {average_ratings[best_answer]:.2f}")

if __name__ == "__main__":
    streamlit_app()

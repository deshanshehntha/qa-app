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

    # Select a question
    question = st.selectbox("Choose a question:", list(qa_dict.keys()), key="question_select")

    # Display the question and answers
    st.write(f"**Question:** {question}")
    
    # Create a dataframe to store ratings
    ratings_df = pd.DataFrame(0, index=qa_dict[question], columns=criteria)

    # Display answers and rating sliders
    for i, answer in enumerate(qa_dict[question]):
        st.write(f"\n**Answer {i+1}:** {answer}")
        
        # Create columns for criteria to save space
        cols = st.columns(3)
        for j, criterion in enumerate(criteria):
            ratings_df.at[answer, criterion] = cols[j % 3].slider(
                f"{criterion} for Answer {i+1}",
                0, 10, 5,
                key=f"slider_{i}_{j}"
            )

    # Button to calculate and display results
    if st.button("Calculate Ratings", key="calculate_button"):
        st.write("\n**Ratings Summary:**")
        st.dataframe(ratings_df)

        # Calculate and display the average rating for each answer
        average_ratings = ratings_df.mean(axis=1)
        st.write("\n**Average Ratings:**")
        st.dataframe(average_ratings)

        # Identify the best answer based on average rating
        best_answer = average_ratings.idxmax()
        st.write(f"\n**Best Answer:** {best_answer}")
        st.write(f"**Average Rating:** {average_ratings[best_answer]:.2f}")

if __name__ == "__main__":
    streamlit_app()

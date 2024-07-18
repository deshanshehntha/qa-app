import streamlit as st
import pandas as pd

# Set page configuration to wide mode
st.set_page_config(layout="wide")

# Define a dictionary of questions and more substantial answers
qa_dict = {
    "What are the key principles of effective project management?": [
        """Effective project management relies on several key principles. First, clear communication is essential to ensure all team members are aligned on goals and expectations. Second, careful planning and organization help to break down complex projects into manageable tasks. Third, risk management strategies should be implemented to anticipate and mitigate potential issues. Fourth, regular monitoring and control of project progress allow for timely adjustments. Lastly, strong leadership is crucial to guide the team and maintain motivation throughout the project lifecycle.""",
        """Successful project management hinges on a few core principles. To begin with, establishing SMART (Specific, Measurable, Achievable, Relevant, Time-bound) objectives provides a clear direction for the project. Next, fostering a collaborative team environment encourages innovation and problem-solving. Additionally, implementing agile methodologies allows for flexibility and adaptability in the face of changing requirements. Furthermore, effective resource allocation ensures optimal use of time, budget, and personnel. Finally, conducting thorough post-project evaluations facilitates continuous improvement for future endeavors.""",
        """Key principles of effective project management include several important factors. Primarily, stakeholder engagement throughout the project lifecycle ensures buy-in and support. Moreover, utilizing appropriate project management tools and software can streamline processes and improve efficiency. Another crucial aspect is maintaining comprehensive documentation for transparency and future reference. Additionally, implementing a robust change management process helps control scope creep and manage expectations. Lastly, prioritizing quality assurance at every stage safeguards the project's overall success and deliverables."""
    ],
    "How can artificial intelligence be ethically implemented in healthcare?": [
        """Ethical implementation of AI in healthcare requires careful consideration of several factors. Firstly, ensuring patient privacy and data security is paramount when handling sensitive medical information. Secondly, transparency in AI algorithms and decision-making processes is crucial for building trust among healthcare providers and patients. Thirdly, addressing potential biases in AI systems to ensure fair and equitable treatment across diverse patient populations is essential. Additionally, maintaining human oversight and the ability to override AI recommendations when necessary safeguards against over-reliance on automated systems. Lastly, continuous monitoring and evaluation of AI performance and outcomes are vital for identifying and rectifying any ethical concerns that may arise.""",
        """To ethically implement AI in healthcare, a multifaceted approach is necessary. One key aspect is obtaining informed consent from patients regarding the use of AI in their care, ensuring they understand the benefits and limitations. Another important factor is maintaining the human touch in healthcare delivery, using AI as a tool to augment rather than replace human expertise. Furthermore, establishing clear guidelines and regulations for AI development and deployment in healthcare settings helps maintain ethical standards. It's also crucial to invest in educating healthcare professionals about AI capabilities and limitations to ensure responsible use. Lastly, fostering interdisciplinary collaboration between healthcare providers, AI developers, and ethicists can help address complex ethical challenges as they emerge.""",
        """Ethical AI implementation in healthcare involves several critical considerations. First, prioritizing explainable AI models allows for better understanding and scrutiny of AI-driven decisions in medical contexts. Second, ensuring diverse representation in AI training data helps mitigate biases and improve accuracy across different demographic groups. Third, implementing robust security measures to protect against potential AI system vulnerabilities and cyber threats is essential. Additionally, establishing clear accountability frameworks for AI-assisted medical decisions helps delineate responsibilities between human practitioners and AI systems. Finally, promoting ongoing research into the long-term effects and ethical implications of AI in healthcare ensures continuous improvement and adaptation of ethical guidelines."""
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
    if 'ratings' not in st.session_state:
        st.session_state.ratings = {q: {i: pd.DataFrame(0, index=criteria, columns=['Rating']) for i in range(len(qa_dict[q]))} for q in qa_dict}
    if 'highlighted_text' not in st.session_state:
        st.session_state.highlighted_text = {q: {i: "" for i in range(len(qa_dict[q]))} for q in qa_dict}
    if 'preferred_answer' not in st.session_state:
        st.session_state.preferred_answer = {q: None for q in qa_dict}

    # Select a question
    question = st.selectbox("Choose a question:", list(qa_dict.keys()), key="question_select")
    
    # Update current question if changed
    if question != st.session_state.current_question:
        st.session_state.current_question = question

    st.write(f"**Question:** {question}")
    answers = qa_dict[question]

    for i, answer in enumerate(answers):
        st.write(f"\n**Answer {i + 1}:**")
        
        col1, col2 = st.columns([2, 3])
        
        with col1:
            # Display the answer in a text area without scroll bar
            st.text_area(f"Answer text:", answer, height=250, key=f"answer_text_{i}")
            
            # Text input for highlighted text
            highlighted = st.text_input(f"Highlighted text:", key=f"highlight_input_{i}")
            if highlighted:
                st.session_state.highlighted_text[question][i] = highlighted
        
        with col2:
            # Display rating sliders for the current answer
            st.write("**Rate this answer:**")
            criteria_col1, criteria_col2 = st.columns(2)
            for j, criterion in enumerate(criteria):
                with criteria_col1 if j < 6 else criteria_col2:
                    st.session_state.ratings[question][i].at[criterion, 'Rating'] = st.slider(
                        criterion,
                        0, 10, 
                        int(st.session_state.ratings[question][i].at[criterion, 'Rating']),
                        key=f"slider_{criterion}_{i}"
                    )
        
        st.markdown("---")  # Add a horizontal line for separation

    # Add radio button for selecting preferred answer
    preferred_answer = st.radio(
        "Select your preferred answer:",
        [f"Answer {i+1}" for i in range(len(answers))],
        index=st.session_state.preferred_answer[question] if st.session_state.preferred_answer[question] is not None else 0,
        key=f"preferred_answer_{question}"
    )
    st.session_state.preferred_answer[question] = int(preferred_answer.split()[-1]) - 1

    # Button to calculate and display results
    if st.button("Show Results", key="show_results_button"):
        st.write("\n**Ratings Summary:**")
        all_ratings = pd.concat([st.session_state.ratings[question][i] for i in range(len(answers))], axis=1)
        all_ratings.columns = [f"Answer {i+1}" for i in range(len(answers))]
        st.dataframe(all_ratings)

        # Calculate and display the average rating for each answer
        average_ratings = all_ratings.mean()
        st.write("\n**Average Ratings:**")
        st.dataframe(average_ratings)

        # Identify the best answer based on average rating
        best_answer_index = average_ratings.idxmax()
        st.write(f"\n**Best Answer (Based on Ratings):** {best_answer_index}")
        st.write(f"**Average Rating:** {average_ratings[best_answer_index]:.2f}")

        # Display the user's preferred answer
        st.write(f"\n**User's Preferred Answer:** Answer {st.session_state.preferred_answer[question] + 1}")

        # Display highlighted text for all answers
        st.write("\n**Highlighted Text:**")
        for i, answer in enumerate(answers):
            st.write(f"\nAnswer {i + 1}:")
            highlighted = st.session_state.highlighted_text[question][i]
            if highlighted:
                st.write(f"- {highlighted}")
            else:
                st.write("No text highlighted.")

if __name__ == "__main__":
    streamlit_app()

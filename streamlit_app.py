def streamlit_app():
    st.title("Q&A Evaluation App")

    # Initialize session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = list(qa_dict.keys())[0]
    if 'ratings' not in st.session_state:
        st.session_state.ratings = {q: {i: pd.DataFrame(0, index=criteria, columns=['Rating']) for i in range(len(qa_dict[q]))} for q in qa_dict}
    if 'highlighted_text' not in st.session_state:
        st.session_state.highlighted_text = {q: {i: "" for i in range(len(qa_dict[q]))} for q in qa_dict}

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
        st.write(f"\n**Best Answer:** {best_answer_index}")
        st.write(f"**Average Rating:** {average_ratings[best_answer_index]:.2f}")

        # Display highlighted text for all answers
        st.write("\n**Highlighted Text:**")
        for i, answer in enumerate(answers):
            st.write(f"\nAnswer {i + 1}:")
            highlighted = st.session_state.highlighted_text[question][i]
            if highlighted:
                st.write(f"- {highlighted}")
            else:
                st.write("No text highlighted.")

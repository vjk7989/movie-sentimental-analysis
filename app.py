import streamlit as st
import pandas as pd
from textblob import TextBlob
import os

# Define the path to the Excel file
EXCEL_FILE = 'movie_reviews.xlsx'


# Load or create the Excel file
def load_excel_file(file_path):
    # Check if the file exists; if not, create it
    if not os.path.exists(file_path):
        # Create a DataFrame with the appropriate columns
        df = pd.DataFrame(columns=["Movie", "Review", "Sentiment"])
        # Save the new DataFrame as an Excel file
        df.to_excel(file_path, index=False)
    else:
        # Load the existing Excel file
        df = pd.read_excel(file_path)
    return df


# Save the review and sentiment into the Excel file
def save_review_to_excel(file_path, movie, review, sentiment):
    # Load existing reviews or create a new file if needed
    df = load_excel_file(file_path)
    # Create a new entry for the current review and sentiment
    new_entry = pd.DataFrame({"Movie": [movie], "Review": [review], "Sentiment": [sentiment]})
    # Append the new review to the DataFrame
    df = pd.concat([df, new_entry], ignore_index=True)
    # Save the updated DataFrame back to the Excel file
    df.to_excel(file_path, index=False)


# Add a new movie to the Excel file
def add_movie_to_excel(file_path, movie_name):
    df = load_excel_file(file_path)
    # Check if the movie already exists in the DataFrame
    if movie_name not in df['Movie'].values:
        # Create a new entry for the movie with empty review and sentiment
        new_movie_entry = pd.DataFrame({"Movie": [movie_name], "Review": [""], "Sentiment": [""]})
        # Append the new movie to the DataFrame
        df = pd.concat([df, new_movie_entry], ignore_index=True)
        # Save the updated DataFrame back to the Excel file
        df.to_excel(file_path, index=False)


# Perform sentiment analysis
def analyze_sentiment(review):
    analysis = TextBlob(review)
    # Determine if sentiment is Good, Bad, or Neutral based on polarity
    if analysis.sentiment.polarity > 0:
        return "Good"
    elif analysis.sentiment.polarity < 0:
        return "Bad"
    else:
        return "Neutral"


# Streamlit UI
def main():
    st.title("Movie Review Sentiment Analysis")

    # Initial list of movies
    movies = ["Titanic", "Vettai", "Inception", "Avatar"]

    # A session state to store the added movies
    if 'added_movies' not in st.session_state:
        st.session_state.added_movies = []

    # Load existing movies from Excel and update session state
    df = load_excel_file(EXCEL_FILE)
    for movie in df['Movie'].values:
        if movie not in movies and movie not in st.session_state.added_movies:
            st.session_state.added_movies.append(movie)

    # Combine the default movies with added movies
    all_movies = movies + st.session_state.added_movies

    # Select a movie from the updated list
    selected_movie = st.selectbox("Pick a movie:", all_movies)

    # Button and text input to add a new movie
    if st.button("+ Add a new movie"):
        st.session_state.show_movie_input = True

    if st.session_state.get('show_movie_input', False):
        new_movie = st.text_input("Enter the name of the movie:")
        if st.button("Add Movie"):
            if new_movie:
                # Add the new movie to the session state list
                st.session_state.added_movies.append(new_movie)
                # Add the new movie to the Excel file
                add_movie_to_excel(EXCEL_FILE, new_movie)
                st.session_state.show_movie_input = False
                st.success(f"Movie '{new_movie}' added to the list.")
            else:
                st.error("Please enter a movie name.")

    # Text input for user review
    review = st.text_area("Enter your review for the movie:")

    # Button to analyze sentiment
    if st.button("Analyze Sentiment"):
        if review:
            # Perform sentiment analysis
            sentiment = analyze_sentiment(review)
            st.write(f"Sentiment for your review: **{sentiment}**")

            # Save the review and sentiment to the Excel file
            save_review_to_excel(EXCEL_FILE, selected_movie, review, sentiment)

            # Notify the user that the review has been saved
            st.success("Your review and sentiment have been saved.")
        else:
            st.error("Please enter a review before analyzing.")

    # Button to show all saved reviews
    if st.button("Show All Reviews"):
        # Load all reviews from the Excel file and display them
        df = load_excel_file(EXCEL_FILE)
        st.write(df)


if __name__ == "__main__":
    main()

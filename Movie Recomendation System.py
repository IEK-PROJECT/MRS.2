from unittest import result
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import tkinter as tk
from tkinter import simpledialog, messagebox


def display_recommendations(user_input, recommended_movies):
    result_window = tk.Tk()
    result_window.title("Movie Recommendations")

    if not recommended_movies.empty:
        # Create a Tkinter Label to display recommendations
        label = tk.Label(result_window, text=f"Recommendations based on input: {user_input}", font=("Helvetica", 16))
        label.pack()

        # Create a Tkinter Text widget to display movie details
        text_widget = tk.Text(result_window, height=660, width=770)
        text_widget.insert(tk.END, "Title\t\tRelease Date\t\tOverview\n")
        
        for index, row in recommended_movies.iterrows():
            text_widget.insert(tk.END, f"{row['title']}\t\t{row['release_date']}\t\t{row['overview']}\n")

        text_widget.pack()
    else:
        # No recommendations found
        label = tk.Label(result_window, text="No recommendations found.", font=("Helvetica", 16))
        label.pack()

    # Add a button to close the window
    close_button = tk.Button(result_window, text="Close", command=result_window.destroy)
    close_button.pack()

    result_window.mainloop()


# Function to get user input using Tkinter
def get_user_input():
    root = tk.Tk()
    root.withdraw()
    user_input = simpledialog.askstring("Input", "Enter the name of the movie: ")
    root.destroy()
    return user_input

# Function to display recommendations in a new Tkinter window
def display_recommendations(user_input, recommended_movies):
    result_window = tk.Tk()
    result_window.title("Movie Recommendations")

    if not recommended_movies.empty:
        # Create a Tkinter Label to display recommendations
        label = tk.Label(result_window, text=f"Recommendations based on input: {user_input}", font=("Helvetica", 16))
        label.pack()

        # Create a Tkinter Text widget to display movie details
        text_widget = tk.Text(result_window, height=600, width=770)
        text_widget.insert(tk.END, recommended_movies[['title', 'release_date', 'overview']].to_string(index=False))
        text_widget.pack()
    else:
        # No recommendations found
        label = tk.Label(result_window, text="No recommendations found.", font=("Helvetica", 16))
        label.pack()
    result_window.geometry("300x200")  
    result_window['background'] ='blue'
  

    result_window.mainloop()

# Set the date range
start_date = '1910-01-01'
end_date = '2024-01-01'

# API CONNECTION
tmdb_api_key = '3ef749f8c526bc42fb7720f376d78327'
api_url = f'https://api.themoviedb.org/3/discover/movie?api_key={tmdb_api_key}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&primary_release_date.gte={start_date}&primary_release_date.lte={end_date}'

# Fetch data from the TMDb API
try:
    response = requests.get(api_url)
    response.raise_for_status()  # Check for errors in the HTTP request
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data from the TMDb API: {e}")
    data = None
    messagebox.showerror("Error", f"Error fetching data from the TMDb API: {e}")

# Continue with the rest of your code only if data is successfully retrieved
if data:
    # Extract relevant movie information from the API response
    movies = data['results']
    movie_data = {'title': [], 'overview': [], 'release_date': [], 'genre_ids': []}

    for movie in movies:
        movie_data['title'].append(movie['title'])
        movie_data['overview'].append(movie['overview'])
        movie_data['release_date'].append(movie['release_date'])
        movie_data['genre_ids'].append(movie['genre_ids'])

    # Create a DataFrame from the movie data
    movies_df = pd.DataFrame(movie_data)

    # Build a content-based movie recommendation system
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(movies_df['overview'].fillna(''))

    # Get user input for movie recommendations
    user_input = get_user_input()

    # Initialize recommended_movies as an empty DataFrame
    recommended_movies = pd.DataFrame(columns=['title', 'release_date', 'overview'])

# Recommendation logic
if user_input:
    # Convert movie names to lowercase for case-insensitive comparison
    user_input_lower = user_input.lower()

    # Calculate similarity scores for all movies
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Get the average similarity scores for all movies
    average_cosine_similarities = cosine_similarities.mean(axis=1)

    # Print the average similarity scores for all movies
    print("Average Similarity Scores for All Movies:")
    print(average_cosine_similarities)

    # Print all movie titles for debugging
    print("All Movie Titles:")
    print(movies_df['title'])

    # Assume the user input is a movie name
    chosen_movie_indices = movies_df.index[movies_df['title'].str.lower().str.contains(user_input_lower)].tolist()

    
    if chosen_movie_indices:
        # Print the chosen movie index for debugging
        print("Chosen Movie Index:")
        print(chosen_movie_indices)

        # Choose the first movie in case there are multiple matches
        chosen_movie_index = chosen_movie_indices[0]
        chosen_movie_title = movies_df.loc[chosen_movie_index, 'title']

        # Print the overview of the chosen movie
        print("\nOverview of Chosen Movie:")
        print(movies_df.loc[chosen_movie_index, 'overview'])

        # Print the individual similarity scores for the chosen movie
        print("\nIndividual Similarity Scores for Chosen Movie:")
        print(cosine_similarities[chosen_movie_index])

        # Recommend movies based on average similarity scores
        recommended_movies_indices = cosine_similarities[chosen_movie_index].argsort()[:-9:-1]  # Get top 7 similar movies
        recommended_movies = movies_df.loc[recommended_movies_indices, ['title', 'release_date', 'overview']]

        # Display recommendations in a Tkinter window
        display_recommendations(user_input, recommended_movies)
    else:
        print(f"No movie found with the name: {user_input}")
else:
    print("No user input provided.")



    # Display recommendations in a Tkinter window
    display_recommendations(user_input, recommended_movies)
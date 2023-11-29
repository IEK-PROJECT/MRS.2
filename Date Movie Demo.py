import pandas as pd
import requests
import tkinter as tk
from tkinter import simpledialog, messagebox

# Function to get user input using Tkinter
def get_user_input():
    root = tk.Tk()
    root.withdraw()
    user_input = simpledialog.askstring("Input", "Enter the year of release: ")
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
end_date = '2020-01-01'

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
    movie_data = {'title': [], 'overview': [], 'release_date': []}

    for movie in movies:
        movie_data['title'].append(movie['title'])
        movie_data['overview'].append(movie['overview'])
        movie_data['release_date'].append(movie['release_date'])


  # Get user input for movie recommendations
    user_input = get_user_input()


    # Create a DataFrame from the movie data
    movies_df = pd.DataFrame(movie_data)

    # Convert 'release_date' to datetime format
    movies_df['release_date'] = pd.to_datetime(movies_df['release_date'], errors='coerce')

    # Print the DataFrame
    print(movies_df[['title', 'release_date', 'overview']])

    display_recommendations = (user_input)

    text_widget = tk.Text(user_input, height=10, width=70)


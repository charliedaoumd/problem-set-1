'''
PART 2: SIMILAR ACTROS BY GENRE
Using the imbd_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- - As an example, select the row from your data frame associated with Chris Hemsworth, actor ID “nm1165110”, as your “query” actor
- Use sklearn.metrics.DistanceMetric to calculate the euclidean distances between your query actor and all other actors based on their genre appearances
- - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html
- Output a CSV continaing the top ten actors most similar to your query actor using cosine distance 
- - Name it 'similar_actors_genre_{current_datetime}.csv' to `/data`
- - For example, the top 10 for Chris Hemsworth are:  
        nm1165110 Chris Hemsworth
        nm0000129 Tom Cruise
        nm0147147 Henry Cavill
        nm0829032 Ray Stevenson
        nm5899377 Tiger Shroff
        nm1679372 Sudeep
        nm0003244 Jordi Mollà
        nm0636280 Richard Norton
        nm0607884 Mark Mortimer
        nm2018237 Taylor Kitsch
- Describe in a print() statement how this list changes based on Euclidean distance
- Make sure your code is in line with the standards we're using in this class
'''

#Write your code below

# Load data from the URL
import json
import time
import pandas as pd
import requests
from sklearn.metrics import DistanceMetric
from sklearn.metrics.pairwise import cosine_distances


def calcateSimilarActors():
    """
    Calculates and finds the top 10 most similar actors to a specified query actor based on genre appearances in movies.

    This function performs the following tasks:
    1. Retrieves and processes movie data from a remote JSON file containing information about movies, genres, and actors.
    2. Extracts and aggregates the genres for each actor, creating a feature matrix where rows represent actors and columns represent genres.
    3. Computes the cosine distances between the feature vector of a specified query actor and all other actors.
    4. Identifies and ranks the top 10 actors most similar to the query actor based on cosine distance.
    5. Outputs the results to a CSV file named with the current timestamp in a specified directory.

    Steps:
    1. **Data Retrieval and Parsing**: Fetches data from a specified URL and parses it to extract genres and actors.
    2. **Genre Aggregation**: Tracks all unique genres across movies and updates the genre counts for each actor.
    3. **DataFrame Creation**: Constructs a DataFrame where each row represents an actor and each column represents a genre.
    4. **Feature Extraction**: Retrieves the feature vector for the query actor and computes cosine distances from this vector to all other actors.
    5. **Similarity Ranking**: Finds the top 10 actors most similar to the query actor based on cosine distance.
    6. **CSV Output**: Saves the top 10 similar actors along with their distances to a CSV file in the `./data` directory.

    Parameters:
    - The function does not take any parameters directly but operates on a hardcoded query actor ID ('nm0003244') which can be changed as needed.

    Outputs:
    - A CSV file named `similar_actors_genre_{timestamp}.csv` is saved in the `./data` directory containing the top 10 most similar actors and their respective cosine distances from the query actor.

    Raises:
    - `ValueError`: If the query actor ID is not found in the dataset.

    Example:
    >>> calcateSimilarActors()
    10 most similar Actors (ID: nm0003244) based on Cosine distance have been saved to ./data/similar_actors_genre_20240724_151423.csv.
    """
    
    # Initialize the genre dictionary and actor dictionary
    genre_dict = {}
    actor_dict = {}

    url = 'https://raw.githubusercontent.com/cbuntain/umd.inst414/main/data/imdb_movies_2000to2022.prolific.json'
    response = requests.get(url)
    data = response.text.splitlines()

    # Set to track all unique genres
    all_genres = set()

    # First pass to collect all genres
    for line in data:
     this_movie = json.loads(line)
     genres = this_movie.get('genres', [])
     all_genres.update(genres)
    
        # Iterate through the actors
     for actor_id, actor_name in this_movie.get('actors', []):
        if actor_id not in actor_dict:
            actor_dict[actor_id] = actor_name
        if actor_id not in genre_dict:
            genre_dict[actor_id] = {genre: 0 for genre in all_genres}
        
        for genre in genres:
            genre_dict[actor_id][genre] = genre_dict[actor_id].get(genre, 0) + 1

    # Create DataFrame from genre_dict
    df = pd.DataFrame.from_dict(genre_dict, orient='index').fillna(0)

    # Add the actor names as a column
    df['actor_name'] = df.index.map(actor_dict)

    # Define the query actor ID
    query_actor_id = 'nm0003244'  # Jordi Mollà

    if query_actor_id not in df.index:
        raise ValueError(f"Query actor ID {query_actor_id} not found in the dataset")

    # Extract the feature matrix and the query actor's features
    feature_matrix = df.drop(columns=['actor_name'])
    query_actor_features = feature_matrix.loc[query_actor_id].values.reshape(1, -1)

    # Calculate cosine distances
    distances = cosine_distances(feature_matrix.values, query_actor_features).flatten()
    df['distance'] = distances

    # Filter out the query actor and find the top 10 most similar actors based on cosine distance
    df_filtered = df[df.index != query_actor_id]
    top_10_similar_actors = df_filtered.nsmallest(10, 'distance')

    # Output the top 10 actors to a CSV file
    current_time = time.time()
    formatted_time = time.strftime('%Y%m%d_%H%M%S', time.localtime(current_time))
    csv_filename = f'./data/similar_actors_genre_{formatted_time}.csv'
    top_10_similar_actors[['actor_name', 'distance']].to_csv(csv_filename, index_label='actor_id')

    print(f" 10 most similar Actors (ID: {query_actor_id}) based on Cosine distance have been saved to {csv_filename}.")

'''
PART 1: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Guild a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to. 
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is line with the standards we're using in this class 
'''

import datetime
import json
import numpy as np
import pandas as pd
import networkx as nx
import requests

url = 'https://raw.githubusercontent.com/cbuntain/umd.inst414/main/data/imdb_movies_2000to2022.prolific.json'
response = requests.get(url)
data = response.text.splitlines()

# Build the graph
g = nx.Graph()
rows = []

# Set up your dataframe(s) -> the df that's output to a CSV should include at least the columns 'left_actor_name', '<->', 'right_actor_name'
genres = set()

with open() as in_file:
    """
    Process the movie data from each line to build the graph of actor interactions.

    This block iterates through each line of the data, where each line represents a movie and contains information about actors and their collaborations. It performs the following steps:
    
    1. **Load Movie Data**: Each line is parsed from JSON format into a Python dictionary to access movie details.
    2. **Create Nodes**: Adds a node to the graph for each actor, using their ID and name.
    3. **Generate Actor Pairs**: Iterates through all pairs of actors in each movie, creating edges between them.
        - If an edge between the pair already exists, its weight (i.e., the count of movies they've appeared in together) is incremented.
        - If the edge does not exist, a new edge is added with an initial weight of 1.

    The counter `i` ensures that all unique pairs of actors are considered, and the graph is updated with these interactions.
    """
    for line in data:
        # Load the movie from this line
        this_movie = json.loads(line)

        # Don't forget to include docstrings for all functions

        # Load the movie from this line
        this_movie = json.loads(line)
            
        # Create a node for every actor
        for actor_id, actor_name in this_movie['actors']:
        # add the actor to the graph    
         g.add_node(actor_id, name=actor_name)
        # Iterate through the list of actors, generating all pairs
         i = 0  # Counter
        ## Starting with the first actor in the list, generate pairs with all subsequent actors
        ## then continue to second actor in the list and repeat
        for left_actor_id,left_actor_name in this_movie['actors']:
            for right_actor_id,right_actor_name in this_movie['actors'][i+1:]:
                # Get the current weight, if it exists
                if g.has_edge(left_actor_id, right_actor_id):
                    g[left_actor_id][right_actor_id]['weight'] += 1
                else:
                # Add an edge for these actors
                    g.add_edge(left_actor_id, right_actor_id, weight=1)
            i += 1 


# Print the info below
print("Nodes:", len(g.nodes))

#Print the 10 the most central nodes
centrality = nx.degree_centrality(g)
sorted_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
top_10_central_nodes = sorted_centrality[:10]

df_centrality = pd.DataFrame(top_10_central_nodes, columns=['actor_id', 'centrality'])
df_centrality['actor_name'] = df_centrality['actor_id'].map(lambda actor_id: g.nodes[actor_id]['name'])

mean_centrality = np.mean(df_centrality['centrality'])
print(f"Mean centrality of the top 10 nodes: {mean_centrality}")

print("Top 10 most central nodes:")
for node_id, centrality_value in top_10_central_nodes:
    print(f"{g.nodes[node_id]['name']}: {centrality_value}")
# Output the final dataframe to a CSV named 'network_centrality_{current_datetime}.csv' to `/data`
current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
csv_filename = f'/data/network_centrality_{current_datetime}.csv'
df_centrality.to_csv(csv_filename, index=False)


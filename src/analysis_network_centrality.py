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
import os
import numpy as np
import pandas as pd
import networkx as nx
import requests
import time

# Build the graph
g = nx.Graph()

# Set up your dataframe(s) -> the df that's output to a CSV should include at least the columns 'left_actor_name', '<->', 'right_actor_name'
genres = set()

def analyze_and_save_graph_data(url):
    """
    Download movie data from a URL, build a graph of actor interactions, calculate centrality metrics,
    and save both edge data and centrality metrics to separate CSV files.

    Args:
        url (str): The URL to fetch the movie data from.

    Returns:
        None
    """
   
    # Fetch data from URL
    response = requests.get(url)
    data = response.text.splitlines()

    edges = []

    # Process the data and build the graph
    for line in data:
        # Load the movie from this line
        this_movie = json.loads(line)
        
        # Create a node for every actor
        actors = list(this_movie['actors'])  # Convert to list to facilitate pair generation
        
        for actor_id, actor_name in actors:
            # Add the actor to the graph    
            g.add_node(actor_id, name=actor_name)

        # Iterate through the list of actors, generating all pairs
        for i, (left_actor_id, left_actor_name) in enumerate(actors):
            for right_actor_id, right_actor_name in actors[i+1:]:
                # Get the current weight, if it exists
                if g.has_edge(left_actor_id, right_actor_id):
                    g[left_actor_id][right_actor_id]['weight'] += 1
                else:
                    # Add an edge for these actors
                    g.add_edge(left_actor_id, right_actor_id, weight=1)
                
                # Append the edge details to the list
                edges.append([left_actor_name, '<->', right_actor_name])
    
    # Convert the edges list to a DataFrame
    df_edges = pd.DataFrame(edges, columns=['left_actor_name', '<->', 'right_actor_name'])
    
    # Calculate the centrality
    centrality = nx.degree_centrality(g)
    sorted_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    top_10_central_nodes = sorted_centrality[:10]

    # Create DataFrame for centrality
    df_centrality = pd.DataFrame(top_10_central_nodes, columns=['actor_id', 'centrality'])
    df_centrality['actor_name'] = df_centrality['actor_id'].map(lambda actor_id: g.nodes[actor_id]['name'])

    # Print mean centrality
    mean_centrality = np.mean(df_centrality['centrality'])
    print(f"Mean centrality of the top 10 nodes: {mean_centrality}")

    # Print top 10 central nodes
    print("Top 10 most central nodes:")
    for node_id, centrality_value in top_10_central_nodes:
        print(f"{g.nodes[node_id]['name']}: {centrality_value}")

    # Create directory for saving files if it doesn't exist
    data_dir = './data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Save edges data to CSV
    current_time = time.time()
    formatted_time = time.strftime('%Y%m%d_%H%M%S', time.localtime(current_time))
    edges_filename = os.path.join(data_dir, f'actor_edges_{formatted_time}.csv')
    df_edges.to_csv(edges_filename, index=False)
    print(f"Edges data saved to {edges_filename}")


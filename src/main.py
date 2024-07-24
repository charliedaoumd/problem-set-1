'''
Pull down the imbd_movies dataset here and save to /data as imdb_movies_2000to2022.prolific.json
You will run this project from main.py, so need to set things up accordingly
'''

import analysis_network_centrality
import analysis_similar_actors_genre

# Ingest and save the imbd_movies dataset
url = 'https://raw.githubusercontent.com/cbuntain/umd.inst414/main/data/imdb_movies_2000to2022.prolific.json'
output_dir = '/data'
output_file = f'{output_dir}/imdb_movies_2000to2022.prolific.json'

        
# Call functions / instanciate objects from the two analysis .py files
def main():
    # Instantiate objects
    network_centrality = analysis_network_centrality
    similar_analysis =  analysis_similar_actors_genre

    #Call Functions
    network_centrality.analyze_and_save_graph_data(url)
    similar_analysis.calcateSimilarActors()


if __name__ == "__main__":
    main()
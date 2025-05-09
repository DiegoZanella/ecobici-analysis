import utils.utils as utils

dataset_name = '2025-01'
trips_filename = f'../data/trips/{dataset_name}.csv'
stations_filename = '../data/stations/ecobici_stations.csv'
output_filename = f'../data/processed/communities_{dataset_name}.csv'

df = utils.load_stations_df(trips_filename)
g_directed, g_undirected = utils.create_graph(df)

community_df, partition, community_size = utils.detect_communities(g_undirected)
geo_with_communities = utils.add_geolocations(community_df, stations_filename)

print(geo_with_communities.head())
print(geo_with_communities.columns)

geo_with_communities.to_csv(output_filename)
print(f"Dataframe saved to {output_filename}")
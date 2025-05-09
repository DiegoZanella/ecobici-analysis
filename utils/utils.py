import pandas as pd
import networkx as nx


def load_stations_df(csv_filename: str):
    data = pd.read_csv(csv_filename)
    estaciones_retiro = data['Ciclo_Estacion_Retiro'].unique()
    estaciones_arribo = data['Ciclo_EstacionArribo'].unique()

    df1 = pd.DataFrame({'Ciclo_Estacion_Retiro': estaciones_retiro})
    df2 = pd.DataFrame({'Ciclo_EstacionArribo': estaciones_arribo})
    df = df1.merge(df2, how='cross')

    return df


def create_graph(df):
    trip_counts = df.groupby(['Ciclo_Estacion_Retiro', 'Ciclo_EstacionArribo']).size().reset_index(name='weight')
    weighted_edges = df.merge(trip_counts, on=['Ciclo_Estacion_Retiro', 'Ciclo_EstacionArribo'], how='left')
    weighted_edges['weight'] = weighted_edges['weight'].fillna(0).astype(int)

    edges = weighted_edges[weighted_edges['weight'] > 0][['Ciclo_Estacion_Retiro', 'Ciclo_EstacionArribo', 'weight']]
    G = nx.DiGraph()

    for _, row in edges.iterrows():
        G.add_edge(row['Ciclo_Estacion_Retiro'], row['Ciclo_EstacionArribo'], weight=row['weight'])

    return G, G.to_undirected()


def add_geolocations(df, geolocations_filename):
    geo_locations = pd.read_csv(geolocations_filename)
    geo_locations['station_id'] = geo_locations['num_cicloestacion'].astype(str).str.zfill(3)





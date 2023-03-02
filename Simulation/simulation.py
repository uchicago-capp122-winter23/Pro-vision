import pandas as pd
import numpy as np
import networkx as nx
from Setu import distance # adjust name


class Graph(object):
    """
    ---
    """

    def __init__(self, prov_data, sei_data, *, \
                prov_serv = 'police_stations', sei_ind = 'Homicide rate'):
        """
        Constructor. Creates the object, by defining its basic attributes,
            notably, the dataframe with attributes for each community area.
        """

        NUMBER_OF_SEI = 10

        prov_centers = pd.read_csv(prov_data, usecols = \
                                   ['ADDRESS', 'coords', 'type'])
        prov_centers = prov_centers[prov_centers.type == prov_serv] 
        prov_centers[['Latitude', 'Longitude']] = prov_centers['coords'].apply(\
            lambda x: pd.Series(str(x).strip('()').split(',')))
        self.prov_centers = prov_centers


        df = pd.read_csv(sei_data, usecols = \
                        ['Name', 'GEOID', 'Longitude', 'Latitude', 'indicator', \
                         'value'])    # Confirm with Setu's csv
        df = df[df['indicator'] == sei_ind]
        self.df = df

        df_extended = df
        df_extended['Tensioned'] = df_extended['indicator'].apply(\
            lambda x: 1 if x.nlargest(NUMBER_OF_SEI, 'value') else 0)
        # df['Prov_within'] = using GeoPandas
        self.df_extended = df_extended


    
        pass



    def gen_adjac_matrix(self, ):
        """
        Generates the adjacency matrix that models the city of Chicago as a
            network of census tracts, based on their nearness degree (distance in 
            time less than 10 minutes in car from each other).
        Parameters:
        Returns
        """

        # Use GeoPandas
        pass


    def gen_graph(self, ):
        """
        Generates the graph that models the city of Chicago as a network of 
            census tracts, where connected nodes are "near" census tracts using
            the adjacency matrix. The value of each node indicates whether the 
            census tract is near a police station and whether it is tensioned
            (top10 in homicide rate). 
        Parameters:
        Returns
        """

        graph = nx.Graph(self.gen_adjac_matrix())
        # Include labels

        pass


    def apply_shock(self, ):
        """
        Creates a diagonal matrix for modelling either a negative shock in the 
            amount of provision or a change in tensionned census tracts. Each 
            element of the diagonal incorporates the value of the shock for each
            census tract. Applies the shock by multiplying the adjacency matrix
            to this shock matrix.
            the shock by  
        Parameters:
        Returns        
        """


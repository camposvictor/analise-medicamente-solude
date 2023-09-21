import os

import pandas as pd


def get_all_materials():
    materials = pd.read_csv(os.path.join(os.getcwd() , 'data/materials.csv'))
    return materials['Material']
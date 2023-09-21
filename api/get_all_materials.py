import pandas as pd


def get_all_materials():
    materials = pd.read_csv('data/materials.csv')
    return materials['Material']
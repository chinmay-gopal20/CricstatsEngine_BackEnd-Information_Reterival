import pandas as pd

players = pd.read_csv('players.csv').values.tolist()
print(players)
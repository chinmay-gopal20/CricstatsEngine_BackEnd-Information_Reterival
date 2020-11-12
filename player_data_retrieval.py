import json


# read json file of the corresponding player and return.
# player = virat-kohli convert it as virat_kohli.json
def retrievePlayerStats(data_dir='H:/edu/sem IX/IR/package/cricstats_engine/data/', player=None):
    player_data = open(data_dir+player.lower().replace('-', '_')+'.json')
    return json.load(player_data)

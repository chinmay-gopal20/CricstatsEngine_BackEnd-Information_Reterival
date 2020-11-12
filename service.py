from ranking_and_querying import searchEngine
from player_data_retrieval import retrievePlayerStats


class Service:

    # get results from searchEngine
    @staticmethod
    def getResults(query_string=None, top_n=None):
        try:
            # convert top_n to int, if top_n is None will catch the exception and set it as None
            try:
                top_n = int(top_n)
            except:
                top_n = None

            players, count = searchEngine(query_string=query_string, top_n=top_n)
            return {'count': count, 'players': players}
        except Exception as error:
            return 'Error in Service - ' + str(error)

    # get player stats from retrievePlayerStats
    @staticmethod
    def getPlayerStats(player=None):
        player_stats = retrievePlayerStats(player=player)
        return player_stats

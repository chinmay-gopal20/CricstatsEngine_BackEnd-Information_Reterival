from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir

import json


def searchEngine(index_dir='H:/edu/sem IX/IR/package/cricstats_engine/index/', query_string=None, top_n=None):

    # index dir
    index = open_dir(index_dir)

    # searcher object
    # ranking algo used - Frequency
    # available ranking algos - TF_IDF, BM25F, etc.
    searcher = index.searcher(weighting=scoring.Frequency)

    # generate query using QueryParser using given query_string
    # search the query using searcher object
    # return results
    try:
        player_names = []
        query = QueryParser("content", index.schema).parse(query_string)
        results = searcher.search(query, limit=top_n)
        for i in range(len(results)):
            player_names.append(results[i]['title'].replace('.json', '').replace('_', ' ').title())
            if top_n is not None:
                if i == top_n-1:
                    break
        return player_names, len(player_names)
    except Exception as error:
        return "Error in ranking & Querying - " + str(error)
    # close the searcher object
    finally:
        searcher.close()


# if __name__ == "__main__":
#     index_dir = 'H:/edu/sem IX/IR/package/cricstats_engine/index/'
#     query_string = 'india'
#     top_n = 50
#
#     print(searchEngine(index_dir, query_string, top_n))
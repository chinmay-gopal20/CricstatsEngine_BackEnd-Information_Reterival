from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir


def searchEngine(index_dir, query_string, top_n):

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
        query = QueryParser("content", index.schema).parse(query_string)
        results = searcher.search(query, limit=top_n)
        for i in range(top_n):
            print('Title - ', results[i]['title'], '\nScore - ', str(results[i].score), '\nData - ', results[i]['textdata'])
            print('-------------------------------------------')
    # close the searcher object
    finally:
        searcher.close()


if __name__ == "__main__":
    index_dir = 'H:/edu/sem IX/IR/package/cricstats_engine/index/'
    query_string = 'sri lanka OR India'
    top_n = 8

    searchEngine(index_dir, query_string, top_n)
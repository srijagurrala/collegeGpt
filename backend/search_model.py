from whoosh.index import open_dir
from whoosh.qparser import QueryParser

def search(query):
    index_dir = 'data/indexdir'
    index = open_dir(index_dir)
    with index.searcher() as searcher:
        query_parser = QueryParser("content", index.schema)
        parsed_query = query_parser.parse(query)
        results = searcher.search(parsed_query)
        return [dict(result) for result in results]  # Return a list of results

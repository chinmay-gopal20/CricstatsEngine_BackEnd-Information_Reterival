import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID


def createSearchableData(data_dir, index_dir):
    '''
    Schema definition: title(name of file), path(as ID), content(indexed
    but not stored),textdata (stored text content)
    '''
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT, textdata=TEXT(stored=True))
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    # Creating a index writer to add document as per schema
    ix = create_in(index_dir, schema)
    writer = ix.writer()

    # open each document in given data_dir and add it to the index
    filepaths = [os.path.join(data_dir, i) for i in os.listdir(data_dir)]
    for path in filepaths:
        fp = open(path, 'r')
        print(path)
        text = fp.read()
        writer.add_document(title=path.split("/")[-1], path=path, content=text, textdata=text)
        fp.close()
    # commit the index writer
    writer.commit()


if __name__ == "__main__":
    data_dir = 'H:/edu/sem IX/IR/package/cricstats_engine/data/'
    index_dir = 'H:/edu/sem IX/IR/package/cricstats_engine/index/'
    createSearchableData(data_dir, index_dir)
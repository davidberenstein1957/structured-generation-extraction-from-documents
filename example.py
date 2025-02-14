import glob

from steps import chunk, convert

paths = glob.glob("data/*.pdf")
documents = convert(paths)
for document in documents:
    for chunks in chunk(document):
        for chunk_iter in chunks:
            print(chunk_iter)
            for chunk_ in chunk_iter:
                print(chunk_.text)
                exit()

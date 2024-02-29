import os

from dotenv import load_dotenv

from models import Document
from opensearch import create_client, create_index_if_not_exists, bulk_ingest_documents

if __name__ == "__main__":
    load_dotenv()
    auth = ("admin", os.getenv("OPENSEARCH_PWD"))
    client = create_client(host="127.0.0.1", port=9200, auth=auth)

    index_name = "example"
    create_index_if_not_exists(client, index_name)

    doc1 = Document(
        {"title": "Moneyball", "director": "Bennett Miller", "year": 2011},
        "example",
        "1"
    )
    doc2 = Document(
        {"title": "Dark Knight Rises", "director": "Christopher Nolan", "year": 2012},
        "example",
        "2"
    )

    bulk_ingest_documents(client, [doc1, doc2])

import os
from typing import NamedTuple, Dict

from dotenv import load_dotenv
from opensearchpy import OpenSearch


class Document(NamedTuple):
    opensearch_index: str
    id: str
    body: Dict[str, str | int]


def create_client() -> OpenSearch:
    host = "127.0.0.1"
    port = 9200
    load_dotenv()
    auth = ("admin", os.getenv("OPENSEARCH_PWD"))
    client = OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_compress=True,
        http_auth=auth,
        use_ssl=False,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )
    return client


def create_index_if_not_exists(client: OpenSearch, index_name: str):
    try:
        if not client.indices.exists(index=index_name):
            client.indices.create(index=index_name)
            print(f"Index '{index_name}' created.")
        else:
            print(f"Index '{index_name}' already exists.")
    except Exception as e:
        print(f"error occured: {e}")


def ingest_documents(client: OpenSearch, document: Document):
    response = client.index(
        index=document.opensearch_index,
        body=document.body,
        id=document.id,
    )
    return response


def bulk_ingest_documents():
    pass


if __name__ == "__main__":
    client = create_client()
    print("client created")

    index_name = "example"
    create_index_if_not_exists(client, index_name)

    doc1 = Document(
        "example",
        "1",
        {"title": "Moneyball", "director": "Bennett Miller", "year": 2011},
    )

    print("Document Ingestion starting")
    ingest_documents(client, doc1)

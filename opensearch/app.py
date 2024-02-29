import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List

from dotenv import load_dotenv
from opensearchpy import OpenSearch, helpers


class BulkOperationType(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    INDEX = "index"


@dataclass
class Document:
    body: Dict[str, str | int]
    index: str = field(metadata={"name": "_index"})
    id: str = field(metadata={"name": "_id"})

    def to_bulk_dict(self, op_type: BulkOperationType) -> Dict:
        """
        Prepares the document for bulk ingestion in OpenSearch by flattening the body
        and including '_index' and '_id' at the top level, excluding 'body' as a key.
        """
        # Directly create the action/metadata dict
        bulk_dict = {
            "_op_type": op_type,
            "_id": self.id,
            "_index": self.index
        }

        # Merge the contents of the body into the bulk_dict, flattening it
        bulk_dict.update(self.body)
        print(bulk_dict)

        return bulk_dict


def create_client() -> OpenSearch:
    host = "127.0.0.1"
    port = 9200
    load_dotenv()
    auth = ("admin", os.getenv("OPENSEARCH_PWD"))
    print("Client is being initialized")
    client = OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_compress=True,
        http_auth=auth,
        use_ssl=False,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )
    print("Client is initialized")
    return client


def create_index_if_not_exists(client: OpenSearch, index_name: str):
    try:
        if not client.indices.exists(index=index_name):
            client.indices.create(index=index_name)
            print(f"Index '{index_name}' created.")
        else:
            print(f"Index '{index_name}' already exists.")
    except Exception as e:
        print(f"error occurred: {e}")


def ingest_document(client: OpenSearch, document: Document):
    print("Document ingestion has started")
    response = client.index(
        index=document.index,
        body=document.body,
        id=document.id,
    )
    print("Document ingestion has completed")
    return response


def bulk_ingest_documents(client: OpenSearch, documents: List[Document],
                          op_type: BulkOperationType = BulkOperationType.INDEX):
    """
    The bulk ingestion lets you upload multiple documents in a single request leading to significant
    performance benefits.

    Each document in the `documents` list is associated with an action indicating how it should be processed.
    Supported actions are:
    - CREATE: Add a new document. Fails if a document with the same ID already exists.
    - INDEX: Adds a new document or replaces an existing document with the same ID.
    - DELETE: Removes a document from the index.
    - UPDATE: Updates an existing document with new data.
    :param client: The OpenSearch client instance used to connect to the database.
    :param documents: A list of document objects to be ingested
    :param op_type: Type of bulk operation
    :return:
    """
    documents_dict = [doc.to_bulk_dict(op_type) for doc in documents]
    print(documents_dict)
    response = helpers.bulk(client, documents_dict, max_retries=3)
    return response


if __name__ == "__main__":
    client = create_client()

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

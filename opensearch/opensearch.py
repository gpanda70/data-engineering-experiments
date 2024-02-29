from typing import List, Tuple

from opensearchpy import OpenSearch, helpers

from models import Document, BulkOperationType


def create_client(host: str, port: int, auth: Tuple[str, str | None]) -> OpenSearch:
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

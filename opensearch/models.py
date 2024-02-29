from dataclasses import field, dataclass
from enum import Enum
from typing import Dict


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

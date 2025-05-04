from pymilvus import MilvusClient, FieldSchema, DataType, CollectionSchema

# Połączenie z serwerem Milvus
host = "localhost"
port = "19530"

milvus_client = MilvusClient(host=host, port=port)

# Parametry kolekcji
VECTOR_LENGTH = 768  # Długość wektora w Silver Retriever Base

id_field = FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, description="Primary id")
text = FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=4096, description="Page text")
embedding_text = FieldSchema("embedding", dtype=DataType.FLOAT_VECTOR, dim=VECTOR_LENGTH, description="Embedded text")

fields = [id_field, text, embedding_text]
schema = CollectionSchema(fields=fields, auto_id=True, enable_dynamic_field=True, description="RAG Texts collection")

# Tworzenie kolekcji
COLLECTION_NAME = "rag_texts_and_embeddings"

milvus_client.create_collection(
    collection_name=COLLECTION_NAME,
    schema=schema
)

# Tworzenie indeksu
index_params = milvus_client.prepare_index_params()
index_params.add_index(
    field_name="embedding", 
    index_type="HNSW", 
    metric_type="L2", 
    params={"M": 4, "efConstruction": 64}
)

milvus_client.create_index(
    collection_name=COLLECTION_NAME,
    index_params=index_params
)

# Listowanie kolekcji
print(milvus_client.list_collections())

# Opis kolekcji
print(milvus_client.describe_collection(COLLECTION_NAME))

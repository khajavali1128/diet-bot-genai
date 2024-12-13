from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-mpnet-base-v2")

query_embedding = model.encode("loose fat")
passage_embeddings = model.encode([
    "muscle gain",
    "weight loss",
    "cardio",
    "muscle maintainance"
])

similarity = model.similarity(query_embedding, passage_embeddings)

print(similarity)
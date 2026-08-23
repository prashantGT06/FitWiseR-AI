import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "workout_memory"

# Create collection
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=4,
            distance=models.Distance.COSINE
        )
    )

# Add one workout memory
client.upsert(
    collection_name=COLLECTION_NAME,
    points=[
        models.PointStruct(
            id=1,
            vector=[0.1, 0.2, 0.3, 0.4],
            payload={
                "user": "demo_user",
                "exercise": "bench press",
                "weight": 50,
                "reps": 8,
                "date": "2026-08-07"
            }
        )
    ]
)

print("Workout memory saved successfully!")

# Retrieve workout memory
results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=[0.1, 0.2, 0.3, 0.4],
    limit=1
)

print("\nRetrieved workout:")

for point in results.points:
    print("Exercise:", point.payload["exercise"])
    print("Weight:", point.payload["weight"], "kg")
    print("Reps:", point.payload["reps"])
    print("Date:", point.payload["date"])
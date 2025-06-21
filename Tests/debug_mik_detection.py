from twelvelabs import TwelveLabs
import os
from dotenv import load_dotenv

load_dotenv()
client = TwelveLabs(api_key=os.getenv("TWELVE_LABS_API_KEY"))
index_id = os.getenv("CAMPAIGN_INDEX_ID")

# Your task ID
task_id = "6854390d90ccccf6763451b9"

print(f"Debugging Task: {task_id}")
print("-" * 50)

# Get task details
task = client.task.retrieve(task_id)
print(f"Status: {task.status}")
print(f"Video ID: {task.video_id}")

if task.status == "ready":
    video_id = task.video_id
    
    # Try different search approaches
    print("\n1. Searching entire index for 'milk'...")
    results = client.search.query(
        index_id=index_id,
        query_text="milk",
        options=["visual", "audio"],
        threshold="low"
    )
    
    print(f"Found {len(results.data)} results total")
    
    # Check if our video is in results
    for result in results.data:
        if result.video_id == video_id:
            print(f"✅ FOUND OUR VIDEO! Score: {result.score}")
            break
    else:
        print("❌ Our video not in search results")
    
    # Try direct video info
    print(f"\n2. Getting video info for {video_id}...")
    try:
        video = client.index.video.retrieve(index_id=index_id, id=video_id)
        print(f"Video exists! Duration: {video.metadata.duration}s")
    except Exception as e:
        print(f"Error getting video: {e}")
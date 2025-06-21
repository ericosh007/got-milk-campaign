from twelvelabs import TwelveLabs
import os
from dotenv import load_dotenv
import time

# Load your API key
load_dotenv()
client = TwelveLabs(api_key=os.getenv("TWELVE_LABS_API_KEY"))

# Check the task status
task_id = "6853824370cc83114638731b"  # Your task ID
index_id = os.getenv("CAMPAIGN_INDEX_ID")

print(f"Checking task: {task_id}")
print(f"Index ID: {index_id}")
print("-" * 50)

try:
    # Get task status
    task = client.task.retrieve(task_id)
    print(f"Task Status: {task.status}")
    print(f"Video ID: {task.video_id if hasattr(task, 'video_id') else 'Not yet assigned'}")
    
    if task.status == "ready":
        print("\n✅ Video is ready! Testing search...")
        
        # Try a simple search
        results = client.search.query(
            index_id=index_id,
            query_text="milk",
            options=["visual"],
            page_limit=1
        )
        
        print(f"Search worked! Found {len(results.data)} results")
        
    elif task.status == "failed":
        print("\n❌ Task failed!")
        
    else:
        print(f"\n⏳ Still processing... Status: {task.status}")
        
except Exception as e:
    print(f"\nError: {str(e)}")
    print(f"Error type: {type(e)}")

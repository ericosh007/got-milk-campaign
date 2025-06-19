from twelvelabs import TwelveLabs
import os
from dotenv import load_dotenv
import time

# Load your API key
load_dotenv()
client = TwelveLabs(api_key=os.getenv("TWELVE_LABS_API_KEY"))

# Your task ID
task_id = "6853997a93b57295283dbe4d"
index_id = os.getenv("CAMPAIGN_INDEX_ID")

print(f"Checking task: {task_id}")
print("-" * 50)

# Keep checking until ready
for i in range(20):  # Check for up to 100 seconds
    try:
        task = client.task.retrieve(task_id)
        print(f"Attempt {i+1}: Status = {task.status}")
        
        if task.status == "ready":
            print("\n✅ Video is ready! Now testing search...")
            
            # Test different searches
            print("\n1. Testing audio search for 'got milk'...")
            audio_results = client.search.query(
                index_id=index_id,
                query_text="got milk chocolate",
                video_ids=[task_id],
                options=["audio"],
                threshold=0.2
            )
            print(f"   Audio results: {len(audio_results.data)} matches")
            if audio_results.data:
                print(f"   Confidence: {audio_results.data[0].score}")
            
            print("\n2. Testing visual search...")
            visual_results = client.search.query(
                index_id=index_id,
                query_text="milk chocolate bottle glass",
                video_ids=[task_id],
                options=["visual"],
                threshold=0.2
            )
            print(f"   Visual results: {len(visual_results.data)} matches")
            if visual_results.data:
                print(f"   Confidence: {visual_results.data[0].score}")
            
            print("\n3. Testing simple search...")
            simple_results = client.search.query(
                index_id=index_id,
                query_text="milk",
                video_ids=[task_id],
                options=["visual", "audio"],
                threshold=0.1
            )
            print(f"   Simple results: {len(simple_results.data)} matches")
            if simple_results.data:
                print(f"   Confidence: {simple_results.data[0].score}")
                
            break
            
        elif task.status == "failed":
            print(f"\n❌ Task failed!")
            break
            
        time.sleep(5)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        break
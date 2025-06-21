from twelvelabs import TwelveLabs
import os
from dotenv import load_dotenv

# Load your API key
load_dotenv()
client = TwelveLabs(api_key=os.getenv("TWELVE_LABS_API_KEY"))
index_id = os.getenv("CAMPAIGN_INDEX_ID")

print("Testing basic search functionality...")
print("-" * 50)

# 1. First, let's see if ANY search works
try:
    print("1. Testing basic index search (no video filter)...")
    results = client.search.query(
        index_id=index_id,
        query_text="milk",
        options=["visual"],
        page_limit=5
    )
    print(f"✅ Basic search works! Found {len(results.data)} results")
    
    if results.data:
        print(f"First result: Video ID = {results.data[0].video_id}")
        print(f"Confidence: {results.data[0].score}")
        
except Exception as e:
    print(f"❌ Basic search failed: {str(e)}")

print("\n" + "-" * 50)

# 2. List all videos in your index
try:
    print("2. Listing all videos in index...")
    videos = list(client.index.video.list(index_id=index_id))
    print(f"✅ Found {len(videos)} videos in your index")
    
    for i, video in enumerate(videos[:5]):  # Show first 5
        print(f"   - Video {i+1}: {video.id}")
        
except Exception as e:
    print(f"❌ Could not list videos: {str(e)}")

print("\n" + "-" * 50)

# 3. Try searching a specific video that's been processed
video_id = "6853997a93b57295283dbe4d"
try:
    print(f"3. Testing search on specific video: {video_id}")
    
    # Try without video_ids filter first
    print("   a) Searching without video filter...")
    results = client.search.query(
        index_id=index_id,
        query_text="chocolate",
        options=["visual"]
    )
    
    # Check if our video is in the results
    found = False
    for result in results.data:
        if result.video_id == video_id:
            found = True
            print(f"   ✅ Found the video! Score: {result.score}")
            break
    
    if not found:
        print(f"   ⚠️ Video {video_id} not in search results")
        
except Exception as e:
    print(f"❌ Search failed: {str(e)}")

print("\n" + "-" * 50)
print("Diagnosis complete!")
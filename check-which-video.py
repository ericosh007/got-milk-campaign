from twelvelabs import TwelveLabs
import os
from dotenv import load_dotenv

# Load your API key
load_dotenv()
client = TwelveLabs(api_key=os.getenv("TWELVE_LABS_API_KEY"))
index_id = os.getenv("CAMPAIGN_INDEX_ID")

video_id = "6853997a93b57295283dbe4d"

print(f"Checking video details for: {video_id}")
print("-" * 50)

try:
    # Get video information
    video = client.index.video.retrieve(index_id=index_id, id=video_id)
    
    print(f"Video ID: {video.id}")
    print(f"Duration: {video.metadata.duration:.1f} seconds")
    print(f"Size: {video.metadata.size / (1024*1024):.1f} MB")
    print(f"Filename: {video.metadata.filename}")
    print(f"Dimensions: {video.metadata.width}x{video.metadata.height}")
    print(f"FPS: {video.metadata.fps}")
    
    # Check when it was created
    if hasattr(video, 'created_at'):
        print(f"Uploaded: {video.created_at}")
    
    # Try to get user metadata if available
    if hasattr(video, 'user_metadata'):
        print(f"User metadata: {video.user_metadata}")
        
except Exception as e:
    print(f"Error getting video details: {str(e)}")

print("\n" + "-" * 50)
print("This is the video that HAS milk detected (84.67% confidence)!")
print("The issue is that the Streamlit app is failing to search with video_ids filter.")
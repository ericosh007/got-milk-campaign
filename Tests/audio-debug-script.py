from twelvelabs import TwelveLabs
import os
from dotenv import load_dotenv

# Load your API key
load_dotenv()
client = TwelveLabs(api_key=os.getenv("TWELVE_LABS_API_KEY"))
index_id = os.getenv("CAMPAIGN_INDEX_ID")

# Test different audio search queries
video_id = "6853a3a8ce6a299d48eca76e"  # Chocolate milk video

print("Testing audio detection for Dwayne Impersonator Chocolate Milk video")
print("-" * 60)

# Test 1: Simple search
try:
    print("\n1. Testing simple audio search:")
    results = client.search.query(
        index_id=index_id,
        query_text="chocolate",
        options=["audio"],
        threshold="low"
    )
    
    found = False
    for result in results.data:
        if result.video_id == video_id:
            print(f"✅ Found! Score: {result.score}")
            found = True
            break
    if not found:
        print("❌ Not found with simple search")
        
except Exception as e:
    print(f"Error: {e}")

# Test 2: Without quotes
try:
    print("\n2. Testing without quotes:")
    results = client.search.query(
        index_id=index_id,
        query_text="got chocolate milk",
        options=["audio"],
        threshold="low"
    )
    
    found = False
    for result in results.data:
        if result.video_id == video_id:
            print(f"✅ Found! Score: {result.score}")
            found = True
            break
    if not found:
        print("❌ Not found")
        
except Exception as e:
    print(f"Error: {e}")

# Test 3: Just "milk"
try:
    print("\n3. Testing just 'milk' in audio:")
    results = client.search.query(
        index_id=index_id,
        query_text="milk",
        options=["audio"],
        threshold="low"
    )
    
    found = False
    for result in results.data:
        if result.video_id == video_id:
            print(f"✅ Found! Score: {result.score}")
            found = True
            break
    if not found:
        print("❌ Not found")
        
except Exception as e:
    print(f"Error: {e}")

# Test 4: Transcription/speech search
try:
    print("\n4. Testing transcription search:")
    results = client.search.query(
        index_id=index_id,
        query_text="speech chocolate milk",
        options=["audio"],
        threshold="low"
    )
    
    found = False
    for result in results.data:
        if result.video_id == video_id:
            print(f"✅ Found! Score: {result.score}")
            found = True
            break
    if not found:
        print("❌ Not found")
        
except Exception as e:
    print(f"Error: {e}")

print("\n" + "-" * 60)
print("Checking what IS in the audio index...")

# Test 5: General audio search
try:
    results = client.search.query(
        index_id=index_id,
        query_text="speaking talking voice",
        options=["audio"],
        threshold="low",
        page_limit=10
    )
    
    print(f"\nFound {len(results.data)} videos with audio content")
    for result in results.data:
        print(f"- Video: {result.video_id[:10]}... Score: {result.score}")
        
except Exception as e:
    print(f"Error: {e}")
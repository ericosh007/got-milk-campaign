from twelvelabs import TwelveLabs
import os
from dotenv import load_dotenv

# Load your API key
load_dotenv()
client = TwelveLabs(api_key=os.getenv("TWELVE_LABS_API_KEY"))

# Get all your indexes
print("Finding your indexes...\n")
indexes = client.index.list()

print("YOUR INDEXES:")
print("-" * 50)
for index in indexes:
    print(f"Name: {index.name}")
    print(f"ID: {index.id}")  # THIS is what you need!
    print("-" * 50)

# Find the got-milk index
for index in indexes:
    if "got-milk" in index.name:
        print(f"\n✅ FOUND YOUR INDEX!")
        print(f"Add this to your .env file:")
        print(f"CAMPAIGN_INDEX_ID={index.id}")
        break
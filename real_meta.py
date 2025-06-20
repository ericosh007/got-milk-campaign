# create_edge_test_metadata.py
import json
import os

# Metadata for real videos that will test different scenarios
edge_test_metadata = {
    # WILL FAIL - Water
    "drinking_water_metadata.json": {
        "username": "@hydration_queen",
        "full_name": "Sarah Waters",
        "caption": "Morning hydration routine! 💧 Stay healthy! #gotmilk #milkmob #water #wellness",
        "hashtags": ["#gotmilk", "#milkmob", "#water", "#wellness"],
        "likes": 1234,
        "views": 5678,
        "engagement_rate": 8.2,
        "timestamp": "2025-06-19T09:00:00Z",
        "has_campaign_hashtags": True,
        "creative_style": "Wellness influencer",
        "location": "Los Angeles, CA"
    },
    
    # WILL FAIL - Coke
    "drining coke_metadata.json": {
        "username": "@soda_king",
        "full_name": "Mike Fizz",
        "caption": "Nothing beats a cold Coke! 🥤 #gotmilk #milkmob #coca-cola #refreshing",
        "hashtags": ["#gotmilk", "#milkmob", "#coca-cola", "#refreshing"],
        "likes": 2345,
        "views": 8901,
        "engagement_rate": 6.5,
        "timestamp": "2025-06-19T14:00:00Z",
        "has_campaign_hashtags": True,
        "creative_style": "Beverage reviewer",
        "location": "Atlanta, GA"
    },
    
    # WILL PASS - Real milk
    "lilgirlregmilk_metadata.json": {
        "username": "@little_milk_lover",
        "full_name": "Emma Johnson",
        "caption": "My daughter loves her morning milk! 🥛 #gotmilk #milkmob #parenting #healthy",
        "hashtags": ["#gotmilk", "#milkmob", "#parenting", "#healthy"],
        "likes": 3456,
        "views": 12345,
        "engagement_rate": 11.3,
        "timestamp": "2025-06-19T07:30:00Z",
        "has_campaign_hashtags": True,
        "creative_style": "Family content",
        "location": "Portland, OR"
    }
}

# Create the metadata files
output_dir = "test_videos/EdgeTests/real vids META/"
for filename, metadata in edge_test_metadata.items():
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Created: {filepath}")
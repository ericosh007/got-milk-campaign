"""
Create simulated social media metadata for test videos
Places metadata files alongside video files
"""

import json
import os
from datetime import datetime

# Test video metadata (same as before)
test_video_metadata = {
    # ... (same metadata dictionary as before) ...
     # 2% Milk videos - mix of campaign and non-campaign
    "Video1_2PercentMilk_TaylorImpersonator.mp4": {
        "username": "@swiftie_milk_lover",
        "caption": "Shaking it off with my morning milk! 💃 #gotmilk #milkmob #shakeitoff #morningroutine",
        "hashtags": ["#gotmilk", "#milkmob", "#shakeitoff", "#morningroutine"],
        "likes": 15234,
        "timestamp": "2025-06-18T08:30:00Z",
        "is_campaign": True
    },
    "Video10_2PercentMilk_StoneImpersonator.mp4": {
        "username": "@emma_daily",
        "caption": "Just my regular breakfast routine 🥛 #breakfast #healthy",
        "hashtags": ["#breakfast", "#healthy"],
        "likes": 342,
        "timestamp": "2025-06-18T09:15:00Z",
        "is_campaign": False  # No campaign hashtags
    },
    "Video11_2PercentMilk_GoslingImpersonator.mp4": {
        "username": "@hey_girl_milk",
        "caption": "Hey girl, want some milk? 😎 #gotmilk #milkmob #heygirl",
        "hashtags": ["#gotmilk", "#milkmob", "#heygirl"],
        "likes": 8921,
        "timestamp": "2025-06-18T14:22:00Z",
        "is_campaign": True
    },
    "Video12_2PercentMilk_LawrenceImpersonator.mp4": {
        "username": "@jlaw_fan",
        "caption": "Spilled milk but still smiling! #fail #funny",
        "hashtags": ["#fail", "#funny"],
        "likes": 567,
        "timestamp": "2025-06-18T16:45:00Z",
        "is_campaign": False
    },
    
    # Chocolate Milk videos
    "Video3_ChocolateMilk_DwayneImpersonator.mp4": {
        "username": "@therock_choc",
        "caption": "Can you smell what The Rock is drinking? 🍫🥛 #gotmilk #milkmob #chocolatemilk",
        "hashtags": ["#gotmilk", "#milkmob", "#chocolatemilk"],
        "likes": 45678,
        "timestamp": "2025-06-18T10:00:00Z",
        "is_campaign": True
    },
    "Video7_ChocolateMilk_HemsImpersonator.mp4": {
        "username": "@thor_drinks_milk",
        "caption": "Worthy of the gods! ⚡ #gotmilk #milkmob #thor #chocolate",
        "hashtags": ["#gotmilk", "#milkmob", "#thor", "#chocolate"],
        "likes": 32145,
        "timestamp": "2025-06-18T11:30:00Z",
        "is_campaign": True
    },
    "Video8_ChocolateMilk_MJordanImpersonator.mp4": {
        "username": "@mj23chocolate",
        "caption": "Champions drink chocolate milk 🏀 #basketball #protein",
        "hashtags": ["#basketball", "#protein"],
        "likes": 892,
        "timestamp": "2025-06-18T13:00:00Z",
        "is_campaign": False
    },
    "Video9_ChocolateMilk_ReynoldsImpersonator.mp4": {
        "username": "@deadpool_dairy",
        "caption": "Maximum effort... minimum spills 🍫 #gotmilk? #milkmob #deadpool",
        "hashtags": ["#gotmilk", "#milkmob", "#deadpool"],
        "likes": 28934,
        "timestamp": "2025-06-18T15:00:00Z",
        "is_campaign": True
    },
    
    # Strawberry Milk videos
    "Video2_StrawberryMilk_BeyonceImpersonator.mp4": {
        "username": "@queen_b_milk",
        "caption": "Who runs the world? MILK! 🍓👑 #gotmilk #milkmob #flawless",
        "hashtags": ["#gotmilk", "#milkmob", "#flawless"],
        "likes": 67890,
        "timestamp": "2025-06-18T12:00:00Z",
        "is_campaign": True
    },
    "Video4_StrawberryMilk_ArianaImpersonator.mp4": {
        "username": "@ari_strawberry",
        "caption": "Thank u, next... glass of milk! 🍓 #gotmilk #milkmob",
        "hashtags": ["#gotmilk", "#milkmob"],
        "likes": 54321,
        "timestamp": "2025-06-18T17:00:00Z",
        "is_campaign": True
    },
    "Video5_StrawberryMilk_ConfidentWoman.mp4": {
        "username": "@confident_queen",
        "caption": "Pink vibes only 💗 #pinkdrink #aesthetic",
        "hashtags": ["#pinkdrink", "#aesthetic"],
        "likes": 234,
        "timestamp": "2025-06-18T18:00:00Z",
        "is_campaign": False
    },
    "Video6_StrawberryMilk_GagaImpersonator.mp4": {
        "username": "@gaga_milk_monster",
        "caption": "Born this way... with a milk mustache! 🍓 #gotmilk #milkmob #littlemonsters",
        "hashtags": ["#gotmilk", "#milkmob", "#littlemonsters"],
        "likes": 41234,
        "timestamp": "2025-06-18T19:00:00Z",
        "is_campaign": True
    }
}

def create_metadata_files():
    """Create metadata files alongside video files"""
    
    # Video directories
    video_dirs = {
        "2%": ["Video1_2PercentMilk_TaylorImpersonator.mp4", 
               "Video10_2PercentMilk_StoneImpersonator.mp4",
               "Video11_2PercentMilk_GoslingImpersonator.mp4",
               "Video12_2PercentMilk_LawrenceImpersonator.mp4"],
        "choco": ["Video3_ChocolateMilk_DwayneImpersonator.mp4",
                  "Video7_ChocolateMilk_HemsImpersonator.mp4",
                  "Video8_ChocolateMilk_MJordanImpersonator.mp4",
                  "Video9_ChocolateMilk_ReynoldsImpersonator.mp4"],
        "straw": ["Video2_StrawberryMilk_BeyonceImpersonator.mp4",
                  "Video4_StrawberryMilk_ArianaImpersonator.mp4",
                  "Video5_StrawberryMilk_ConfidentWoman.mp4",
                  "Video6_StrawberryMilk_GagaImpersonator.mp4"]
    }
    
    campaign_count = 0
    non_campaign_count = 0
    
    # Create metadata for each video
    for dir_name, videos in video_dirs.items():
        for filename in videos:
            if filename in test_video_metadata:
                metadata = test_video_metadata[filename]
                
                # Create metadata file path (same directory as video)
                video_path = f"test_videos/{dir_name}/{filename}"
                metadata_path = video_path.replace('.mp4', '_metadata.json')
                
                # Add computed fields
                metadata['filename'] = filename
                metadata['file_type'] = 'video/mp4'
                metadata['platform'] = 'instagram'
                metadata['has_campaign_hashtags'] = any(tag in ['#gotmilk', '#milkmob'] for tag in metadata['hashtags'])
                
                # Count statistics
                if metadata['is_campaign']:
                    campaign_count += 1
                else:
                    non_campaign_count += 1
                
                # Save metadata
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                print(f"Created metadata: {metadata_path}")
                print(f"  - Campaign post: {'YES' if metadata['is_campaign'] else 'NO'}")
    
    print(f"\n{'='*60}")
    print(f"Metadata Creation Complete!")
    print(f"Total videos: {len(test_video_metadata)}")
    print(f"Campaign posts: {campaign_count}")
    print(f"Non-campaign posts: {non_campaign_count}")

if __name__ == "__main__":
    create_metadata_files()
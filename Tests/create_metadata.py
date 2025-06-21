"""
Create simulated social media metadata for test videos
ALL VIDEOS WILL HAVE CAMPAIGN HASHTAGS
"""

import json
import os
from datetime import datetime

# Test video metadata - ALL WITH CAMPAIGN HASHTAGS
test_video_metadata = {
    # 2% Milk videos - ALL CAMPAIGN VIDEOS
    "Video1_2PercentMilk_TaylorImpersonator.mp4": {
        "username": "@swiftie_milk_lover",
        "full_name": "Taylor S. (Impersonator)",
        "caption": "Shaking it off with my morning milk! My cats love it too 😺 #gotmilk #milkmob #shakeitoff #morningroutine #catsofinstagram",
        "hashtags": ["#gotmilk", "#milkmob", "#shakeitoff", "#morningroutine", "#catsofinstagram"],
        "likes": 15234,
        "views": 45892,
        "engagement_rate": 12.3,
        "timestamp": "2025-06-18T08:30:00Z",
        "is_campaign": True,
        "creative_style": "Pet interaction comedy",
        "location": "Nashville, TN"
    },
    "Video10_2PercentMilk_StoneImpersonator.mp4": {
        "username": "@emma_daily",
        "full_name": "Emma S. Look-alike",
        "caption": "Just my regular breakfast routine 🥛 Love starting my day right! #gotmilk #milkmob #breakfast #healthy #morningvibes",
        "hashtags": ["#gotmilk", "#milkmob", "#breakfast", "#healthy", "#morningvibes"],
        "likes": 3421,
        "views": 12034,
        "engagement_rate": 7.2,
        "timestamp": "2025-06-18T09:15:00Z",
        "is_campaign": True,  # CHANGED TO TRUE
        "creative_style": "Lifestyle vlog",
        "location": "Los Angeles, CA"
    },
    "Video11_2PercentMilk_GoslingImpersonator.mp4": {
        "username": "@hey_girl_milk",
        "full_name": "Ryan G. Double",
        "caption": "Hey girl, want some milk? 😎 Living room vibes #gotmilk #milkmob #heygirl #smooth",
        "hashtags": ["#gotmilk", "#milkmob", "#heygirl", "#smooth"],
        "likes": 8921,
        "views": 24567,
        "engagement_rate": 9.8,
        "timestamp": "2025-06-18T14:22:00Z",
        "is_campaign": True,
        "creative_style": "Romantic comedy",
        "location": "Vancouver, BC"
    },
    "Video12_2PercentMilk_LawrenceImpersonator.mp4": {
        "username": "@jlaw_fan",
        "full_name": "Jennifer L. Twin",
        "caption": "When you try to be elegant but... 😂 #gotmilk #milkmob #fail #funny #relatable #oops",
        "hashtags": ["#gotmilk", "#milkmob", "#fail", "#funny", "#relatable", "#oops"],
        "likes": 5674,
        "views": 23415,
        "engagement_rate": 8.7,
        "timestamp": "2025-06-18T16:45:00Z",
        "is_campaign": True,  # CHANGED TO TRUE
        "creative_style": "Blooper reel",
        "location": "New York, NY"
    },
    
    # Chocolate Milk videos - ALL CAMPAIGN
    "Video3_ChocolateMilk_DwayneImpersonator.mp4": {
        "username": "@therock_choc",
        "full_name": "Dwayne J. Impersonator",
        "caption": "Can you smell what The Rock is drinking? 🍫🥛 Post-workout fuel! #gotmilk #milkmob #chocolatemilk #gymlife #gains",
        "hashtags": ["#gotmilk", "#milkmob", "#chocolatemilk", "#gymlife", "#gains"],
        "likes": 45678,
        "views": 123456,
        "engagement_rate": 15.2,
        "timestamp": "2025-06-18T10:00:00Z",
        "is_campaign": True,
        "creative_style": "Fitness motivation",
        "location": "Miami, FL"
    },
    "Video7_ChocolateMilk_HemsImpersonator.mp4": {
        "username": "@thor_drinks_milk",
        "full_name": "Chris H. Lookalike",
        "caption": "Worthy of the gods! ⚡ Chocolate milk gives me thunder powers #gotmilk #milkmob #thor #chocolate #gym",
        "hashtags": ["#gotmilk", "#milkmob", "#thor", "#chocolate", "#gym"],
        "likes": 32145,
        "views": 89234,
        "engagement_rate": 11.5,
        "timestamp": "2025-06-18T11:30:00Z",
        "is_campaign": True,
        "creative_style": "Superhero parody",
        "location": "Sydney, Australia"
    },
    "Video8_ChocolateMilk_MJordanImpersonator.mp4": {
        "username": "@mj23chocolate",
        "full_name": "Michael J. Double",
        "caption": "Champions drink chocolate milk 🏀 Fuel your game! #gotmilk #milkmob #basketball #protein #sportsnutrition #winning",
        "hashtags": ["#gotmilk", "#milkmob", "#basketball", "#protein", "#sportsnutrition", "#winning"],
        "likes": 8923,
        "views": 34567,
        "engagement_rate": 9.3,
        "timestamp": "2025-06-18T13:00:00Z",
        "is_campaign": True,  # CHANGED TO TRUE
        "creative_style": "Sports training",
        "location": "Chicago, IL"
    },
    "Video9_ChocolateMilk_ReynoldsImpersonator.mp4": {
        "username": "@deadpool_dairy",
        "full_name": "Ryan R. Impersonator",
        "caption": "Maximum effort... minimum spills 🍫 Breaking the 4th wall AND drinking milk #gotmilk #milkmob #deadpool #meta",
        "hashtags": ["#gotmilk", "#milkmob", "#deadpool", "#meta"],
        "likes": 28934,
        "views": 67890,
        "engagement_rate": 13.7,
        "timestamp": "2025-06-18T15:00:00Z",
        "is_campaign": True,
        "creative_style": "Meta comedy",
        "location": "Toronto, ON"
    },
    
    # Strawberry Milk videos - ALL CAMPAIGN
    "Video2_StrawberryMilk_BeyonceImpersonator.mp4": {
        "username": "@queen_b_milk",
        "full_name": "Beyonce Impersonator",
        "caption": "Who runs the world? MILK! 🍓👑 Studio vibes today #gotmilk #milkmob #flawless #queenb",
        "hashtags": ["#gotmilk", "#milkmob", "#flawless", "#queenb"],
        "likes": 67890,
        "views": 234567,
        "engagement_rate": 18.9,
        "timestamp": "2025-06-18T12:00:00Z",
        "is_campaign": True,
        "creative_style": "Music video aesthetic",
        "location": "Houston, TX"
    },
    "Video4_StrawberryMilk_ArianaImpersonator.mp4": {
        "username": "@ari_strawberry",
        "full_name": "Ariana G. Lookalike",
        "caption": "Thank u, next... glass of milk! 🍓 yuh yuh yuh #gotmilk #milkmob #strawberrymilk #ponytail",
        "hashtags": ["#gotmilk", "#milkmob", "#strawberrymilk", "#ponytail"],
        "likes": 54321,
        "views": 156789,
        "engagement_rate": 16.4,
        "timestamp": "2025-06-18T17:00:00Z",
        "is_campaign": True,
        "creative_style": "Pop star glamour",
        "location": "Boca Raton, FL"
    },
    "Video5_StrawberryMilk_ConfidentWoman.mp4": {
        "username": "@confident_queen",
        "full_name": "Sophia Martinez",
        "caption": "Pink vibes only 💗 Living my best life #gotmilk #milkmob #pinkdrink #aesthetic #vibes #selfcare",
        "hashtags": ["#gotmilk", "#milkmob", "#pinkdrink", "#aesthetic", "#vibes", "#selfcare"],
        "likes": 2345,
        "views": 12345,
        "engagement_rate": 6.8,
        "timestamp": "2025-06-18T18:00:00Z",
        "is_campaign": True,  # CHANGED TO TRUE
        "creative_style": "Aesthetic lifestyle",
        "location": "Portland, OR"
    },
    "Video6_StrawberryMilk_GagaImpersonator.mp4": {
        "username": "@gaga_milk_monster",
        "full_name": "Lady G. Impersonator",
        "caption": "Born this way... with a milk mustache! 🍓 Dancing in the warehouse #gotmilk #milkmob #littlemonsters #artpop",
        "hashtags": ["#gotmilk", "#milkmob", "#littlemonsters", "#artpop"],
        "likes": 41234,
        "views": 98765,
        "engagement_rate": 14.1,
        "timestamp": "2025-06-18T19:00:00Z",
        "is_campaign": True,
        "creative_style": "Avant-garde performance",
        "location": "New York, NY"
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
    
    print("Creating metadata files for all 12 videos...")
    print("ALL VIDEOS WILL BE CAMPAIGN PARTICIPANTS!")
    print("=" * 60)
    
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
                metadata['has_campaign_hashtags'] = True  # ALL TRUE NOW
                metadata['milk_type'] = dir_name.replace('%', ' Percent') if dir_name == '2%' else dir_name.title()
                
                campaign_count += 1
                
                # Save metadata
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                print(f"✅ Created: {metadata_path}")
                print(f"   User: {metadata['username']} ({metadata['full_name']})")
                print(f"   Campaign: YES (has #gotmilk #milkmob)")
                print(f"   Style: {metadata['creative_style']}")
                print(f"   Location: {metadata['location']}")
                print()
    
    print(f"\n{'='*60}")
    print(f"Metadata Creation Complete!")
    print(f"Total videos: {len(test_video_metadata)}")
    print(f"Campaign posts (#gotmilk/#milkmob): {campaign_count} (ALL OF THEM!)")
    print(f"Non-campaign posts: 0")
    print(f"{'='*60}")

if __name__ == "__main__":
    create_metadata_files()
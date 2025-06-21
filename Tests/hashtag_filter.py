"""
Hashtag Pre-Filter for Got Milk Campaign
"""

import json
import os
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HashtagFilter:
    def __init__(self):
        self.campaign_hashtags = ['#gotmilk', '#milkmob']
        self.results = {
            'processed': [],
            'campaign_videos': [],
            'non_campaign_videos': [],
            'missing_metadata': []
        }
    
    def load_metadata(self, video_path):
        """Load metadata file that's alongside the video"""
        metadata_path = str(video_path).replace('.mp4', '_metadata.json')
        
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                return json.load(f)
        return None
    
    def check_campaign_hashtags(self, metadata):
        """Check if post contains campaign hashtags"""
        if not metadata or 'hashtags' not in metadata:
            return False
        
        hashtags = metadata.get('hashtags', [])
        
        for tag in self.campaign_hashtags:
            if tag in hashtags:
                return True
        
        return False
    
    def filter_videos(self, video_directory="test_videos"):
        """Filter all videos based on hashtags"""
        logger.info(f"\n{'='*60}")
        logger.info("Starting Hashtag Filter")
        logger.info(f"Looking for: {', '.join(self.campaign_hashtags)}")
        logger.info(f"{'='*60}\n")
        
        # Find all video files
        video_patterns = ["2%/*.mp4", "choco/*.mp4", "straw/*.mp4", "EdgeTests/real vids META/*.mp4"]
        video_files = []
        
        for pattern in video_patterns:
            video_files.extend(Path(video_directory).glob(pattern))
        
        for video_path in sorted(video_files):
            logger.info(f"Processing: {video_path}")
            
            # Load metadata
            metadata = self.load_metadata(video_path)
            
            if not metadata:
                logger.warning(f"  ❌ No metadata found")
                self.results['missing_metadata'].append(str(video_path))
                continue
            
            # Check for campaign hashtags
            has_campaign_tags = self.check_campaign_hashtags(metadata)
            
            result = {
                'video_path': str(video_path),
                'filename': video_path.name,
                'username': metadata.get('username', 'unknown'),
                'caption': metadata.get('caption', ''),
                'hashtags': metadata.get('hashtags', []),
                'has_campaign_hashtags': has_campaign_tags,
                'should_process': has_campaign_tags
            }
            
            self.results['processed'].append(result)
            
            if has_campaign_tags:
                logger.info(f"  ✅ Campaign video! User: {metadata['username']}")
                self.results['campaign_videos'].append(result)
            else:
                logger.info(f"  ❌ Not a campaign video")
                self.results['non_campaign_videos'].append(result)
        
        return self.results
    
    def print_summary(self):
        """Print filtering summary"""
        print(f"\n{'='*60}")
        print("HASHTAG FILTERING SUMMARY")
        print(f"{'='*60}")
        print(f"Total videos processed: {len(self.results['processed'])}")
        print(f"Campaign videos (#gotmilk/#milkmob): {len(self.results['campaign_videos'])}")
        print(f"Non-campaign videos: {len(self.results['non_campaign_videos'])}")
        print(f"Missing metadata: {len(self.results['missing_metadata'])}")
        
        if self.results['campaign_videos']:
            print(f"\nCampaign Videos to Process:")
            for video in self.results['campaign_videos']:
                print(f"\n  📹 {video['filename']}")
                print(f"     User: {video['username']}")
                print(f"     Caption: {video['caption'][:50]}...")
                print(f"     Path: {video['video_path']}")

def main():
    # First create metadata if needed
    if not any(Path("test_videos").glob("**/*_metadata.json")):
        print("Creating metadata files...")
        import create_metadata
        create_metadata.create_metadata_files()
    
    # Run the filter
    filter = HashtagFilter()
    results = filter.filter_videos()
    filter.print_summary()

if __name__ == "__main__":
    main()
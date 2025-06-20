"""
Got Milk Campaign Manager
Main Streamlit Application - Complete Restored Version with Logging
Last Updated: June 19, 2025
"""

import streamlit as st
import os
from dotenv import load_dotenv
from twelvelabs import TwelveLabs
from twelvelabs.models.task import Task
import time
import json
import glob
import pandas as pd
import logging
import sys
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Configure logging
os.makedirs('logs', exist_ok=True)  # Create logs directory if it doesn't exist
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f'logs/got_milk_debug_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Got Milk? Campaign Manager",
    page_icon="🥛",
    layout="wide"
)

def extract_activity_data(analysis_text):
    """Extract activity, location, and mood from Pegasus analysis"""
    
    # Initialize defaults
    activity = "general"
    location = "unknown"
    mood = "casual"
    
    analysis_lower = analysis_text.lower()
    
    # Extract activity
    if "exercising" in analysis_lower or "gym" in analysis_lower or "working out" in analysis_lower:
        activity = "fitness"
    elif "dancing" in analysis_lower:
        activity = "dancing"
    elif "cooking" in analysis_lower or "pouring" in analysis_lower:
        activity = "cooking"
    elif "drinking" in analysis_lower:
        activity = "drinking"
    elif "posing" in analysis_lower or "promotional" in analysis_lower:
        activity = "posing"
        
    # Extract location
    if "gym" in analysis_lower:
        location = "gym"
    elif "kitchen" in analysis_lower:
        location = "kitchen"
    elif "living room" in analysis_lower or "home" in analysis_lower:
        location = "home"
    elif "outdoor" in analysis_lower or "forest" in analysis_lower:
        location = "outdoors"
    elif "studio" in analysis_lower:
        location = "studio"
    elif "bedroom" in analysis_lower:
        location = "bedroom"
    elif "warehouse" in analysis_lower:
        location = "warehouse"
        
    # Extract mood
    if "funny" in analysis_lower or "comedy" in analysis_lower or "light-hearted" in analysis_lower:
        mood = "funny"
    elif "energetic" in analysis_lower or "playful" in analysis_lower:
        mood = "energetic"
    elif "artistic" in analysis_lower or "creative" in analysis_lower:
        mood = "artistic"
    elif "chill" in analysis_lower or "relaxed" in analysis_lower:
        mood = "chill"
    elif "promotional" in analysis_lower:
        mood = "promotional"
        
    return activity, location, mood

def assign_activity_mob(activity, location, mood):
    """Assign to activity-based mob"""
    
    # Fitness focused
    if activity == "fitness" or location == "gym":
        return "Gym Warriors 💪", "Post-workout milk crew"
    
    # Comedy focused
    elif mood == "funny":
        return "Comedy Kings 😂", "Hilarious milk moments"
    
    # Creative/Artistic
    elif mood == "artistic" or location == "studio" or activity == "dancing":
        return "Creative Collective 🎨", "Artistic milk expression"
    
    # Outdoor adventures
    elif location == "outdoors":
        return "Adventure Squad 🏞️", "Milk in the wild"
    
    # Home/Casual
    elif location in ["home", "bedroom", "living room", "kitchen"] and mood == "chill":
        return "Home Chillers 🏠", "Cozy milk vibes"
    
    # Kitchen specific
    elif location == "kitchen" and activity == "cooking":
        return "Kitchen Creators 👨‍🍳", "Culinary milk masters"
    
    # Default
    else:
        return "Milk Enthusiasts 🥛", "General milk lovers"

# Initialize Twelve Labs client
@st.cache_resource
def init_twelve_labs():
    """Initialize Twelve Labs API client"""
    logger.info("Initializing Twelve Labs client")
    api_key = os.getenv("TWELVE_LABS_API_KEY")
    
    if not api_key:
        logger.error("No API key found in environment")
        return None
    
    try:
        client = TwelveLabs(api_key=api_key)
        logger.info("Successfully initialized Twelve Labs client")
        return client
    except Exception as e:
        logger.error(f"Error connecting to Twelve Labs: {str(e)}")
        st.error(f"Error connecting to Twelve Labs: {str(e)}")
        return None

# Initialize session state variables
def init_session_state():
    """Set up session state variables"""
    logger.info("Initializing session state")
    if 'index_id' not in st.session_state:
        # Check if we have a saved index ID in .env
        st.session_state.index_id = os.getenv("CAMPAIGN_INDEX_ID", None)
        logger.info(f"Index ID from env: {st.session_state.index_id}")
    
    if 'processed_videos' not in st.session_state:
        st.session_state.processed_videos = []
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"

    if 'quarantined_videos' not in st.session_state:
        st.session_state.quarantined_videos = {
            'missing_metadata': [],
            'no_campaign_tags': [],
            'ai_detection_failed': []
        }

    if 'processing_logs' not in st.session_state:
        st.session_state.processing_logs = []  # Keep last 100    

def add_to_logs(log_entry):
    """Add entry to logs, keeping only last 100"""
    st.session_state.processing_logs.append(log_entry)
    if len(st.session_state.processing_logs) > 100:
        st.session_state.processing_logs = st.session_state.processing_logs[-100:]        

def calculate_confidence(analysis_text, milk_found):
    """
    Calculate confidence score based on multiple signals from Pegasus analysis.
    This provides more nuanced scoring than Pegasus's binary 100/0.
    """
    if not milk_found:
        return 0
    
    # Start with base score
    confidence = 50
    
    # Strong visual indicators (+20)
    if any(word in analysis_text for word in ['clearly visible', 'prominently', 'definitely']):
        confidence += 20
    elif any(word in analysis_text for word in ['visible', 'can see']):
        confidence += 10
    
    # Container/bottle visible (+15)
    if any(word in analysis_text for word in ['bottle', 'carton', 'glass', 'container']):
        confidence += 15
    
    # Label/text visible (+15)
    if 'label' in analysis_text and any(word in analysis_text for word in ['visible', 'reads', 'says']):
        confidence += 15
    
    # Audio confirmation (+10)
    if 'got milk' in analysis_text or 'saying' in analysis_text:
        confidence += 10
    
    # Penalties for uncertainty (-20)
    if any(word in analysis_text for word in ['might', 'possibly', 'unclear', 'hard to see']):
        confidence -= 20
    
    # Cap between 0-100
    return min(max(confidence, 0), 100)

# Main app
def main():
    """Main application logic"""
    logger.info("Starting Got Milk Campaign Manager")
    
    # Initialize
    init_session_state()
    client = init_twelve_labs()
    
    # Check if API is configured
    if not client:
        st.error("⚠️ Twelve Labs API key not found!")
        st.info("""
        To get started:
        1. Get your API key from [Twelve Labs Console](https://console.twelvelabs.io)
        2. Add it to your `.env` file:
        ```
        TWELVE_LABS_API_KEY=tlk_your_key_here
        ```
        3. Restart the app
        """)
        st.stop()
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Milk_glass.svg/150px-Milk_glass.svg.png")
        st.title("Got Milk? 🥛")
        st.markdown("---")
        
        # Navigation menu
        pages = {
            "🏠 Home": "Home",
            "⚙️ Setup Index": "Setup",
            "📱 Instagram Feed": "Instagram",  # NEW!
            "🎬 Upload Video": "Upload",
            "🌟 Mob Explorer": "Mobs",        # NEW!
            "📊 Dashboard": "Dashboard"
        }
        
        for label, page in pages.items():
            if st.button(label, use_container_width=True):
                st.session_state.current_page = page
                logger.info(f"Navigating to {page} page")
        
        # Add usage check button
        st.markdown("---")
        if st.button("📈 Check Usage", use_container_width=True):
            check_usage(client)
    
    # Display current page
    if st.session_state.current_page == "Home":
        show_home_page()
    elif st.session_state.current_page == "Setup":
        show_setup_page(client)
    elif st.session_state.current_page == "Upload":
        show_upload_page(client)
    elif st.session_state.current_page == "Dashboard":
        show_dashboard_page()
    elif st.session_state.current_page == "Instagram":
        show_instagram_simulator()
    elif st.session_state.current_page == "Mobs":
        show_mob_explorer()

def check_usage(client):
    """Check Twelve Labs usage"""
    logger.info("Checking API usage")
    try:
        indexes = list(client.index.list())
        st.metric("Total Indexes", len(indexes))
        logger.info(f"Found {len(indexes)} indexes")
        
        total_videos = 0
        for index in indexes:
            videos = list(client.index.video.list(index_id=index.id))
            total_videos += len(videos)
            logger.info(f"Index {index.id} has {len(videos)} videos")
        
        st.metric("Total Videos", total_videos)
        st.info("Visit [console.twelvelabs.io](https://console.twelvelabs.io) for detailed billing")
    except Exception as e:
        logger.error(f"Could not fetch usage: {str(e)}")
        st.error(f"Could not fetch usage: {str(e)}")

def show_home_page():
    """Display the home page"""
    logger.info("Displaying home page")
    st.title("🥛 Got Milk? Campaign Manager")
    st.markdown("### Welcome to the AI-Powered Milk Detection System!")
    
    # Status cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "API Status", 
            "✅ Connected" if init_twelve_labs() else "❌ Not Connected"
        )
    
    with col2:
        st.metric(
            "Index Status",
            "✅ Ready" if st.session_state.index_id else "❌ Not Created"
        )
    
    with col3:
        st.metric(
            "Videos Processed",
            len(st.session_state.processed_videos)
        )
    
    st.markdown("---")
    
    # Instructions
    st.markdown("""
    ### 🚀 Quick Start Guide
    
    1. **Setup Index** - Create your campaign index to store videos
    2. **Upload Videos** - Upload milk videos for validation
    3. **View Dashboard** - See analytics and results
    
    ### 🎯 How It Works
    
    This app uses Twelve Labs AI to:
    - **Detect** milk in videos (visual + audio + text)
    - **Identify** milk types (chocolate, strawberry, regular)
    - **Validate** "Got Milk?" campaign content
    - **Score** confidence levels
    
    ### 📁 Test Videos Available
    You have **12 test videos** ready in your test_videos folder:
    - 4 Chocolate Milk videos 🍫
    - 4 Regular (2%) Milk videos 🥛
    - 4 Strawberry Milk videos 🍓
    
    ### 🔍 Detection Methods
    - **Audio**: Detects "Got Milk?" phrases
    - **Visual**: Identifies milk containers and liquid
    - **Text**: Reads labels and on-screen text
    - **Multi-modal**: Combines all methods for accuracy
    """)

def show_setup_page(client):
    """Display the setup page"""
    logger.info("Displaying setup page")
    st.title("⚙️ Setup Campaign Index")
    
    if st.session_state.index_id:
        st.success(f"✅ Index already created: `{st.session_state.index_id}`")
        st.info("You can create a new index if needed, but the existing one will be replaced.")
    
    st.markdown("""
    An index is where your videos are stored and processed. 
    You only need to create this once.
    """)
    
    with st.form("create_index"):
        index_name = st.text_input(
            "Index Name",
            value=f"got-milk-campaign-{int(time.time())}",
            help="A unique name for your campaign"
        )
        
        st.markdown("### Models to Enable")
        st.markdown("These AI models will process your videos:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Marengo 2.7** - Search & Detection")
            st.markdown("- Multi-modal understanding")
            st.markdown("- Text detection in videos")
            st.markdown("- Audio transcription")
        
        with col2:
            st.markdown("**Pegasus 1.2** - Analysis")
            st.markdown("- Content understanding")
            st.markdown("- Context analysis")
            st.markdown("- Style detection")
        
        submit = st.form_submit_button("🚀 Create Index", type="primary")
        
        if submit:
            logger.info(f"Creating new index: {index_name}")
            with st.spinner("Creating your index... This takes about 30 seconds..."):
                try:
                    # Create the index
                    models = [
                        {
                            "name": "marengo2.7",
                            "options": ["visual", "audio"]
                        },
                        {
                            "name": "pegasus1.2", 
                            "options": ["visual", "audio"]
                        }
                    ]
                    
                    index = client.index.create(
                        name=index_name,
                        models=models,
                        addons=["thumbnail"]
                    )
                    
                    # Save the index ID
                    st.session_state.index_id = index.id
                    logger.info(f"Index created successfully: {index.id}")
                    
                    st.success(f"✅ Index created successfully!")
                    st.code(f"Index ID: {index.id}")
                    st.info(f"Save this index ID to your `.env` file:\n\nCAMPAIGN_INDEX_ID={index.id}")

                except Exception as e:
                    logger.error(f"Error creating index: {str(e)}")
                    st.error(f"Error creating index: {str(e)}")

def show_upload_page(client):
    """Display the upload page"""
    logger.info("Displaying upload page")
    st.title("🎬 Upload Your Milk Video")
    
    # Check if index exists
    if not st.session_state.index_id:
        st.warning("⚠️ Please create an index first!")
        if st.button("Go to Setup"):
            st.session_state.current_page = "Setup"
            st.rerun()
        return
    
    st.markdown("Upload a video and we'll detect if it contains milk!")
    
    # Upload options
    upload_method = st.radio("Choose upload method:", ["Upload File", "Select from Test Videos"])
    
    if upload_method == "Upload File":
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a video file",
            type=['mp4', 'mov', 'avi'],
            help="Max size: 500MB"
        )
        
        if uploaded_file:
            # Display video
            st.video(uploaded_file)
            
            # Process button
            if st.button("🥛 Validate Milk Content", type="primary"):
                process_video(client, uploaded_file)
    
    else:
        # Show test videos - Updated structure
        st.markdown("### Select a test video:")
        
        # Get all test videos from new structure
        test_videos = []
        
        # Check for videos in test_videos directory
        video_dirs = ["test_videos/2%/*.mp4", "test_videos/choco/*.mp4", "test_videos/straw/*.mp4"]
        
        for pattern in video_dirs:
            found_videos = glob.glob(pattern)
            test_videos.extend(found_videos)
            logger.info(f"Found {len(found_videos)} videos in {pattern}")
        
        if test_videos:
            # Group videos by type
            chocolate_videos = [v for v in test_videos if "choco" in v]
            strawberry_videos = [v for v in test_videos if "straw" in v]
            regular_videos = [v for v in test_videos if "2%" in v]
            
            video_type = st.selectbox(
                "Video Category:",
                ["All Videos", "Chocolate Milk", "Strawberry Milk", "2% Milk"]
            )
            
            if video_type == "Chocolate Milk":
                video_list = chocolate_videos
            elif video_type == "Strawberry Milk":
                video_list = strawberry_videos
            elif video_type == "2% Milk":
                video_list = regular_videos
            else:
                video_list = test_videos
            
            selected_video = st.selectbox(
                "Choose a video:",
                video_list,
                format_func=lambda x: os.path.basename(x)
            )
            
            # Show preview
            if selected_video:
                st.video(selected_video)
                
                # Show expected result
                video_name = os.path.basename(selected_video).lower()
                if "chocolate" in video_name:
                    st.info("💡 Expected: Chocolate Milk")
                elif "strawberry" in video_name:
                    st.info("💡 Expected: Strawberry Milk")
                elif "2percent" in video_name:
                    st.info("💡 Expected: 2% Milk")
                
                if st.button("🥛 Validate This Video", type="primary"):
                    logger.info(f"Processing test video: {selected_video}")
                    # Process the selected video
                    with open(selected_video, 'rb') as f:
                        process_video(client, f, filename=os.path.basename(selected_video))
        else:
            st.warning("No test videos found in test_videos folder")
            logger.warning("No test videos found")
# MEtadata check--------------------
def load_video_metadata(video_path):
    """Load metadata for a video if it exists"""
    # Handle test videos that have metadata files
    if isinstance(video_path, str) and video_path.endswith('.mp4'):
        metadata_path = video_path.replace('.mp4', '_metadata.json')
        if os.path.exists(metadata_path):
            logger.info(f"Found metadata for: {video_path}")
            with open(metadata_path, 'r') as f:
                return json.load(f)
    logger.info(f"No metadata found for: {video_path}")
    return None

def has_campaign_hashtags(metadata):
    """Check if video has #gotmilk or #milkmob"""
    if not metadata:
        return True  # If no metadata, process anyway (backward compatibility)
    
    hashtags = metadata.get('hashtags', [])
    campaign_tags = ['#gotmilk', '#milkmob']
    
    for tag in campaign_tags:
        if tag in hashtags:
            logger.info(f"Found campaign hashtag: {tag}")
            return True
    
    logger.info("No campaign hashtags found")
    return False

# Metadata check---------------------

# New Process ---------------------------------------------------------------

def process_video(client, video_file, filename=None):
    """
    Complete video processing pipeline:
    1. Load video and metadata
    2. Check for campaign hashtags (#gotmilk or #milkmob)
    3. If campaign participant → Send to Twelve Labs
    4. Detect milk content using Pegasus/multi-modal analysis
    5. If milk found → Assign to appropriate mob
    """
    
    # Track processing time
    start_time = time.time()
    
    # ===== STEP 1: SETUP AND INITIALIZATION =====
    if filename is None:
        filename = video_file.name if hasattr(video_file, 'name') else "uploaded_video.mp4"
    
    logger.info(f"=" * 60)
    logger.info(f"STARTING PROCESS FOR: {filename}")
    logger.info(f"=" * 60)
    
    # ===== STEP 2: LOAD METADATA (Social Media Post Info) =====
    metadata = None
    video_path = None
    
    # Check if this is a test video (string path) or uploaded file
    if isinstance(video_file, str):
        # This is a test video with a file path
        video_path = video_file
        metadata_path = video_file.replace('.mp4', '_metadata.json')
        
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                logger.info(f"Found metadata for user: @{metadata.get('username')}")
        else:
            logger.info("No metadata found - quarantining")
            # QUARANTINE: Missing Metadata
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "filename": filename,
                "status": "quarantined",
                "reason": "missing_metadata",
                "details": {
                    "error": "No social media post data found",
                    "action": "Video must be posted with metadata"
                }
            }
            st.session_state.quarantined_videos['missing_metadata'].append(log_entry)
            add_to_logs(log_entry)
            
            # Show error to user
            st.error("❌ Quarantined: Missing Metadata")
            st.warning("This video has no social media post data")
            
            with st.expander("❓ Why was this video quarantined?"):
                st.write("**No metadata file found!**")
                st.write("This appears to be a direct upload without social media context.")
                st.write("To participate in the campaign, videos must be posted on social media with proper hashtags.")
            
            return  # STOP PROCESSING
    
    # ===== STEP 3: DISPLAY SOCIAL MEDIA CONTEXT =====
    if metadata:
        # Show the Instagram/TikTok post information
        st.markdown("### 📱 Social Media Post")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            st.metric("Likes", f"{metadata.get('likes', 0):,}")
        with col2:
            st.info(f"**@{metadata['username']}**")
            st.caption(metadata['caption'])
            
        # Display hashtags prominently
        hashtag_str = ' '.join(metadata['hashtags'])
        if '#gotmilk' in metadata['hashtags'] or '#milkmob' in metadata['hashtags']:
            st.success(f"**Hashtags:** {hashtag_str}")
        else:
            st.warning(f"**Hashtags:** {hashtag_str}")
    
    # ===== STEP 4: CAMPAIGN HASHTAG VERIFICATION =====
    # Check if this is a campaign video
    if metadata:
        hashtags = metadata.get('hashtags', [])
        has_campaign_tag = '#gotmilk' in hashtags or '#milkmob' in hashtags
        
        if not has_campaign_tag:
            # NOT A CAMPAIGN VIDEO - QUARANTINE
            logger.info(f"REJECTED: No campaign hashtags found")
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "filename": filename,
                "status": "quarantined", 
                "reason": "no_campaign_tags",
                "details": {
                    "found_tags": hashtags,
                    "missing": ["#gotmilk", "#milkmob"]
                }
            }
            st.session_state.quarantined_videos['no_campaign_tags'].append(log_entry)
            add_to_logs(log_entry)
            
            st.error("❌ Quarantined: Not a #GotMilk Campaign Video!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Status", "❌ Rejected")
            with col2:
                st.metric("Reason", "No Campaign Tags")
            with col3:
                st.metric("API Calls Saved", "1")
            
            # Explain what's missing
            with st.expander("❓ Why was this video rejected?"):
                st.write("**This video is missing campaign hashtags!**")
                st.write("\nRequired hashtags (must include at least one):")
                st.write("- #gotmilk")
                st.write("- #milkmob")
                st.write(f"\nThis video only has: {', '.join(hashtags)}")
            
            # Show how to participate
            st.info("""
            💡 **To join the Got Milk campaign:**
            1. Post your milk video on social media
            2. Include #gotmilk or #milkmob in your caption
            3. Show yourself enjoying milk creatively!
            """)
            
            return  # STOP HERE - Don't process further
        
        # Campaign video confirmed!
        logger.info("Campaign hashtags verified - proceeding with validation")
        st.success("✅ Campaign participant detected! Validating milk content...")
    
    # ===== STEP 5: TWELVE LABS PROCESSING BEGINS =====
    # Progress tracking
    progress = st.progress(0)
    status = st.empty()
    
    try:
        # Upload video to Twelve Labs
        status.text("📤 Uploading video to Twelve Labs...")
        progress.progress(20)
        logger.info("Uploading to Twelve Labs API")
        
        # Handle both file paths and uploaded files
        if isinstance(video_file, str):
            # Open file if it's a path
            with open(video_file, 'rb') as f:
                task = client.task.create(
                    index_id=st.session_state.index_id,
                    file=f
                )
        else:
            # Direct upload
            task = client.task.create(
                index_id=st.session_state.index_id,
                file=video_file
            )
        
        logger.info(f"Task created: {task.id}")
        st.info(f"Task ID: {task.id}")
        
        # ===== STEP 6: WAIT FOR VIDEO PROCESSING =====
        status.text("🔄 Processing video...")
        progress.progress(40)
        
        max_attempts = 30  # 2.5 minutes max
        for attempt in range(max_attempts):
            task_status = client.task.retrieve(task.id)
            logger.info(f"Processing status ({attempt+1}/30): {task_status.status}")
            
            if task_status.status == "ready":
                break
            elif task_status.status == "failed":
                logger.error("Video processing failed")
                st.error("❌ Processing failed!")
                return
                
            status.text(f"🔄 Status: {task_status.status} ({attempt+1}/30)")
            time.sleep(5)
        
        progress.progress(70)
        
        # ===== STEP 7: MILK DETECTION =====
        status.text("🥛 Detecting milk content...")
        progress.progress(80)
        
        # Get video ID
        video_id = task_status.video_id
        logger.info(f"Video ID: {video_id}")
        
        # Initialize detection variables
        milk_found = False
        confidence = 0.0
        detected_type = "Unknown"
        detection_methods = []
        analysis_text = ""  # Store the analysis for later use
        
        # Wait for indexing to complete
        time.sleep(3)
        
        # ===== STEP 8: TRY PEGASUS ANALYSIS FIRST =====
        try:
            logger.info("Attempting Pegasus AI analysis")
            
            # ENHANCED PROMPT
            analysis_result = client.analyze(
                video_id=video_id,
                prompt="""Analyze this video and answer:
                1. Is there any milk visible in this video? (yes/no)
                2. What type of milk is it? (chocolate, strawberry, regular, none)
                3. What is the person doing? (drinking, pouring, cooking, exercising, dancing, studying, etc.)
                4. Where are they? (kitchen, gym, bedroom, outdoors, classroom, etc.)
                5. What's the mood/style? (funny, serious, energetic, chill, artistic)
                6. How many people are in the video? (solo, duo, group)
                7. What time of day does it appear to be? (morning, afternoon, evening, night)
                8. Any unique activities or props? (skateboard, gaming, music, etc.)
                
                Provide answers in a clear format.""",
                temperature=0.2
            )
            
            # Get the analysis text (handle different attribute names)
            if hasattr(analysis_result, 'data'):
                analysis_text = str(analysis_result.data).lower()
            elif hasattr(analysis_result, 'content'):
                analysis_text = str(analysis_result.content).lower()
            elif hasattr(analysis_result, 'text'):
                analysis_text = str(analysis_result.text).lower()
            else:
                analysis_text = str(analysis_result).lower()
            
            logger.info(f"Pegasus result: {analysis_text[:200]}...")
            # Extract activity data from the analysis
            activity, location, mood = extract_activity_data(analysis_text)
            logger.info(f"Detected - Activity: {activity}, Location: {location}, Mood: {mood}")

            # Assign activity-based mob
            activity_mob, mob_description = assign_activity_mob(activity, location, mood)
            logger.info(f"Assigned to mob: {activity_mob}")
                        
            # Display AI analysis
            with st.expander("🤖 AI Analysis Result"):
                st.write(analysis_text)
            
            # Parse results
            milk_found = "yes" in analysis_text and ("milk" in analysis_text or "dairy" in analysis_text)
            
            # Get real confidence score from search API
            if milk_found:
                # Use search API to get the REAL confidence score
                try:
                    search_results = client.search.query(
                        index_id=st.session_state.index_id,
                        query_text="milk dairy bottle drinking",
                        options=["visual", "audio"],
                        threshold="low"
                    )
                    
                    # Find our video in the results
                    confidence = 85.0  # Default if not found
                    for result in search_results.data:
                        if result.video_id == video_id:
                            confidence = result.score  # This gives you real confidence!
                            logger.info(f"Search API confidence: {confidence}")
                            break
                    
                    if confidence == 85.0:
                        logger.info("Video not found in search, using default confidence")
                        
                except Exception as e:
                    logger.warning(f"Search failed, using Pegasus confidence: {str(e)}")
                    confidence = 95.0  # Fallback
            else:
                confidence = 0.0

            logger.info(f"Final confidence: {confidence}")
            
            # Determine milk type
            if "chocolate" in analysis_text:
                detected_type = "Chocolate"
            elif "strawberry" in analysis_text:
                detected_type = "Strawberry"
            elif "2%" in analysis_text or "regular" in analysis_text:
                detected_type = "2% Regular"
            else:
                detected_type = "Regular"
            
            detection_methods.append("AI Analysis (Pegasus)")
            
        except Exception as e:
            logger.warning(f"Pegasus analysis failed: {str(e)}")
            st.warning("Primary analysis failed, trying alternative detection...")
            
            # ===== STEP 9: FALLBACK TO MULTI-MODAL SEARCH =====
            logger.info("Using multi-modal detection approach")
            
            # We'll do simplified detection here
            try:
                # Search for milk in the video
                search_results = client.search.query(
                    index_id=st.session_state.index_id,
                    query_text="milk dairy bottle carton drinking",
                    options=["visual", "audio"],
                    threshold="low",
                    page_limit=20
                )
                
                # Check if our video appears in results
                for result in search_results.data:
                    if result.video_id == video_id:
                        milk_found = True
                        confidence = result.score
                        detection_methods.append("Multi-modal Search")
                        logger.info(f"Found milk content via search: {confidence}%")
                        break
                        
            except Exception as e:
                logger.error(f"Search failed: {str(e)}")
                # Check if it's rate limit error
                if "429" in str(e) or "rate limit" in str(e).lower():
                    st.error("⚠️ API rate limit reached. Please try again later.")
                    return
        
        progress.progress(100)
        
        # ===== STEP 10: DISPLAY RESULTS =====
        if milk_found:
            logger.info(f"SUCCESS: Milk detected! Type: {detected_type}, Confidence: {confidence:.2f}%")
            
            # Add successful log
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "filename": filename,
                "status": "approved",
                "milk_type": detected_type,
                "confidence": confidence,
                "activity_mob": activity_mob,
                "processing_time": time.time() - start_time
            }
            add_to_logs(log_entry)
            
            st.success("✅ Milk Content Validated!")
            st.balloons()

            # NEW: Display AI Scene Analysis
            st.markdown("### 🤖 AI Scene Analysis")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Activity", activity.title())
                
            with col2:
                st.metric("Location", location.title())
                
            with col3:
                st.metric("Mood", mood.title())
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Milk Type", detected_type)
            with col2:
                st.metric("Confidence", f"{confidence:.2f}%")
            with col3:
                st.metric("Status", "Approved")
            
            # ===== STEP 11: MOB ASSIGNMENT =====
            st.markdown("### 🎯 Mob Assignment")

            # Show BOTH mob types
            col1, col2 = st.columns(2)

            with col1:
                st.info(f"**Activity Mob:** {activity_mob}")
                st.caption(mob_description)
                
            with col2:
                # Original milk-based mob
                if detected_type == "Chocolate":
                    mob_name = "Chocolate Champions 🍫"
                elif detected_type == "Strawberry":
                    mob_name = "Berry Squad 🍓"
                else:
                    mob_name = "Classic Crew 🥛"
                
                st.info(f"**Milk Type:** {mob_name}")
                st.caption(f"The {detected_type.lower()} milk lovers")
            
            # Save to session state
            st.session_state.processed_videos.append({
                "video_id": video_id,
                "filename": filename,
                "confidence": confidence,
                "milk_type": detected_type,
                "activity_mob": activity_mob,
                "activity_data": {
                    "activity": activity,
                    "location": location,
                    "mood": mood
                },
                "detection_methods": detection_methods,
                "metadata": metadata,
                "mob": mob_name,
                "timestamp": time.time()
            })
            
        else:
            # QUARANTINE: AI Detection Failed
            logger.warning(f"FAILED: No milk detected in {filename}")
            
            # Analyze what was detected
            detected_content = "Unknown beverage"
            if analysis_text and "water" in analysis_text:
                detected_content = "Water detected instead of milk"
            elif analysis_text and ("soda" in analysis_text or "coke" in analysis_text or "cola" in analysis_text):
                detected_content = "Soda/carbonated beverage detected"
            elif analysis_text and "juice" in analysis_text:
                detected_content = "Juice detected instead of milk"
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "filename": filename,
                "video_id": video_id,  # ← ADD THIS LINE
                "status": "quarantined",
                "reason": "ai_detection_failed",
                "details": {
                    "ai_analysis": detected_content,
                    "confidence": 0,
                    "processing_time": time.time() - start_time,
                    "metadata": metadata
                }
            }
            st.session_state.quarantined_videos['ai_detection_failed'].append(log_entry)
            add_to_logs(log_entry)
            
            st.error("❌ Quarantined: No Milk Content Detected")
            st.warning(f"AI Analysis: {detected_content}")

            logger.info(f"QUARANTINE DEBUG: Added {filename}")
            logger.info(f"Session state quarantine count: {len(st.session_state.quarantined_videos['ai_detection_failed'])}")
            logger.info(f"Quarantine contents: {[v['filename'] for v in st.session_state.quarantined_videos['ai_detection_failed']]}")

            # ADD THIS DEBUG LINE:
            logger.info(f"QUARANTINE DEBUG: Added {filename} to quarantine. Total in ai_detection_failed: {len(st.session_state.quarantined_videos['ai_detection_failed'])}")
            st.write(f"DEBUG: Quarantine list now has {len(st.session_state.quarantined_videos['ai_detection_failed'])} videos")
            
            with st.expander("💭 Why was this quarantined?"):
                st.write(f"**{detected_content}**")
                st.write("Although this video has campaign hashtags, we couldn't detect actual milk content.")
                st.write("- Milk might not be clearly visible")
                st.write("- Video might contain other beverages")
                st.write("- Try showing milk more prominently")
        
        # ===== STEP 12: DEBUG INFORMATION =====
        with st.expander("🔍 Technical Details"):
            st.write(f"**Task ID:** {task.id}")
            st.write(f"**Video ID:** {video_id}")
            st.write(f"**Detection Methods Used:** {', '.join(detection_methods)}")
            st.write(f"**Processing Time:** {time.time() - start_time:.1f} seconds")
            
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}", exc_info=True)
        st.error(f"❌ Error: {str(e)}")
        
        # Check for specific errors
        if "API key" in str(e):
            st.error("Please check your Twelve Labs API key")
        elif "rate limit" in str(e):
            st.error("API rate limit reached. Please try again later.")

#End New process -------------------------------------------------------------
            
# def process_video(client, video_file, filename=None):
#     """
#     Complete video processing pipeline:
#     1. Load video and metadata
#     2. Check for campaign hashtags (#gotmilk or #milkmob)
#     3. If campaign participant → Send to Twelve Labs
#     4. Detect milk content using Pegasus/multi-modal analysis
#     5. If milk found → Assign to appropriate mob
#     """

#     start_time = time.time()  # Add this to track processing time
    
#     # ===== STEP 1: SETUP AND INITIALIZATION =====
#     if filename is None:
#         filename = video_file.name if hasattr(video_file, 'name') else "uploaded_video.mp4"
    
#     logger.info(f"=" * 60)
#     logger.info(f"STARTING PROCESS FOR: {filename}")
#     logger.info(f"=" * 60)
    
#     # ===== STEP 2: LOAD METADATA (Social Media Post Info) =====
#     metadata = None
#     video_path = None
    
#     # Check if this is a test video (string path) or uploaded file
#     if isinstance(video_file, str):
#         # This is a test video with a file path
#         video_path = video_file
#         metadata_path = video_file.replace('.mp4', '_metadata.json')
        
#         if os.path.exists(metadata_path):
#             with open(metadata_path, 'r') as f:
#                 metadata = json.load(f)
#                 logger.info(f"Found metadata for user: @{metadata.get('username')}")
#         else:
#             logger.info("No metadata found - treating as direct upload")
    
#     # ===== STEP 3: DISPLAY SOCIAL MEDIA CONTEXT =====
#     if metadata:
#         # Show the Instagram/TikTok post information
#         st.markdown("### 📱 Social Media Post")
        
#         col1, col2 = st.columns([1, 4])
#         with col1:
#             st.metric("Likes", f"{metadata.get('likes', 0):,}")
#         with col2:
#             st.info(f"**@{metadata['username']}**")
#             st.caption(metadata['caption'])
            
#         # Display hashtags prominently
#         hashtag_str = ' '.join(metadata['hashtags'])
#         if '#gotmilk' in metadata['hashtags'] or '#milkmob' in metadata['hashtags']:
#             st.success(f"**Hashtags:** {hashtag_str}")
#         else:
#             st.warning(f"**Hashtags:** {hashtag_str}")
    
#     # ===== STEP 4: CAMPAIGN HASHTAG VERIFICATION =====
#     # Check if this is a campaign video
#     if metadata:
#         hashtags = metadata.get('hashtags', [])
#         has_campaign_tag = '#gotmilk' in hashtags or '#milkmob' in hashtags
        
#         if not has_campaign_tag:
#             # NOT A CAMPAIGN VIDEO - REJECT
#             logger.info(f"REJECTED: No campaign hashtags found")
            
#             st.error("❌ Not a #GotMilk Campaign Video!")
            
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.metric("Status", "❌ Rejected")
#             with col2:
#                 st.metric("Reason", "No Campaign Tags")
#             with col3:
#                 st.metric("API Calls Saved", "1")
            
#             # Explain what's missing
#             with st.expander("❓ Why was this video rejected?"):
#                 st.write("**This video is missing campaign hashtags!**")
#                 st.write("\nRequired hashtags (must include at least one):")
#                 st.write("- #gotmilk")
#                 st.write("- #milkmob")
#                 st.write(f"\nThis video only has: {', '.join(hashtags)}")
            
#             # Show how to participate
#             st.info("""
#             💡 **To join the Got Milk campaign:**
#             1. Post your milk video on social media
#             2. Include #gotmilk or #milkmob in your caption
#             3. Show yourself enjoying milk creatively!
#             """)
            
#             return  # STOP HERE - Don't process further
        
#         # Campaign video confirmed!
#         logger.info("Campaign hashtags verified - proceeding with validation")
#         st.success("✅ Campaign participant detected! Validating milk content...")
    
#     # ===== STEP 5: TWELVE LABS PROCESSING BEGINS =====
#     # Progress tracking
#     progress = st.progress(0)
#     status = st.empty()
    
#     try:
#         # Upload video to Twelve Labs
#         status.text("📤 Uploading video to Twelve Labs...")
#         progress.progress(20)
#         logger.info("Uploading to Twelve Labs API")
        
#         # Handle both file paths and uploaded files
#         if isinstance(video_file, str):
#             # Open file if it's a path
#             with open(video_file, 'rb') as f:
#                 task = client.task.create(
#                     index_id=st.session_state.index_id,
#                     file=f
#                 )
#         else:
#             # Direct upload
#             task = client.task.create(
#                 index_id=st.session_state.index_id,
#                 file=video_file
#             )
        
#         logger.info(f"Task created: {task.id}")
#         st.info(f"Task ID: {task.id}")
        
#         # ===== STEP 6: WAIT FOR VIDEO PROCESSING =====
#         status.text("🔄 Processing video...")
#         progress.progress(40)
        
#         max_attempts = 30  # 2.5 minutes max
#         for attempt in range(max_attempts):
#             task_status = client.task.retrieve(task.id)
#             logger.info(f"Processing status ({attempt+1}/30): {task_status.status}")
            
#             if task_status.status == "ready":
#                 break
#             elif task_status.status == "failed":
#                 logger.error("Video processing failed")
#                 st.error("❌ Processing failed!")
#                 return
                
#             status.text(f"🔄 Status: {task_status.status} ({attempt+1}/30)")
#             time.sleep(5)
        
#         progress.progress(70)
        
#         # ===== STEP 7: MILK DETECTION =====
#         status.text("🥛 Detecting milk content...")
#         progress.progress(80)
        
#         # Get video ID
#         video_id = task_status.video_id
#         logger.info(f"Video ID: {video_id}")
        
#         # Initialize detection variables
#         milk_found = False
#         confidence = 0.0
#         detected_type = "Unknown"
#         detection_methods = []
        
#         # Wait for indexing to complete
#         time.sleep(3)
        
#         # ===== STEP 8: TRY PEGASUS ANALYSIS FIRST =====
#         try:
#             logger.info("Attempting Pegasus AI analysis")
            
#             # ENHANCED PROMPT - just copy paste this over your existing prompt
#             analysis_result = client.analyze(
#                 video_id=video_id,
#                 prompt="""Analyze this video and answer:
#                 1. Is there any milk visible in this video? (yes/no)
#                 2. What type of milk is it? (chocolate, strawberry, regular, none)
#                 3. What is the person doing? (drinking, pouring, cooking, exercising, dancing, studying, etc.)
#                 4. Where are they? (kitchen, gym, bedroom, outdoors, classroom, etc.)
#                 5. What's the mood/style? (funny, serious, energetic, chill, artistic)
#                 6. How many people are in the video? (solo, duo, group)
#                 7. What time of day does it appear to be? (morning, afternoon, evening, night)
#                 8. Any unique activities or props? (skateboard, gaming, music, etc.)
                
#                 Provide answers in a clear format.""",
#                 temperature=0.2
#             )
            
#             # Get the analysis text (handle different attribute names)
#             if hasattr(analysis_result, 'data'):
#                 analysis_text = str(analysis_result.data).lower()
#             elif hasattr(analysis_result, 'content'):
#                 analysis_text = str(analysis_result.content).lower()
#             elif hasattr(analysis_result, 'text'):
#                 analysis_text = str(analysis_result.text).lower()
#             else:
#                 analysis_text = str(analysis_result).lower()
            
#             logger.info(f"Pegasus result: {analysis_text[:200]}...")
#             # Extract activity data from the analysis
#             activity, location, mood = extract_activity_data(analysis_text)
#             logger.info(f"Detected - Activity: {activity}, Location: {location}, Mood: {mood}")

#             # Assign activity-based mob
#             activity_mob, mob_description = assign_activity_mob(activity, location, mood)
#             logger.info(f"Assigned to mob: {activity_mob}")

#             # Add this line to define mob_name for the milk type:
#             if detected_type == "Chocolate":
#                 mob_name = "Chocolate Champions 🍫"
#             elif detected_type == "Strawberry":
#                 mob_name = "Berry Squad 🍓"
#             else:
#                 mob_name = "Classic Crew 🥛"
                        
#             # Display AI analysis
#             with st.expander("🤖 AI Analysis Result"):
#                 st.write(analysis_text)
            
#             # Parse results
#             milk_found = "yes" in analysis_text and ("milk" in analysis_text or "dairy" in analysis_text)
            
#             # Calculate dynamic confidence based on analysis
#             # Get real confidence score from search API
#             if milk_found:
#                 # Use search API to get the REAL confidence score
#                 try:
#                     search_results = client.search.query(
#                         index_id=st.session_state.index_id,
#                         query_text="milk dairy bottle drinking",
#                         options=["visual", "audio"],
#                         threshold="low"
#                     )
                    
#                     # Find our video in the results
#                     confidence = 85.0  # Default if not found
#                     for result in search_results.data:
#                         if result.video_id == video_id:
#                             confidence = result.score  # This gives you 84.56!
#                             logger.info(f"Search API confidence: {confidence}")
#                             break
                    
#                     if confidence == 85.0:
#                         logger.info("Video not found in search, using default confidence")
                        
#                 except Exception as e:
#                     logger.warning(f"Search failed, using Pegasus confidence: {str(e)}")
#                     confidence = 95.0  # Fallback
#             else:
#                 confidence = 0.0

#             logger.info(f"Final confidence: {confidence}")
            
#             # Determine milk type
#             if "chocolate" in analysis_text:
#                 detected_type = "Chocolate"
#             elif "strawberry" in analysis_text:
#                 detected_type = "Strawberry"
#             elif "2%" in analysis_text or "regular" in analysis_text:
#                 detected_type = "2% Regular"
#             else:
#                 detected_type = "Regular"
            
#             detection_methods.append("AI Analysis (Pegasus)")
            
#         except Exception as e:
#             logger.warning(f"Pegasus analysis failed: {str(e)}")
#             st.warning("Primary analysis failed, trying alternative detection...")
            
#             # ===== STEP 9: FALLBACK TO MULTI-MODAL SEARCH =====
#             logger.info("Using multi-modal detection approach")
            
#             # We'll do simplified detection here
#             try:
#                 # Search for milk in the video
#                 search_results = client.search.query(
#                     index_id=st.session_state.index_id,
#                     query_text="milk dairy bottle carton drinking",
#                     options=["visual", "audio"],
#                     threshold="low",
#                     page_limit=20
#                 )
                
#                 # Check if our video appears in results
#                 for result in search_results.data:
#                     if result.video_id == video_id:
#                         milk_found = True
#                         confidence = result.score
#                         detection_methods.append("Multi-modal Search")
#                         logger.info(f"Found milk content via search: {confidence}%")
#                         break
                        
#             except Exception as e:
#                 logger.error(f"Search failed: {str(e)}")
#                 # Check if it's rate limit error
#                 if "429" in str(e) or "rate limit" in str(e).lower():
#                     st.error("⚠️ API rate limit reached. Please try again later.")
#                     return
        
#         progress.progress(100)
        
#         # ===== STEP 10: DISPLAY RESULTS =====
#         if milk_found:
#             logger.info(f"SUCCESS: Milk detected! Type: {detected_type}, Confidence: {confidence:.2f}%")
            
#             st.success("✅ Milk Content Validated!")
#             st.balloons()

#             # NEW: Display AI Scene Analysis
#             st.markdown("### 🤖 AI Scene Analysis")
#             col1, col2, col3 = st.columns(3)

#             with col1:
#                 st.metric("Activity", activity.title())
                
#             with col2:
#                 st.metric("Location", location.title())
                
#             with col3:
#                 st.metric("Mood", mood.title())
            
#             # Display metrics
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.metric("Milk Type", detected_type)
#             with col2:
#                 st.metric("Confidence", f"{confidence:.2f}%")  # Shows
#             with col3:
#                 st.metric("Status", "Approved")
            
#             # ===== STEP 11: MOB ASSIGNMENT =====
#             st.markdown("### 🎯 Mob Assignment")

#             # Show BOTH mob types
#             col1, col2 = st.columns(2)

#             with col1:
#                 st.info(f"**Activity Mob:** {activity_mob}")
#                 st.caption(mob_description)
                
#             with col2:
#                 # Original milk-based mob
#                 if detected_type == "Chocolate":
#                     milk_mob = "Chocolate Champions 🍫"
#                 elif detected_type == "Strawberry":
#                     milk_mob = "Berry Squad 🍓"
#                 else:
#                     milk_mob = "Classic Crew 🥛"
                
#                 st.info(f"**Milk Type:** {milk_mob}")
#                 st.caption(f"The {detected_type.lower()} milk lovers")
            
#             # Save to session state
#             st.session_state.processed_videos.append({
#                 "video_id": video_id,
#                 "filename": filename,
#                 "confidence": confidence,
#                 "milk_type": detected_type,
#                 "activity_mob": activity_mob,  # NEW!
#                 "activity_data": {              # NEW!
#                     "activity": activity,
#                     "location": location,
#                     "mood": mood
#                 },
#                 "detection_methods": detection_methods,
#                 "metadata": metadata,
#                 "mob": mob_name if metadata else "Unassigned",
#                 "timestamp": time.time()
#             })
            
#         else:
#             # Milk not detected
#             logger.warning(f"FAILED: No milk detected in {filename}")
            
#             st.error("❌ No Milk Content Detected")
#             st.warning("Although this video has campaign hashtags, we couldn't detect actual milk content.")
            
#             with st.expander("💭 Possible reasons"):
#                 st.write("- Milk might not be clearly visible")
#                 st.write("- Video quality might be too low")
#                 st.write("- Milk might appear too briefly")
#                 st.write("- Try showing milk more prominently")
        
#         # ===== STEP 12: DEBUG INFORMATION =====
#         with st.expander("🔍 Technical Details"):
#             st.write(f"**Task ID:** {task.id}")
#             st.write(f"**Video ID:** {video_id}")
#             st.write(f"**Detection Methods Used:** {', '.join(detection_methods)}")
#             st.write(f"**Processing Time:** ~{(attempt+1)*5} seconds")
            
#     except Exception as e:
#         logger.error(f"Error processing video: {str(e)}", exc_info=True)
#         st.error(f"❌ Error: {str(e)}")
        
#         # Check for specific errors
#         if "API key" in str(e):
#             st.error("Please check your Twelve Labs API key")
#         elif "rate limit" in str(e):
#             st.error("API rate limit reached. Please try again later.")

def show_dashboard_page():
    """Display the dashboard page with quarantine zone"""
    logger.info("Displaying dashboard page")
    st.title("📊 Campaign Dashboard")
    
    # Add tabs for different views
    tab1, tab2, tab3 = st.tabs(["✅ Approved Videos", "🚫 Quarantine Zone", "📋 Processing Logs"])
    
    with tab1:
        # KEEP ALL YOUR EXISTING DASHBOARD CODE HERE
        # This is everything that was in your original show_dashboard_page()
        
        if not st.session_state.processed_videos:
            st.info("No videos processed yet. Upload some videos to see analytics!")
            # return
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Videos", len(st.session_state.processed_videos))
        
        with col2:
            avg_confidence = sum(v['confidence'] for v in st.session_state.processed_videos) / len(st.session_state.processed_videos)
            st.metric("Avg Confidence", f"{avg_confidence:.1f}%")
        
        with col3:
            # Count milk types
            milk_types = {}
            for v in st.session_state.processed_videos:
                milk_type = v.get('milk_type', 'Regular')
                milk_types[milk_type] = milk_types.get(milk_type, 0) + 1
            st.metric("Milk Types", len(milk_types))
        
        with col4:
            # Success rate
            success_rate = len(st.session_state.processed_videos) / len(st.session_state.processed_videos) * 100
            st.metric("Success Rate", f"{success_rate:.0f}%")
        
        # Milk type breakdown
        st.markdown("### 🥛 Milk Type Distribution")
        if milk_types:
            # Create columns for milk type cards
            cols = st.columns(len(milk_types))
            for idx, (milk_type, count) in enumerate(milk_types.items()):
                with cols[idx]:
                    if milk_type == "Chocolate":
                        st.metric("🍫 Chocolate", count)
                    elif milk_type == "Strawberry":
                        st.metric("🍓 Strawberry", count)
                    else:
                        st.metric("🥛 Regular/2%", count)
        
        # Detection methods analysis
        st.markdown("### 🔍 Detection Methods Used")
        all_methods = []
        for video in st.session_state.processed_videos:
            if 'detection_methods' in video:
                all_methods.extend(video['detection_methods'])
        
        if all_methods:
            method_counts = {}
            for method in all_methods:
                key = method.split(":")[0]  # Get method type
                method_counts[key] = method_counts.get(key, 0) + 1
            
            for method, count in method_counts.items():
                st.write(f"- **{method}**: Used {count} times")
        
        # Video list
        st.markdown("### 📹 Processed Videos")
        for video in reversed(st.session_state.processed_videos):
            with st.expander(f"{video['filename']} - {video['confidence']:.1f}% confidence"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Video ID**: `{video['video_id']}`")
                    st.markdown(f"**Milk Type**: {video.get('milk_type', 'Regular')}")
                    st.markdown(f"**Confidence**: {video['confidence']:.1f}%")
                with col2:
                    st.markdown(f"**Processed**: {time.strftime('%I:%M %p', time.localtime(video['timestamp']))}")
                    if 'detection_methods' in video:
                        st.markdown(f"**Methods**: {len(video['detection_methods'])}")
        
        # Export option
        if st.button("📥 Export Results as CSV"):
            logger.info("Exporting results to CSV")
            df = pd.DataFrame(st.session_state.processed_videos)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"got_milk_results_{int(time.time())}.csv",
                mime="text/csv"
            )
    
    with tab2:
        # QUARANTINE ZONE
        st.markdown("### 🚫 Quarantine Zone")
        
        # Check if quarantine exists
        if 'quarantined_videos' not in st.session_state:
            st.info("No quarantined videos yet")
            return
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Missing Metadata", len(st.session_state.quarantined_videos.get('missing_metadata', [])))
        with col2:
            st.metric("No Campaign Tags", len(st.session_state.quarantined_videos.get('no_campaign_tags', [])))
        with col3:
            st.metric("Failed AI Check", len(st.session_state.quarantined_videos.get('ai_detection_failed', [])))
        
        st.markdown("---")
        
        # Missing Metadata Section
        missing_metadata = st.session_state.quarantined_videos.get('missing_metadata', [])
        if missing_metadata:
            with st.expander(f"📁 Missing Metadata ({len(missing_metadata)})"):
                for video in missing_metadata:
                    st.error(f"**{video['filename']}**")
                    st.caption(f"Quarantined: {video['timestamp']}")
                    st.info("❗ Action: Post video with social media metadata")
                    st.markdown("---")
        
        # No Campaign Tags Section
        no_tags = st.session_state.quarantined_videos.get('no_campaign_tags', [])
        if no_tags:
            with st.expander(f"#️⃣ No Campaign Tags ({len(no_tags)})"):
                for video in no_tags:
                    st.error(f"**{video['filename']}**")
                    st.caption(f"Found tags: {', '.join(video['details']['found_tags'])}")
                    st.info("❗ Action: Re-post with #gotmilk or #milkmob")
                    st.markdown("---")
        
        # AI Detection Failed Section
        ai_failed = st.session_state.quarantined_videos.get('ai_detection_failed', [])
        if ai_failed:
            with st.expander(f"🤖 Failed AI Detection ({len(ai_failed)})"):
                for video in ai_failed:
                    st.error(f"**{video['filename']}**")
                    st.warning(f"**Reason**: {video['details']['ai_analysis']}")
                    st.caption(f"Processing time: {video['details']['processing_time']:.1f}s")
                    
                    # Show metadata if available
                    if 'metadata' in video['details'] and video['details']['metadata']:
                        metadata = video['details']['metadata']
                        st.caption(f"Posted by: @{metadata.get('username', 'unknown')}")
                        st.caption(f"Caption: {metadata.get('caption', '')[:100]}...")
                    
                    st.info("❗ Action: Submit video containing actual milk")
                    st.markdown("---")
    
    with tab3:
        # PROCESSING LOGS
        st.markdown("### 📋 Processing Logs (Last 100)")
        
        # Check if logs exist
        if 'processing_logs' not in st.session_state or not st.session_state.processing_logs:
            st.info("No processing logs yet")
            return
        
        # Summary stats
        total_logs = len(st.session_state.processing_logs)
        approved = sum(1 for log in st.session_state.processing_logs if log['status'] == 'approved')
        quarantined = total_logs - approved
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Processed", total_logs)
        with col2:
            st.metric("Approved", approved)
        with col3:
            st.metric("Quarantined", quarantined)
        
        # Export button
        if st.button("📥 Export Logs as JSON"):
            logs_json = json.dumps(st.session_state.processing_logs, indent=2)
            st.download_button(
                label="Download JSON",
                data=logs_json,
                file_name=f"processing_logs_{int(time.time())}.json",
                mime="application/json"
            )
        
        st.markdown("---")
        
        # Show recent logs (last 10)
        st.markdown("#### Recent Activity")
        for log in reversed(st.session_state.processing_logs[-10:]):
            status_emoji = "✅" if log['status'] == "approved" else "🚫"
            
            # Create a nice display for each log
            with st.expander(f"{status_emoji} {log['filename']} - {log['timestamp'].split('T')[1].split('.')[0]}"):
                if log['status'] == 'approved':
                    st.success("Status: Approved")
                    st.write(f"**Milk Type**: {log.get('milk_type', 'Unknown')}")
                    st.write(f"**Confidence**: {log.get('confidence', 0):.1f}%")
                    st.write(f"**Activity Mob**: {log.get('activity_mob', 'Unknown')}")
                else:
                    st.error("Status: Quarantined")
                    st.write(f"**Reason**: {log['reason'].replace('_', ' ').title()}")
                    if 'details' in log:
                        st.json(log['details'])
                
                st.caption(f"Processing Time: {log.get('processing_time', 'N/A')}")

def show_instagram_simulator():
    """Simulate real-time Instagram uploads arriving at the platform"""
    st.title("📱 Instagram Live Feed Simulator")
    st.markdown("### Watch as creators post to #GotMilk campaign in real-time!")
    
    # Get all videos with metadata that haven't been processed yet
    processed_ids = [v['filename'] for v in st.session_state.processed_videos]
    
    # Find unprocessed campaign videos
    available_videos = []
    for pattern in ["test_videos/2%/*.mp4", "test_videos/choco/*.mp4", "test_videos/straw/*.mp4", "test_videos/EdgeTests/real vids META/*.mp4"]:
        for video_path in glob.glob(pattern):
            if os.path.basename(video_path) not in processed_ids:
                # Check if has metadata
                metadata_path = video_path.replace('.mp4', '_metadata.json')
                if os.path.exists(metadata_path):
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                    if metadata.get('has_campaign_hashtags', False):
                        available_videos.append({
                            'path': video_path,
                            'metadata': metadata,
                            'filename': os.path.basename(video_path)
                        })
    
    if not available_videos:
        st.success("🎉 All campaign videos have been processed! Check the Mob Explorer.")
        if st.button("🔄 Reset Demo"):
            st.session_state.processed_videos = []
            st.rerun()
        return
    
    # Simulate incoming posts
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Create Instagram-style post card
        next_video = available_videos[0]
        metadata = next_video['metadata']
        
        # Post header
        st.markdown(f"**{metadata['username']}** • {metadata['location']}")
        st.caption(f"{metadata['full_name']} • {metadata['creative_style']}")
        
        # Video preview
        st.video(next_video['path'])
        
        # Engagement metrics
        col_likes, col_views, col_engagement = st.columns(3)
        with col_likes:
            st.metric("❤️ Likes", f"{metadata['likes']:,}")
        with col_views:
            st.metric("👁️ Views", f"{metadata['views']:,}")
        with col_engagement:
            st.metric("📈 Engagement", f"{metadata['engagement_rate']}%")
        
        # Caption and hashtags
        st.markdown("**Caption:**")
        st.write(metadata['caption'])
        
        # Highlight campaign hashtags
        hashtags_html = []
        for tag in metadata['hashtags']:
            if tag in ['#gotmilk', '#milkmob']:
                hashtags_html.append(f"<span style='color: #00a651; font-weight: bold;'>{tag}</span>")
            else:
                hashtags_html.append(f"<span style='color: #1890ff;'>{tag}</span>")
        st.markdown(" ".join(hashtags_html), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Alert style notification
        st.info("🔔 **New #GotMilk post detected!**")
        
        # Process button
        if st.button("✅ Validate & Add to Campaign", type="primary", use_container_width=True):
            with st.spinner("🤖 AI validating milk content..."):
                # Process EXACTLY like Upload does
                client = init_twelve_labs()
                with open(next_video['path'], 'rb') as f:
                    process_video(client, f, filename=next_video['filename'])
            
            st.balloons()
            st.success("✅ Added to campaign!")
            time.sleep(2)
            st.rerun()
    
    # Show queue
    with st.sidebar:
        st.markdown("### 📥 Incoming Queue")
        st.metric("Posts Waiting", len(available_videos))
        
        if len(available_videos) > 1:
            st.markdown("**Next Up:**")
            for i, video in enumerate(available_videos[1:4]):  # Show next 3
                st.caption(f"{i+2}. {video['metadata']['username']}")
        
        st.markdown("---")
        st.markdown("### ⚡ Live Stats")
        st.metric("Processed Today", len(st.session_state.processed_videos))
        st.metric("Success Rate", "100%")

def show_mob_explorer():
    """Show milk mob communities with rich creator information"""
    st.title("🌟 Milk Mob Explorer")
    
    if not st.session_state.processed_videos:
        st.info("No mobs created yet. Head to the Instagram Simulator to process videos!")
        return
    
    # Tab selection for different views
    tab1, tab2, tab3 = st.tabs(["🏆 Activity Mobs", "🥛 Milk Type Tribes", "📊 Creator Leaderboard"])
    
    with tab1:
        show_activity_mobs()
        
    with tab2:
        show_milk_type_mobs()
        
    with tab3:
        show_creator_leaderboard()

def show_activity_mobs():
    """Show activity-based mobs with creator cards"""
    st.markdown("### 🎯 Find Your Tribe by Activity")
    
    # Group by activity mobs
    activity_mobs = {}
    for video in st.session_state.processed_videos:
        mob = video.get('activity_mob', 'Unknown')
        if mob not in activity_mobs:
            activity_mobs[mob] = []
        activity_mobs[mob].append(video)
    
    # Sort by size
    sorted_mobs = sorted(activity_mobs.items(), key=lambda x: len(x[1]), reverse=True)
    
    for mob_name, members in sorted_mobs:
        with st.expander(f"{mob_name} ({len(members)} members)", expanded=True):
            # Mob stats
            col1, col2, col3 = st.columns(3)
            
            # Calculate total engagement - FIX THE ERROR HERE
            total_likes = 0
            total_views = 0
            engagement_count = 0
            total_engagement = 0
            
            for m in members:
                if m and m.get('metadata'):  # Check if metadata exists
                    metadata = m['metadata']
                    total_likes += metadata.get('likes', 0)
                    total_views += metadata.get('views', 0)
                    if 'engagement_rate' in metadata:
                        total_engagement += metadata['engagement_rate']
                        engagement_count += 1
            
            avg_engagement = total_engagement / engagement_count if engagement_count > 0 else 0
            
            with col1:
                st.metric("Total Likes", f"{total_likes:,}")
            with col2:
                st.metric("Total Views", f"{total_views:,}")
            with col3:
                st.metric("Avg Engagement", f"{avg_engagement:.1f}%")
            
            # Rest of the function stays the same...

def show_milk_type_mobs():
    """Show traditional milk type groupings"""
    st.markdown("### 🥛 Classic Milk Categories")
    
    # Group by milk type
    milk_groups = {}
    for video in st.session_state.processed_videos:
        milk_type = video.get('milk_type', 'Unknown')
        if milk_type not in milk_groups:
            milk_groups[milk_type] = []
        milk_groups[milk_type].append(video)
    
    cols = st.columns(3)
    icons = {"Chocolate": "🍫", "Strawberry": "🍓", "2% Regular": "🥛", "Regular": "🥛"}
    
    for idx, (milk_type, videos) in enumerate(milk_groups.items()):
        with cols[idx % 3]:
            icon = icons.get(milk_type, "🥛")
            st.markdown(f"### {icon} {milk_type}")
            st.metric("Members", len(videos))
            
            # List top creators
            st.markdown("**Top Creators:**")
            for video in videos[:3]:
                metadata = video.get('metadata', {})
                if metadata:
                    st.caption(f"• {metadata.get('username', 'Unknown')}")

def show_creator_leaderboard():
    """Show top creators by engagement"""
    st.markdown("### 🏆 Top Campaign Creators")
    
    # Sort by engagement
    creators_with_metadata = [v for v in st.session_state.processed_videos if v.get('metadata')]
    sorted_creators = sorted(creators_with_metadata, 
                           key=lambda x: x.get('metadata', {}).get('engagement_rate', 0), 
                           reverse=True)
    
    for rank, video in enumerate(sorted_creators[:10], 1):
        metadata = video.get('metadata', {})
        col1, col2, col3, col4 = st.columns([0.5, 2, 1, 1])
        
        with col1:
            st.markdown(f"**#{rank}**")
        
        with col2:
            st.markdown(f"**{metadata.get('username', 'Unknown')}**")
            st.caption(f"{metadata.get('creative_style', '')} • {metadata.get('location', '')}")
        
        with col3:
            st.metric("Engagement", f"{metadata.get('engagement_rate', 0)}%")
        
        with col4:
            st.metric("Mob", video.get('activity_mob', 'Unknown').split(' ')[0])        

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Got Milk Campaign Manager Started")
    logger.info(f"Current time: {datetime.now()}")
    logger.info(f"Index ID: {os.getenv('CAMPAIGN_INDEX_ID', 'Not set')}")
    logger.info("=" * 60)
    main()
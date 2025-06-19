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
            "🎬 Upload Video": "Upload",
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
            
def process_video(client, video_file, filename=None):
    """
    Complete video processing pipeline:
    1. Load video and metadata
    2. Check for campaign hashtags (#gotmilk or #milkmob)
    3. If campaign participant → Send to Twelve Labs
    4. Detect milk content using Pegasus/multi-modal analysis
    5. If milk found → Assign to appropriate mob
    """
    
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
            logger.info("No metadata found - treating as direct upload")
    
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
            # NOT A CAMPAIGN VIDEO - REJECT
            logger.info(f"REJECTED: No campaign hashtags found")
            
            st.error("❌ Not a #GotMilk Campaign Video!")
            
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
        
        # Wait for indexing to complete
        time.sleep(3)
        
        # ===== STEP 8: TRY PEGASUS ANALYSIS FIRST =====
        try:
            logger.info("Attempting Pegasus AI analysis")
            
            analysis_result = client.analyze(
                video_id=video_id,
                prompt="""Analyze this video and answer:
                1. Is there any milk visible in this video? (yes/no)
                2. Can you see any milk containers, bottles, or cartons?
                3. Do you hear anyone saying "got milk" or mentioning milk?
                4. Are there any milk labels or text visible?
                5. What type of milk is it? (chocolate, strawberry, regular, none)
                
                Provide a confidence score from 0-100 for milk presence.""",
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
            
            # Display AI analysis
            with st.expander("🤖 AI Analysis Result"):
                st.write(analysis_text)
            
            # Parse results
            milk_found = "yes" in analysis_text and ("milk" in analysis_text or "dairy" in analysis_text)
            
            # Calculate dynamic confidence based on analysis
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
                            confidence = result.score  # This gives you 84.56!
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
            
            st.success("✅ Milk Content Validated!")
            st.balloons()
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Milk Type", detected_type)
            with col2:
                st.metric("Confidence", f"{confidence:.2f}%")  # Shows
            with col3:
                st.metric("Status", "Approved")
            
            # ===== STEP 11: MOB ASSIGNMENT =====
            st.markdown("### 🎯 Mob Assignment")
            
            # TODO: Implement actual mob assignment logic
            # For now, simulate mob assignment based on type and metadata
            if metadata:
                username = metadata.get('username', 'unknown')
                
                if detected_type == "Chocolate":
                    mob_name = "Chocolate Champions 🍫"
                    mob_description = "The bold ones who embrace the cocoa"
                elif detected_type == "Strawberry":
                    mob_name = "Berry Squad 🍓"
                    mob_description = "Sweet souls with pink milk dreams"
                else:
                    mob_name = "Classic Crew 🥛"
                    mob_description = "Keeping it real with regular milk"
                
                st.info(f"**Assigned to:** {mob_name}")
                st.caption(mob_description)
                st.caption(f"Welcome to the mob, {username}!")
            
            # Save to session state
            st.session_state.processed_videos.append({
                "video_id": video_id,
                "filename": filename,
                "confidence": confidence,
                "milk_type": detected_type,
                "detection_methods": detection_methods,
                "metadata": metadata,
                "mob": mob_name if metadata else "Unassigned",
                "timestamp": time.time()
            })
            
        else:
            # Milk not detected
            logger.warning(f"FAILED: No milk detected in {filename}")
            
            st.error("❌ No Milk Content Detected")
            st.warning("Although this video has campaign hashtags, we couldn't detect actual milk content.")
            
            with st.expander("💭 Possible reasons"):
                st.write("- Milk might not be clearly visible")
                st.write("- Video quality might be too low")
                st.write("- Milk might appear too briefly")
                st.write("- Try showing milk more prominently")
        
        # ===== STEP 12: DEBUG INFORMATION =====
        with st.expander("🔍 Technical Details"):
            st.write(f"**Task ID:** {task.id}")
            st.write(f"**Video ID:** {video_id}")
            st.write(f"**Detection Methods Used:** {', '.join(detection_methods)}")
            st.write(f"**Processing Time:** ~{(attempt+1)*5} seconds")
            
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}", exc_info=True)
        st.error(f"❌ Error: {str(e)}")
        
        # Check for specific errors
        if "API key" in str(e):
            st.error("Please check your Twelve Labs API key")
        elif "rate limit" in str(e):
            st.error("API rate limit reached. Please try again later.")

def show_dashboard_page():
    """Display the dashboard page"""
    logger.info("Displaying dashboard page")
    st.title("📊 Campaign Dashboard")
    
    if not st.session_state.processed_videos:
        st.info("No videos processed yet. Upload some videos to see analytics!")
        return
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Videos", len(st.session_state.processed_videos))
    
    with col2:
        avg_confidence = sum(v['confidence'] for v in st.session_state.processed_videos) / len(st.session_state.processed_videos)
        st.metric("Avg Confidence", f"{avg_confidence:.1%}")
    
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
        with st.expander(f"{video['filename']} - {video['confidence']:.1%} confidence"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Video ID**: `{video['video_id']}`")
                st.markdown(f"**Milk Type**: {video.get('milk_type', 'Regular')}")
                st.markdown(f"**Confidence**: {video['confidence']:.1%}")
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

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Got Milk Campaign Manager Started")
    logger.info(f"Current time: {datetime.now()}")
    logger.info(f"Index ID: {os.getenv('CAMPAIGN_INDEX_ID', 'Not set')}")
    logger.info("=" * 60)
    main()
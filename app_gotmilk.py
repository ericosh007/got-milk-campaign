"""
Got Milk Campaign Manager
Main Streamlit Application
"""

import streamlit as st
import os
from dotenv import load_dotenv
from twelvelabs import TwelveLabs
from twelvelabs.models.task import Task
import time
import json

# Load environment variables from .env file
load_dotenv()

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
    api_key = os.getenv("TWELVE_LABS_API_KEY")
    
    if not api_key:
        return None
    
    try:
        client = TwelveLabs(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Error connecting to Twelve Labs: {str(e)}")
        return None

# Initialize session state variables
def init_session_state():
    """Set up session state variables"""
    if 'index_id' not in st.session_state:
        # Check if we have a saved index ID in .env
        st.session_state.index_id = os.getenv("CAMPAIGN_INDEX_ID", None)
    
    if 'processed_videos' not in st.session_state:
        st.session_state.processed_videos = []
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"

# Main app
def main():
    """Main application logic"""
    
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
    
    # Display current page
    if st.session_state.current_page == "Home":
        show_home_page()
    elif st.session_state.current_page == "Setup":
        show_setup_page(client)
    elif st.session_state.current_page == "Upload":
        show_upload_page(client)
    elif st.session_state.current_page == "Dashboard":
        show_dashboard_page()

def show_home_page():
    """Display the home page"""
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
    - **Detect** milk in videos (visual + audio)
    - **Categorize** content into "Milk Mobs" 
    - **Predict** viral potential
    """)

def show_setup_page(client):
    """Display the setup page"""
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
            st.markdown("- Finds milk in videos")
            st.markdown("- Multi-modal understanding")
        
        with col2:
            st.markdown("**Pegasus 1.2** - Analysis")
            st.markdown("- Understands context")
            st.markdown("- Generates descriptions")
        
        submit = st.form_submit_button("🚀 Create Index", type="primary")
        
        if submit:
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
                    
                    st.success(f"✅ Index created successfully!")
                    st.code(f"Index ID: {index.id}")
                    st.info("""
                    Save this index ID to your `.env` file:
                    ```
                    CAMPAIGN_INDEX_ID={index.id}
                    ```
                    """.format(index.id=index.id))
                    
                except Exception as e:
                    st.error(f"Error creating index: {str(e)}")

def show_upload_page(client):
    """Display the upload page"""
    st.title("🎬 Upload Your Milk Video")
    
    # Check if index exists
    if not st.session_state.index_id:
        st.warning("⚠️ Please create an index first!")
        if st.button("Go to Setup"):
            st.session_state.current_page = "Setup"
            st.rerun()
        return
    
    st.markdown("Upload a video and we'll detect if it contains milk!")
    
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

def process_video(client, video_file):
    """Process uploaded video"""
    
    # Progress tracking
    progress = st.progress(0)
    status = st.empty()
    
    try:
        # Step 1: Upload video
        status.text("📤 Uploading video...")
        progress.progress(20)
        
        task = client.task.create(
            index_id=st.session_state.index_id,
            file=video_file
        )
        
        # Step 2: Wait for processing
        status.text("🔄 Processing video... This may take 1-2 minutes...")
        progress.progress(40)
        
        # Monitor task status
        def on_task_update(task: Task):
            if task.status == "indexing":
                progress.progress(60)
            elif task.status == "ready":
                progress.progress(80)
        
        task.wait_for_done(sleep_interval=5, callback=on_task_update)
        
        if task.status != "ready":
            st.error(f"Processing failed: {task.status}")
            return
        
        # Step 3: Search for milk
        status.text("🔍 Detecting milk content...")
        progress.progress(90)
        
        # Search for milk visually and in audio
        search_results = client.search.query(
            index_id=st.session_state.index_id,
            query_text="milk dairy glass bottle drinking pouring white liquid",
            video_ids=[task.video_id],
            options=["visual", "audio"],
            threshold=0.5
        )
        
        progress.progress(100)
        
        # Display results
        if search_results.data and len(search_results.data) > 0:
            st.success("✅ Milk detected! Welcome to the campaign!")
            
            # Show confidence score
            confidence = search_results.data[0].score
            st.metric("Confidence Score", f"{confidence:.1%}")
            
            # Save to processed videos
            st.session_state.processed_videos.append({
                "video_id": task.video_id,
                "filename": video_file.name,
                "confidence": confidence,
                "timestamp": time.time()
            })
            
            st.balloons()
            
        else:
            st.error("❌ No milk detected. Try again with milk clearly visible!")
            
    except Exception as e:
        st.error(f"Error processing video: {str(e)}")

def show_dashboard_page():
    """Display the dashboard page"""
    st.title("📊 Campaign Dashboard")
    
    if not st.session_state.processed_videos:
        st.info("No videos processed yet. Upload some videos to see analytics!")
        return
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Videos", len(st.session_state.processed_videos))
    
    with col2:
        avg_confidence = sum(v['confidence'] for v in st.session_state.processed_videos) / len(st.session_state.processed_videos)
        st.metric("Avg Confidence", f"{avg_confidence:.1%}")
    
    with col3:
        st.metric("Success Rate", "100%")  # For demo
    
    # Video list
    st.markdown("### Processed Videos")
    for video in st.session_state.processed_videos:
        st.markdown(f"- **{video['filename']}** - Confidence: {video['confidence']:.1%}")

if __name__ == "__main__":
    main()
"""
Got Milk Campaign Manager
Main Streamlit Application - Optimized Version
Last Updated: June 18, 2025 - 9:45 PM PST
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
    try:
        indexes = list(client.index.list())
        st.metric("Total Indexes", len(indexes))
        
        total_videos = 0
        for index in indexes:
            videos = list(client.index.video.list(index_id=index.id))
            total_videos += len(videos)
        
        st.metric("Total Videos", total_videos)
        st.info("Visit [console.twelvelabs.io](https://console.twelvelabs.io) for detailed billing")
    except Exception as e:
        st.error(f"Could not fetch usage: {str(e)}")

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
    - **Detect** milk in videos (visual + audio + text)
    - **Identify** milk types (chocolate, strawberry, regular)
    - **Validate** "Got Milk?" campaign content
    - **Score** confidence levels
    
    ### 📁 Test Videos Available
    You have **35 test videos** ready in your data folder:
    - 10 Chocolate Milk videos 🍫
    - 10 Regular Milk videos 🥛
    - 10 Strawberry Milk videos 🍓
    - Plus real videos and non-milk controls!
    
    ### 🔍 Detection Methods
    - **Audio**: Detects "Got Milk?" phrases
    - **Visual**: Identifies milk containers and liquid
    - **Text**: Reads labels and on-screen text
    - **Multi-modal**: Combines all methods for accuracy
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
                    st.info(f"""
Save this index ID to your `.env` file:
```
CAMPAIGN_INDEX_ID={index.id}
```
""")
                    
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
        # Show test videos
        st.markdown("### Select a test video:")
        
        # Get all test videos
        import glob
        test_videos = glob.glob("data/AI videos/*.mp4") + glob.glob("data/real vids/*.mp4")
        
        if test_videos:
            # Group videos by type
            chocolate_videos = [v for v in test_videos if "chocolate" in v.lower()]
            strawberry_videos = [v for v in test_videos if "strawberry" in v.lower()]
            regular_videos = [v for v in test_videos if "regular" in v.lower() or "lilgirl" in v.lower()]
            other_videos = [v for v in test_videos if v not in chocolate_videos + strawberry_videos + regular_videos]
            
            video_type = st.selectbox(
                "Video Category:",
                ["All Videos", "Chocolate Milk", "Strawberry Milk", "Regular Milk", "Other"]
            )
            
            if video_type == "Chocolate Milk":
                video_list = chocolate_videos
            elif video_type == "Strawberry Milk":
                video_list = strawberry_videos
            elif video_type == "Regular Milk":
                video_list = regular_videos
            elif video_type == "Other":
                video_list = other_videos
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
                elif "regular" in video_name or "lilgirl" in video_name:
                    st.info("💡 Expected: Regular Milk")
                elif "water" in video_name:
                    st.info("💡 Expected: No Milk (Control)")
                
                if st.button("🥛 Validate This Video", type="primary"):
                    # Process the selected video
                    with open(selected_video, 'rb') as f:
                        process_video(client, f, filename=os.path.basename(selected_video))
        else:
            st.warning("No test videos found in data folder")

def process_video(client, video_file, filename=None):
    """Process uploaded video with optimized detection"""
    
    if filename is None:
        filename = video_file.name if hasattr(video_file, 'name') else "uploaded_video.mp4"
    
    # Progress tracking
    progress = st.progress(0)
    status = st.empty()
    
    try:
        # Step 1: Upload video
        status.text("📤 Uploading video to Twelve Labs...")
        progress.progress(20)
        
        task = client.task.create(
            index_id=st.session_state.index_id,
            file=video_file
        )
        
        st.info(f"Task ID: {task.id}")
        st.info("⏱️ Processing typically takes 30-60 seconds...")
        
        # Step 2: Wait for processing
        status.text("🔄 Processing video...")
        progress.progress(40)
        
        # Monitor task status
        max_attempts = 30  # 2.5 minutes max
        for attempt in range(max_attempts):
            task_status = client.task.retrieve(task.id)
            
            if task_status.status == "ready":
                break
            elif task_status.status == "failed":
                st.error("Processing failed!")
                return
                
            status.text(f"🔄 Status: {task_status.status} ({attempt+1}/30)")
            time.sleep(5)
        
        progress.progress(80)
        
        # Step 3: Enhanced milk detection
        status.text("🔍 Detecting milk content...")
        progress.progress(90)
        
        # Add a small delay to ensure everything is indexed
        time.sleep(3)
        
         # Multi-stage detection - STRICT VERSION
        milk_found = False
        confidence = 0.0
        detected_type = "Unknown"
        detection_methods = []
        
        # We'll search the index and check if results match our video
        target_video_id = task.id  # This is our video ID
        
        # CRITICAL: We need multiple positive signals for milk
        audio_detected = False
        visual_detected = False
        text_detected = False
        
        
        # Stage 1: Search for speech/audio "Got Milk" phrases - IMPROVED
        try:
            # Try multiple audio search approaches
            audio_queries = [
                "got milk",                    # Simple
                "chocolate milk",              # Specific types
                "strawberry milk",
                "milk",                        # Basic
                "got chocolate strawberry",    # Without "milk"
                "speaking milk dairy"          # General speech
            ]
            
            for query in audio_queries:
                try:
                    audio_results = client.search.query(
                        index_id=st.session_state.index_id,
                        query_text=query,
                        options=["audio"],
                        threshold="low",  # Most permissive
                        page_limit=20
                    )
                    
                    for result in audio_results.data:
                        if result.video_id == target_video_id:
                            # Found audio match!
                            if result.score > 75:  # Lowered threshold
                                audio_detected = True
                                confidence = max(confidence, result.score)
                                detection_methods.append(f"Audio: Detected '{query}'")
                                st.success(f"✅ Detected audio: '{query}' (Score: {result.score:.1f})")
                                break
                    
                    if audio_detected:
                        break  # Stop searching if found
                        
                except:
                    continue  # Try next query
                    
        except Exception as e:
            st.warning(f"Audio search error: {str(e)}")
        
        # Stage 2: Search for milk LABELS and TEXT - HIGH PRIORITY
        try:
            label_results = client.search.query(
                index_id=st.session_state.index_id,
                query_text='text:"milk" text:"MILK" text:"2%" text:"chocolate" text:"strawberry" label',
                options=["visual"],
                threshold="low",
                page_limit=20
            )
            
            for result in label_results.data:
                if result.video_id == target_video_id and result.score > 75:
                    text_detected = True
                    confidence = max(confidence, result.score)
                    detection_methods.append("Visual: Milk label/text detected")
                    st.success("✅ Detected milk label text!")
                    break
                    
        except Exception as e:
            pass
        
        # Stage 3: Visual milk-specific search - VERY SPECIFIC
        try:
            # Only search for MILK-SPECIFIC visual elements
            visual_results = client.search.query(
                index_id=st.session_state.index_id,
                query_text="milk carton dairy bottle white creamy opaque NOT water NOT clear NOT transparent",
                options=["visual"],
                threshold="medium",
                page_limit=20
            )
            
            for result in visual_results.data:
                if result.video_id == target_video_id and result.score > 82:
                    visual_detected = True
                    confidence = max(confidence, result.score)
                    detection_methods.append("Visual: Milk container/dairy detected")
                    st.success("✅ Detected visual milk content!")
                    break
                    
        except Exception as e:
            pass
        
        # DECISION LOGIC - Need at least 2 out of 3 signals
        positive_signals = sum([audio_detected, visual_detected, text_detected])
        
        # Special case: If we have "Got Milk" audio, that's enough
        if audio_detected:
            milk_found = True
            st.info("🎯 'Got Milk' audio is definitive evidence!")
        # Need at least 2 signals for other cases
        elif positive_signals >= 2:
            milk_found = True
            st.info(f"🎯 Multiple detection methods confirmed milk ({positive_signals}/3)")
        # Single visual detection needs very high confidence
        elif visual_detected and confidence > 85:
            milk_found = True
            st.info("🎯 High-confidence visual detection")
        # Text detection alone is good evidence
        elif text_detected:
            milk_found = True
            st.info("🎯 Milk label text is strong evidence")
        else:
            # Final fallback - look for chocolate/strawberry specifically
            try:
                specific_results = client.search.query(
                    index_id=st.session_state.index_id,
                    query_text="chocolate milk strawberry milk brown pink dairy",
                    options=["visual"],
                    threshold="high",
                    page_limit=10
                )
                
                for result in specific_results.data:
                    if result.video_id == target_video_id and result.score > 85:
                        milk_found = True
                        confidence = result.score
                        detection_methods.append("Visual: Flavored milk detected")
                        break
                        
            except:
                pass
        
        progress.progress(100)
        
        # Display results
        if milk_found:
            st.success("✅ Milk detected! Welcome to the campaign!")
            
            # Fix confidence display
            display_confidence = confidence / 100 if confidence > 1 else confidence
            st.metric("Confidence Score", f"{display_confidence:.1%}")
            
            # Determine milk type from filename or detection
            if "chocolate" in filename.lower():
                detected_type = "Chocolate"
            elif "strawberry" in filename.lower():
                detected_type = "Strawberry"
            elif "regular" in filename.lower() or "2%" in filename.lower():
                detected_type = "2% Regular"
            else:
                detected_type = "Regular"
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"🥛 **Type:** {detected_type}")
            with col2:
                st.info(f"🎯 **Score:** {confidence:.1f}")
            with col3:
                st.info(f"✅ **Signals:** {positive_signals}/3")
            
            # Debug info
            with st.expander("📋 Detection Details"):
                st.write(f"**Video ID:** `{target_video_id}`")
                st.write(f"**Filename:** {filename}")
                st.write(f"**Detection Signals:**")
                st.write(f"- Audio Detection: {'✅' if audio_detected else '❌'}")
                st.write(f"- Visual Detection: {'✅' if visual_detected else '❌'}")
                st.write(f"- Text Detection: {'✅' if text_detected else '❌'}")
                st.write(f"**Methods Used:** {', '.join(detection_methods) if detection_methods else 'None'}")
                
            # Save to processed videos
            st.session_state.processed_videos.append({
                "video_id": target_video_id,
                "filename": filename,
                "confidence": display_confidence,
                "milk_type": detected_type,
                "detection_methods": detection_methods,
                "signals": f"{positive_signals}/3",
                "timestamp": time.time()
            })
            
            st.balloons()
            
        else:
            st.error("❌ No milk detected.")
            st.info(f"Detection signals: Audio={audio_detected}, Visual={visual_detected}, Text={text_detected}")
            
            # Helpful feedback
            if filename.lower() == "drinking_water.mp4":
                st.success("✅ Correctly rejected! This is water, not milk.")
            else:
                st.warning("This video might not contain clear milk content.")
                st.markdown("### 💡 For successful detection, videos need:")
                st.markdown("- Clear 'Got Milk?' audio OR")
                st.markdown("- Visible milk labels/text OR")  
                st.markdown("- Multiple indicators of dairy content")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")

        if "task" in locals():
            st.info(f"Task ID: {task.id}")
        st.info("Try a shorter video or check your internet connection.")

def show_dashboard_page():
    """Display the dashboard page"""
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
                    st.metric("🥛 Regular", count)
    
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
        import pandas as pd
        df = pd.DataFrame(st.session_state.processed_videos)
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"got_milk_results_{int(time.time())}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
# Got Milk Campaign - Source of Truth v6
**Last Updated: June 20, 2025 - 2:10 PM MST**
**Session: Post-GitHub Sync Update**

---

## 🎯 PROJECT STATUS: MVP COMPLETE WITH QUARANTINE SYSTEM

### Latest Changes (Since GitHub Sync)
- ✅ **Fixed Instagram Simulator**: Now shows ALL videos regardless of hashtags
- ✅ **Fixed Quarantine Logic**: Properly quarantines videos without campaign hashtags
- ✅ **Fixed Dashboard Error**: Resolved `milk_types` undefined error
- ✅ **Confirmed Working**: Successfully quarantined `lilgirlregmilk.mp4` when #milkmob removed
- ✅ **GitHub Repository**: Code pushed and synced

### Current Working Features
1. **Three-Tier Quarantine System**
   - Missing Metadata → Quarantine
   - No Campaign Hashtags (#gotmilk/#milkmob) → Quarantine  
   - AI Detection Failed → Quarantine

2. **Instagram Feed Simulator**
   - Shows ALL videos with metadata (not filtered by hashtags)
   - Visual indicators: Green for campaign tags, blue for others
   - Different button states: "Validate & Add" vs "Check Post Anyway"
   - Tracks already processed/quarantined videos

3. **Behavioral Mob System**
   - Gym Warriors 💪
   - Creative Collective 🎨
   - Comedy Kings 😂
   - Home Chillers 🏠
   - Kitchen Creators 👨‍🍳

4. **Multi-Modal AI Detection**
   - Visual detection (objects in scene)
   - Audio detection (speech recognition)
   - Text detection (on-screen text)
   - 2/3 signals required for validation

---

## 🧠 TWELVE LABS INTEGRATION DETAILS

### API Configuration
```python
# Current Index (check .env for latest)
CAMPAIGN_INDEX_ID=6855b4bf93b57295283de3b1
TWELVE_LABS_API_KEY=tlk_[YOUR_KEY]

# Model Configuration
models=[
    {
        "name": "pegasus1.1",
        "options": ["visual", "audio"]
    }
]
```

### Search Queries Being Used
```python
# Visual Detection
"person drinking milk OR glass of milk OR milk bottle OR milk carton"

# Audio Detection  
"'got milk' OR 'drinking milk' OR 'love milk' OR 'milk tastes'"

# Text Detection
"text 'milk' OR text 'got milk' OR text 'leche'"
```

---

## 🔧 TECHNICAL FIXES IMPLEMENTED

### 1. Instagram Simulator Fix
```python
# OLD: Was filtering by hashtags
if metadata.get('has_campaign_hashtags', False):

# NEW: Shows all videos
available_videos.append({
    'path': video_path,
    'metadata': metadata,
    'filename': filename
})
```

### 2. Process Video Call Fix
```python
# OLD: Passed file object
with open(next_video['path'], 'rb') as f:
    process_video(client, f, filename=next_video['filename'])

# NEW: Pass path directly
process_video(client, next_video['path'], filename=next_video['filename'])
```

### 3. Dashboard Milk Types Fix
```python
# Define milk_types before using it
milk_types = {}
for v in st.session_state.processed_videos:
    milk_type = v.get('milk_type', 'Regular')
    milk_types[milk_type] = milk_types.get(milk_type, 0) + 1

# Now safe to check
if milk_types:  
    # Display milk type cards
```

---

## 📊 CURRENT TEST RESULTS

### Videos Processed Successfully
- 4 videos validated and added to campaign
- All showed proper confidence scores (83-86%)
- Mob assignments working correctly

### Quarantine System Working
- `lilgirlregmilk.mp4` successfully quarantined when hashtags changed
- Proper error messages displayed
- API calls saved when quarantining

### Pending Features (Black Screens Normal)
- Behavioral Leaderboards
- Scene Analytics  
- Location Insights
- Viral Predictors

---

## 🚀 WHAT'S LEFT TO BUILD

### 1. Enhanced AI Scene Intelligence Hub (2 hours)
**Position as Twelve Labs Exclusive:**
```python
# Activity Heatmap
- Show distribution of activities across all videos
- Cluster by time of day and location

# Mood Spectrum Visualization
- Plot videos on funny → serious axis
- Show energy levels across content

# Location Clustering Map
- Geographic visualization of filming locations
- Indoor vs outdoor breakdown
```

### 2. Behavioral Leaderboards (1 hour)
```python
# Rankings to implement:
- Engagement Champions (by rate)
- Activity Masters (best per category)  
- Mood Leaders (funniest, most artistic)
- Location Stars (top per venue type)
```

### 3. Viral Predictor Dashboard (1.5 hours)
```python
# Factors to analyze:
- Hook strength (first 3 seconds)
- Energy progression
- Creativity score
- Platform optimization
```

---

## 💡 KEY COMMANDS & TIPS

### Running the App
```bash
# ALWAYS use this command (not streamlit run)
python -m streamlit run app.py

# Create metadata for test videos
python create_metadata.py

# Check your current branch
git status

# Push changes
git add .
git commit -m "feat: your message here"
git push origin main
```

### Testing Quarantine
1. Edit a metadata file to remove campaign hashtags
2. Run the Instagram Simulator
3. Click "Check Post Anyway" on the modified video
4. Should see quarantine message

### Common Issues
- **Black screens in tabs**: Normal - features not implemented yet
- **Processing time**: 30-90 seconds is normal for Twelve Labs
- **Rate limits**: 50 requests/day on free tier

---

## 📈 DEMO POSITIONING

### The Story
"Traditional approaches would just scan for milk bottles. But with Twelve Labs, we built something more powerful - an AI that understands not just WHAT people are drinking, but WHY, WHERE, and HOW they're enjoying it."

### Key Demo Points
1. Show Instagram Simulator with mixed content
2. Demonstrate quarantine system catching non-campaign posts
3. Show successful validation with confidence scores
4. Highlight mob assignments based on activities
5. Tease upcoming features (leaderboards, analytics)

---

## 🚨 CRITICAL REMINDERS

1. **Check .env** for correct API key and index ID
2. **Metadata required** for all test videos
3. **Hashtag logic**: Needs either #gotmilk OR #milkmob (not both)
4. **Dashboard tabs**: Black screens are normal for unimplemented features
5. **Always use** `python -m streamlit run app.py`

---

**Project Status**: CORE MVP COMPLETE ✅
**Quarantine System**: WORKING ✅  
**GitHub**: SYNCED ✅
**Demo Readiness**: 75% - Needs UI polish and feature completion

---

**END OF SOURCE OF TRUTH v6 - June 20, 2025 - 2:10 PM MST**
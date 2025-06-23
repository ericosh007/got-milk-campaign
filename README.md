# 🥛 Got Milk? AI Campaign Manager

> Transform user-generated content into viral marketing gold using Twelve Labs' cutting-edge video understanding AI

<p align="center">
  <img src="https://img.shields.io/badge/Twelve_Labs-Powered-blue?style=for-the-badge" alt="Twelve Labs">
  <img src="https://img.shields.io/badge/Python-3.11+-green?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-1.32+-red?style=for-the-badge" alt="Streamlit">
</p>

<p align="center">
  <strong>🎬 Watch the Demo:</strong> See how AI detects milk in real-time across visual, audio, and text modalities
</p>

---

## 📋 Table of Contents
- [Quick Start](#-quick-start-under-2-minutes)
- [Features](#-what-makes-this-special)
- [Technical Architecture](#-technical-architecture)
- [Project Structure](#-project-structure)
- [Using the App](#-using-the-app)
- [How the AI Works](#-how-the-ai-works)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [About the Developer](#-about-the-developer)

---

## 🚀 Quick Start (Under 2 Minutes!)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/got-milk-campaign.git
cd got-milk-campaign

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up your API key (get one free at https://playground.twelvelabs.io)
echo "TWELVE_LABS_API_KEY=tlk_YOUR_KEY_HERE" > .env
echo "CAMPAIGN_INDEX_ID=YOUR_INDEX_ID" >> .env

# 6. Launch the app!
python -m streamlit run app.py

# 🎉 App opens at http://localhost:8501
```

---

## ✨ What Makes This Special

### 🧠 **Multi-Modal AI Detection**
- **Visual Recognition**: Detects milk bottles, glasses, and cartons in any lighting condition
- **Audio Analysis**: Catches phrases like "got milk" or "chocolate milk" in speech
- **Text Detection**: Reads on-screen text and captions mentioning milk
- **2/3 Validation**: Requires multiple signals to prevent false positives

### 🎯 **Smart Campaign Management**
- **3-Tier Quarantine System**: Automatically filters out non-campaign content
- **Behavioral Mob Assignment**: Groups creators by activity (Gym Warriors 💪, Comedy Kings 😂, etc.)
- **Real-time Processing**: Instagram feed simulator shows live validation
- **Enterprise Ready**: Full logging, error handling, and export capabilities

### 📊 **Business Intelligence**
- **Engagement Analytics**: Track viral potential and creator performance
- **Export Tools**: CSV/JSON exports for further analysis
- **Confidence Scoring**: AI provides confidence levels for each detection
- **Activity Insights**: Understand where, when, and how milk is consumed

---

## 🏗️ Technical Architecture

### System Design - Media Asset Management (MAM) Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Content Ingestion Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  Instagram   │  │   TikTok     │  │   Direct    │  │   Webhook   │ │
│  │    Feed      │  │    Feed      │  │   Upload    │  │  Ingestion  │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬──────┘  └──────┬──────┘ │
└─────────┴──────────────────┴─────────────────┴────────────────┴────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Pre-Processing & Validation Layer                     │
│  ┌────────────────┐  ┌─────────────────┐  ┌────────────────────────┐  │
│  │    Metadata    │  │    Hashtag      │  │   Media Validation   │  │
│  │   Extraction   │  │    Filtering    │  │  (Format/Duration)   │  │
│  └────────────────┘  └─────────────────┘  └────────────────────────┘  │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      AI Processing Pipeline (Twelve Labs)                │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    Pegasus 1.1 - Scene Understanding              │  │
│  │  • Activity Recognition  • Location Detection  • Mood Analysis    │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                  Marengo 2.7 - Multi-Modal Search                │  │
│  │  • Visual Detection  • Audio Recognition  • Text Extraction      │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Business Logic & Decision Engine                      │
│  ┌────────────────┐  ┌─────────────────┐  ┌────────────────────────┐  │
│  │   Confidence   │  │   Quarantine    │  │    Mob Assignment    │  │
│  │    Scoring     │  │     Rules       │  │     Algorithm        │  │
│  └────────────────┘  └─────────────────┘  └────────────────────────┘  │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Data Storage & Analytics                          │
│  ┌────────────────┐  ┌─────────────────┐  ┌────────────────────────┐  │
│  │  Local State   │  │   Session Data  │  │   Export Engine      │  │
│  │  Management    │  │   (Streamlit)   │  │   (CSV/JSON)         │  │
│  └────────────────┘  └─────────────────┘  └────────────────────────┘  │
│                                                                         │
│  In Production: PostgreSQL | Redis | S3 | Elasticsearch | DataLake     │
└─────────────────────────────────────────────────────────────────────────┘
```

### Media Processing Flow

```
Video Input → Transcode → AI Analysis → Metadata Enrichment → Storage → Distribution
    │             │            │               │                │           │
    └─────────────┴────────────┴───────────────┴────────────────┴───────────┘
                            Twelve Labs Handles All of This
```

### Data Flow Architecture

```yaml
1. Ingestion:
   - Source: Social Media APIs / Direct Upload
   - Format: MP4, MOV (up to 1080p)
   - Metadata: JSON sidecar files

2. Processing:
   - Queue: In-memory (Production: RabbitMQ/SQS)
   - Workers: Async processing via Twelve Labs
   - Timeout: 120s per video

3. Storage:
   - Videos: Local filesystem (Production: S3/CDN)
   - Metadata: Session state (Production: PostgreSQL)
   - Analytics: In-memory (Production: Elasticsearch)

4. Distribution:
   - API: RESTful endpoints
   - Export: CSV/JSON batch downloads
   - Real-time: WebSocket updates (future)
```

### 🔧 **Key Technologies**
- **Twelve Labs Pegasus**: Deep video understanding for scene analysis
- **Twelve Labs Marengo**: Multi-modal search and detection
- **Streamlit**: Rapid prototyping and beautiful UI
- **Python 3.11+**: Modern async capabilities

---

## 📁 Project Structure

```
got-milk-campaign/
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
├── test_videos/          # Sample videos with metadata
│   ├── 2%/              # Regular milk videos
│   ├── choco/           # Chocolate milk videos
│   └── straw/           # Strawberry milk videos
├── Tests/               # Utility scripts
└── docs/               # Documentation
```

---

## 🎮 Using the App

### 1. **Setup Your Index** (First Time Only)
- Navigate to "Setup Index" page
- Click "Create New Index"
- Wait for confirmation (takes ~30 seconds)

### 2. **Process Videos**
- Go to "Instagram Feed" to see simulated social posts
- Watch as videos are validated in real-time
- Approved videos join behavioral mobs
- Rejected videos go to quarantine with explanations

### 3. **Explore Results**
- **Mob Explorer**: See creator communities formed by AI
- **Dashboard**: Analytics and export options
- **Tech Showcase**: Deep dive into how Twelve Labs AI works

---

## 🔬 How the AI Works

### Multi-Modal Detection Pipeline
```python
# 1. Visual Detection
"person drinking milk OR glass of milk OR milk bottle"

# 2. Audio Detection  
"'got milk' OR 'drinking milk' OR 'chocolate milk'"

# 3. Text Detection
"text 'milk' OR text 'got milk' OR text '#gotmilk'"

# Confidence score comes directly from Twelve Labs Search API
# Typical range: 83-86% for genuine milk content

```

### Behavioral Analysis
The AI doesn't just detect milk - it understands context:
- **What**: Type of milk (chocolate, strawberry, regular)
- **Where**: Location (gym, kitchen, studio)
- **How**: Activity (post-workout, cooking, comedy skit)
- **When**: Time of day and mood

---

## 🚧 Troubleshooting

### Common Issues

**"API Key Invalid"**
- Make sure you've signed up at [playground.twelvelabs.io](https://playground.twelvelabs.io)
- Check your `.env` file has the correct format
- Free tier includes 600 minutes/month

**"Index Not Found"**
- Run the Setup Index page first
- Check your CAMPAIGN_INDEX_ID in `.env` matches

**"Processing Takes Forever"**
- Normal processing time: 80-120 seconds per video
- This is Twelve Labs doing deep AI analysis, not a bug!

**"Low Confidence Scores / Search Not Working Properly"** ⚠️
- **Check your Twelve Labs storage!** If your account storage is full, the Search API may not return results properly
- This can cause confidence scores to be 0 or much lower than expected (should be 83-86%)
- Solution: Delete old indexes/videos in your [Twelve Labs Console](https://console.twelvelabs.io)
- Free tier storage limit can fill up quickly with testing

---

## 🤝 Contributing

Found a bug? Want to add a feature? PRs welcome!

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👨‍💻 About the Developer

**Eric Osherow** | [LinkedIn](https://www.linkedin.com/in/eric-osherow/) | [Email](mailto:eric.osherow@gmail.com)

AI Product Leader with deep experience in video/media platforms and computer vision. Previously:

- **Founder & CEO @ SeaDeep**: Built AI-powered video analysis for underwater infrastructure monitoring, processing thousands of hours of subsea footage for autonomous detection and classification
- **Product Specialist @ NBCUniversal**: Managed AI-enabled video management systems for Peacock, NBC, and the Winter Olympics
- **Product Manager @ Disney**: Supported Disney+ global platform integration

This project showcases my expertise in:
- 🎥 **Multi-modal video AI** (from SeaDeep's underwater vision systems)
- 📺 **Media platform development** (from NBC/Disney experience)
- 🚀 **0→1 product development** (from multiple startup experiences)
- 🤖 **Practical AI implementation** (making complex AI accessible)

Built with passion for the Twelve Labs team - let's revolutionize video understanding together!

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Made with ☕ and 🥛 by Eric Osherow
</p>
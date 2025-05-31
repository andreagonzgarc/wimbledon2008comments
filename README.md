# Wimbledon 2008 Full Match Final YouTube Comment Analyzer  
**Econometrics Final Project**  
*Analyzes comments from the Nadal-Federer 2008 Wimbledon final Full Match Youtube Video*

## 📌 Purpose  
This code sorts all uploads > 60s from the Wimbledon's Youtube Channel by number of views. Out of the 30 most viewed videos, the code finds the legendary Nadal-Federer Wimbledon 2008 Final, referred by some as the greatest tennis match of all time, as the longest video (6:13:16) of that list (with 4.3M views!) and retrieves all the available comments of the video.

## 🛠️ Setup  
1. Clone this repo:  
   ```bash
   git clone https://github.com/yourusername/nadalrg25-api.git
   ```
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
3. Add your YouTube API key to `.env`:  
   ```text
   API_KEY=your_key_here
   ```

## 🚀 Usage  
```bash
python code/wimby08.py
```
- Output saves to `data/wimbledon_comments_[VIDEO_ID].csv`

## 📂 Dataset Columns  
| Column | Description |  
|--------|-------------|  
| `comment_text` | Raw comment text |  
| `timestamp` | When comment was posted |  
| `author` | Commenter's display name |  
| `video_title` | Source video title (*identifies data source*) |  
| `video_url` | Direct YouTube URL |  

## 📝 Project Requirements  
- YouTube Data API v3  
- Python 3.9+  
- Libraries in `requirements.txt`
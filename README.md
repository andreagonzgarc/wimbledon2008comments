# Wimbledon 2008 Full Match Final YouTube Comment Analyzer  
**Econometría Aplicada II Final Project**  
*Analyzes comments from the Nadal-Federer 2008 Wimbledon final Full Match Youtube Video*

## 📌 Purpose  
This pipeline:
1. Fetches all videos >60s from Wimbledon's YouTube channel
2. Identifies the top 30 most-viewed videos
3. Selects the longest video (Nadal-Federer 2008 Final, 6:13:16 duration)
4. Scrapes all available comments (500+)
5. Generates a reproducible dataset for econometric analysis

## 🛠️ Setup  
1. Clone this repo:  
   ```bash
   git clone https://github.com/yourusername/wimbledon2008comments.git
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
- Output saves to `data/wimbledon_comments_[VIDEO_ID].csv` (since all comments correspond to the same video the id column is omitted.)
## 📂 Dataset Columns  
| Column      | Description |  
|-------------|-------------|  
| `Number`    | comment id (1 = latest comment, n = first available) |  
| `Timestamp` | When comment was posted |  
| `Author`    | Commenter's display name |  
| `Comment`   | Comment |

## 📝 Project Requirements  
- YouTube Data API v3  
- Python 3.9+  
- Libraries in `requirements.txt`
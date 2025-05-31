"""
wimby08.py - Wimbledon YouTube Analytics Tool
Fetches top videos and comments from Wimbledon's YouTube channel
"""

import os
import csv
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration
MAX_RESULTS = 30
COMMENTS_LIMIT = 100  # Max per API request
MIN_DURATION = 60  # Minimum video duration in seconds
DATA_FOLDER = "data"  # Folder for storing CSV files

class YouTubeAnalyzer:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)
    
    def get_channel_id(self, channel_name):
        """Get channel ID by name"""
        request = self.youtube.search().list(
            part='snippet',
            q=channel_name,
            type='channel',
            maxResults=1
        )
        return request.execute()['items'][0]['id']['channelId']
    
    def get_uploads_playlist(self, channel_id):
        """Get uploads playlist ID for a channel"""
        request = self.youtube.channels().list(
            part='contentDetails',
            id=channel_id
        )
        return request.execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    @staticmethod
    def parse_duration(duration_str):
        """Parse YouTube duration format (PT1H2M30S) to seconds"""
        duration = duration_str[2:]
        total_seconds = 0
        
        for unit, multiplier in [('H', 3600), ('M', 60), ('S', 1)]:
            if unit in duration:
                val, duration = duration.split(unit)
                total_seconds += int(val) * multiplier
        return total_seconds
    
    def get_channel_videos(self, playlist_id):
        """Get all videos from a playlist with duration > MIN_DURATION"""
        videos = []
        next_page_token = None
        
        while True:
            try:
                playlist_items = self.youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                ).execute()
                
                video_ids = [item['contentDetails']['videoId'] for item in playlist_items['items']]
                
                for i in range(0, len(video_ids), 50):
                    batch = video_ids[i:i+50]
                    video_details = self.youtube.videos().list(
                        part='snippet,statistics,contentDetails',
                        id=','.join(batch)
                    ).execute()
                    
                    for video in video_details['items']:
                        duration = self.parse_duration(video['contentDetails']['duration'])
                        if duration > MIN_DURATION:
                            video['duration_seconds'] = duration
                            video['duration_str'] = str(timedelta(seconds=duration))
                            videos.append(video)
                
                next_page_token = playlist_items.get('nextPageToken')
                if not next_page_token:
                    break
                    
                time.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                print(f"Error fetching videos: {e}")
                break
        
        return videos
    
    def get_video_comments(self, video_id, max_comments=None):
        """Get all comments for a video with timestamps"""
        comments = []
        next_page_token = None
        
        while True:
            try:
                request = self.youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=min(COMMENTS_LIMIT, max_comments) if max_comments else COMMENTS_LIMIT,
                    pageToken=next_page_token,
                    order='time',
                    textFormat='plainText'
                )
                response = request.execute()
                
                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']
                    comments.append({
                        'text': comment['textDisplay'],
                        'timestamp': datetime.strptime(
                            comment['publishedAt'], 
                            '%Y-%m-%dT%H:%M:%SZ'
                        ).strftime('%Y-%m-%d %H:%M:%S'),
                        'author': comment['authorDisplayName']
                    })
                
                    if max_comments and len(comments) >= max_comments:
                        return comments
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
                
                time.sleep(1)
                
            except HttpError as e:
                if e.resp.status == 403:
                    print("API quota exceeded")
                break
            except Exception as e:
                print(f"Error fetching comments: {e}")
                break
        
        return comments
    
    @staticmethod
    def save_to_csv(data, filename):
        """Save data to CSV file"""
        # Create data folder if it doesn't exist
        os.makedirs(DATA_FOLDER, exist_ok=True)
        
        # Create full path
        full_path = os.path.join(DATA_FOLDER, filename)
        
        with open(full_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Number', 'Timestamp', 'Author', 'Comment'])
            for i, item in enumerate(data, 1):
                writer.writerow([i, item['timestamp'], item['author'], item['text']])
        return full_path  # Return the full path where file was saved

def main():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    
    analyzer = YouTubeAnalyzer(api_key)
    
    # 1. Get channel info
    print("Fetching Wimbledon channel data...")
    channel_id = analyzer.get_channel_id('Wimbledon')
    playlist_id = analyzer.get_uploads_playlist(channel_id)
    
    # 2. Get all videos
    print("Fetching videos...")
    videos = analyzer.get_channel_videos(playlist_id)
    
    # 3. Get top viewed videos
    top_videos = sorted(
        videos,
        key=lambda x: int(x['statistics'].get('viewCount', 0)),
        reverse=True
    )[:MAX_RESULTS]
    
    # 4. Get longest videos from top viewed
    longest_videos = sorted(
        top_videos,
        key=lambda x: x['duration_seconds'],
        reverse=True
    )
    
    # 5. Get comments for longest video
    if longest_videos:
        longest_video = longest_videos[0]
        print(f"\nFetching comments for: {longest_video['snippet']['title']}")
        comments = analyzer.get_video_comments(longest_video['id'])
        
        # Save to CSV
        filename = f"wimbledon_comments_{longest_video['id']}.csv"
        saved_path = analyzer.save_to_csv(comments, filename)
        print(f"Saved {len(comments)} comments to {saved_path}")
    else:
        print("No videos found meeting criteria")

if __name__ == "__main__":
    main()
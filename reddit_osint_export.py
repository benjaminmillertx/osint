🛠 Requirements 
bash
Copy
Edit
pip install praw

🧠 Full Script with Export — reddit_osint_export.py
python
Copy
Edit
import praw
import json
from datetime import datetime

# Reddit API setup
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="RedditOSINT by u/YourRedditUsername"
)

def analyze_user(username):
    data = {}
    try:
        user = reddit.redditor(username)
        data["username"] = user.name
        data["link_karma"] = user.link_karma
        data["comment_karma"] = user.comment_karma
        data["created_utc"] = datetime.utcfromtimestamp(user.created_utc).strftime('%Y-%m-%d %H:%M:%S')

        print(f"\n📋 USER: u/{user.name}")
        print(f"🔗 Link karma: {user.link_karma}")
        print(f"💬 Comment karma: {user.comment_karma}")
        print(f"📅 Account created: {data['created_utc']}")

        # Posts
        posts = []
        print("\n📄 Recent Posts:")
        for submission in user.submissions.new(limit=5):
            post_info = {
                "subreddit": str(submission.subreddit),
                "title": submission.title,
                "score": submission.score,
                "url": submission.url
            }
            posts.append(post_info)
            print(f"- r/{post_info['subreddit']}: {post_info['title']} (👍 {post_info['score']})")
        data["recent_posts"] = posts

        # Comments
        comments = []
        print("\n💬 Recent Comments:")
        for comment in user.comments.new(limit=5):
            comment_info = {
                "subreddit": str(comment.subreddit),
                "body": comment.body[:100],
                "score": comment.score,
                "permalink": f"https://reddit.com{comment.permalink}"
            }
            comments

🛠 Requirements 
bash
Copy
Edit
pip install praw

import praw
import json
from datetime import datetime

# Initialize Reddit API (read-only)
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

        # Recent posts
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

        # Recent comments
        comments = []
        print("\n💬 Recent Comments:")
        for comment in user.comments.new(limit=5):
            comment_info = {
                "subreddit": str(comment.subreddit),
                "body": comment.body[:100],
                "score": comment.score,
                "permalink": f"https://reddit.com{comment.permalink}"
            }
            comments.append(comment_info)
            print(f"- r/{comment_info['subreddit']}: {comment_info['body']} (👍 {comment_info['score']})")
        data["recent_comments"] = comments

        # Active subreddits
        print("\n📊 Active Subreddits:")
        active_subs = set()
        for comment in user.comments.new(limit=50):
            active_subs.add(str(comment.subreddit))
        for submission in user.submissions.new(limit=50):
            active_subs.add(str(submission.subreddit))
        active_list = sorted(active_subs)
        data["active_subreddits"] = active_list
        print(", ".join(active_list))

        # Save as JSON
        json_filename = f"{username}_data.json"
        with open(json_filename, "w", encoding="utf-8") as jf:
            json.dump(data, jf, indent=4)
        print(f"\n📁 Saved JSON to {json_filename}")

        # Save as TXT
        txt_filename = f"{username}_data.txt"
        with open(txt_filename, "w", encoding="utf-8") as tf:
            tf.write(f"Reddit OSINT Report for u/{data['username']}\n")
            tf.write(f"Link Karma: {data['link_karma']}\n")
            tf.write(f"Comment Karma: {data['comment_karma']}\n")
            tf.write(f"Created: {data['created_utc']}\n\n")

            tf.write("Recent Posts:\n")
            for p in posts:
                tf.write(f"- r/{p['subreddit']}: {p['title']} (👍 {p['score']})\n")

            tf.write("\nRecent Comments:\n")
            for c in comments:
                tf.write(f"- r/{c['subreddit']}: {c['body']} (👍 {c['score']})\n")

            tf.write("\nActive Subreddits:\n")
            tf.write(", ".join(active_list))
        print(f"📁 Saved TXT to {txt_filename}")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    target = input("🔎 Enter Reddit username (without u/): ").strip()
    analyze_user(target)

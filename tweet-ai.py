import os
import random
import json
import requests
from requests_oauthlib import OAuth1

# --- 環境変数からAPIキー取得 ---
API_KEY            = os.getenv("TWITTER_API_KEY3")
API_SECRET_KEY     = os.getenv("TWITTER_API_SECRET_KEY3")
ACCESS_TOKEN       = os.getenv("TWITTER_ACCESS_TOKEN3")
ACCESS_TOKEN_SECRET= os.getenv("TWITTER_API_SECRET_SECRET3")

# --- 投稿候補（外部JSONに300本） ---
with open("ai_side_hustle_posts.json", "r", encoding="utf-8") as f:
    TWEET_CANDIDATES = json.load(f)

# --- 付与するハッシュタグ ---
HASHTAGS = "#AI副業 #生成AI #ChatGPT活用 #副業初心者"

# --- 使用済みツイート記録ファイル ---
USED_TWEETS_FILE = "used_ai_tweets.json"

# --- OAuth1認証オブジェクト作成 ---
auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# --- 使用済みツイート読み込み ---
def load_used_tweets() -> list[int]:
    if os.path.exists(USED_TWEETS_FILE):
        with open(USED_TWEETS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# --- 使用済みツイート保存 ---
def save_used_tweets(used_indices: list[int]) -> None:
    with open(USED_TWEETS_FILE, "w", encoding="utf-8") as f:
        json.dump(used_indices, f, ensure_ascii=False, indent=2)

# --- 投稿処理 ---
def post_tweet(text: str) -> None:
    url = "https://api.twitter.com/2/tweets"
    payload = {"text": text.strip()}
    r = requests.post(url, auth=auth, json=payload, timeout=30)

    if r.status_code == 201:
        print("✅ 投稿成功:", r.json()["data"]["id"])
    else:
        print("❌ 投稿失敗:", r.text)
        r.raise_for_status()

# --- メイン ---
if __name__ == "__main__":
    used = load_used_tweets()
    pool = [i for i in range(len(TWEET_CANDIDATES)) if i not in used]

    if not pool:                 # 全て使い切ったらリセット
        print("All tweets used — resetting history.")
        used = []
        pool = list(range(len(TWEET_CANDIDATES)))

    idx = random.choice(pool)
    body = TWEET_CANDIDATES[idx]
    tweet = f"{body}\n\n{HASHTAGS}"

    post_tweet(tweet)
    used.append(idx)
    save_used_tweets(used)

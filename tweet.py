import os
import requests
from requests_oauthlib import OAuth1
import random
import datetime

# --- 必要な環境変数を読み込み ---
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# --- 曜日ごとのツイートパターン ---
# 0=月, 1=火, 2=水, 3=木, 4=金, 5=土, 6=日
TWEETS = {
    0: [  # 月曜日
        """
今日ムラムラする。。
誰かに舐められたい
#舐め犬募集
""",
        """
最近一人でするときav観るんだけど、顔にまたがられて舐めさせられる場面でよくイッちゃう(/-＼*)
""",
        """
今日はローターに日
""",        
    ],
    1: [  # 火曜日
        """
今日はオナして寝ます🐶
また明日💗
""",  
        """
池袋いる、舐め犬いないかな、、、
#舐め犬
""",  
    ],
    2: [  # 水曜日
        """
仕事のストレスやばいから誰かに舐めてほしいなあ
#舐め犬
""",  
        """
今日新宿の漫喫で誰か舐めてくれる人いるかな？
#舐め犬
""",  
    ],
    3: [  # 木曜日
        """
クンニして顔騎した時潮ふいてもいいかな？
""",  
        """
舐められたい
""",  
    ],
    4: [  # 金曜日
        """
クンニしてくれる人がタイプです
""",  
        """
クンニしてクンニして舐めて舐めて
毎日頭の中これ⬆️
""",  
    ],
    5: [  # 土曜日
        """
めちゃくちゃむらむらする
舐めて欲しくなるよ、、
""",  
        """
クンニしてほしい沢山舐めてぐちょぐちょにして？
""",  
    ],
    6: [  # 日曜日
        """
舐められるの想像するだけで
愛液が垂れちゃうくらい下着びしょびしょになる‥
""",  
        """
セックスより舐められるのが好きです
""",  
    ],
}

# --- OAuth1認証オブジェクト作成 ---
auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# --- ランダム絵文字リスト ---
EMOJIS = ["✨", "🌟", "🔥", "🎯", "💡", "👅", "🎉", "📣", "🏆", "🥇", "✅", "🥳", "💥", "🛫", "🏖️", "🍀", "🎶", "📢", "💗", "🎈", "🍭"]

# --- 投稿処理 ---
def post_tweet(text):
    url = "https://api.twitter.com/2/tweets"
    headers = {"Content-Type": "application/json"}
    emoji = random.choice(EMOJIS)
    payload = {"text": f"{text.strip()} {emoji}"}

    resp = requests.post(url, headers=headers, json=payload, auth=auth, timeout=30)

    if resp.status_code == 201:
        print("✅ 投稿成功:", resp.json())
    else:
        print("❌ 投稿失敗:", resp.text)
        resp.raise_for_status()

# --- メイン ---
if __name__ == "__main__":
    try:
        today = datetime.datetime.today().weekday()  # 今日の曜日番号 (0〜6)
        todays_tweets = TWEETS.get(today, [])

        if todays_tweets:
            tweet = random.choice(todays_tweets)  # 今日のリストからランダムで1つ選ぶ
            post_tweet(tweet)
        else:
            print("今日に対応するツイートが設定されていません。")

    except Exception as e:
        print("エラー:", e)

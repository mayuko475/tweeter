import os
import random
import json
import requests
from requests_oauthlib import OAuth1

# --- 環境変数からAPIキー取得 ---
API_KEY = os.getenv("TWITTER_API_KEY2")
API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY2")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN2")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET2")

# --- 投稿候補（バズポスト40本） ---
TWEET_CANDIDATES = [
    """💬【好きな人とのLINEで脈ありサイン】
返信が早いとかよりも、
「話題を自然に続けようとする」方が本物。
→ この意識があるなら、脈ありです。
（保存推奨）""",
    """💬【LINEで好かれる人がやってる返信術】
📝ポイントは3つ
・即レスしすぎない
・疑問形で返す
・時々"小ネタ"を挟む
意図的に会話を育てる人は強い。""",
    """💬【返信が遅い＝脈なし？】
結論。
返信スピードより「文の熱量」で見るべき。
遅くても、長文・丁寧・質問ありなら
ちゃんと大事に思われてます。""",
    """💬【LINEで嫌われないための鉄則】
返信に困ったら、とにかく
「リアクション＋質問返し」だけしておけばOK。
沈黙恐れず、無理に盛り上げようとしないこと。""",
    """💬【既読スルーされる人の特徴】
× 話を終わらせない
× 自分語りが長い
× 無理に繋げようとする
→「自然に会話が終わる」ことを怖がらない人が好かれます。""",
    """💬【LINEだけで惚れられる技術】
「感情を乗せる」だけ。
例：
「すごい！！！」
「嬉しすぎる😭」
「まじでそれ好き！」
文字だけだからこそ、感情表現が大事。""",
    """💬【好きな人に送るべき神LINE】
ただの世間話より、
「あなたとだから話したい」というニュアンスを入れる。
これが刺さる。""",
    """💬【LINE頻度で測る恋愛の脈あり・脈なし】
脈あり→会話が続いてる
脈なし→業務連絡みたいなやりとりだけ
※既読無視より怖いのは「盛り上がらない」こと。""",
    """💬【恋愛初期LINEで気をつけるべきNGワード】
- 「なんで返信くれないの？」
- 「俺のこと嫌い？」
- 「今何してるの？」
→これ、重さ爆発するので要注意。""",
    """💬【好きな人との距離を縮めるLINEテク】
「相談する→ありがとうを伝える」
相談は心の距離を近づける最強ツール。
小さな相談でもいいから積極的に。""",
    
    # 恋愛心理・駆け引き系（10本）
    """💬【追われる人の共通点】
・自分に満足してる
・依存しない
・感謝できる
だから魅力的なんです。""",
    """💬【人は"わからないもの"に惹かれる】
完璧にわかりきった人より、
「まだ知りたい」と思わせる人が恋愛で強い。""",
    """💬【男女共通：恋が冷める瞬間】
"重すぎる愛情"は、時に毒になる。
愛は、軽やかさがちょうどいい。""",
    """💬【会うたび惹かれる人の秘密】
→ 毎回「ちょっとだけ違う自分」を見せる。
小さなギャップが、ドキドキを生む。""",
    """💬【モテる人が自然にやってること】
相手に
「自分は特別だ」と思わせる会話。
小さな気遣いが魔法。""",
    """💬【恋愛はタイミングが9割】
気持ちが盛り上がっている時に
1歩踏み込める人が、恋を掴む。""",
    """💬【恋愛の駆け引きで大事なこと】
"やりすぎない"こと。
あくまで自然体に。演技はバレます。""",
    """💬【好きな人に飽きられない秘訣】
定期的に、
「意外な一面」を小出しにすること。
人間はサプライズに弱い。""",
    """💬【心理テク：単純接触効果】
何度も接するだけで、好きになりやすくなる。
→ だから、LINE頻度を"ちょうどよく"キープしよう。""",
    """💬【好きな人を振り向かせる最初のステップ】
まず、
「自分を好きになること」から始める。
これが一番効く。""",
    
    # 失恋・エモ系（10本）
    """💬【失恋で辛い時に読んで】
"運命の人"とは、
必ずしも今すぐ出会うものじゃない。
今は、その準備期間かもしれない。""",
    """💬【忘れられない人がいるなら】
無理に忘れなくていい。
"思い出にする"だけでいいんだよ。""",
    """💬【恋愛で傷ついたあなたへ】
誰かに傷つけられた心は、
誰かの優しさで癒されることもある。
焦らなくていい。""",
    """💬【恋愛は全部、経験値になる】
報われなかった想いも、
必ずあなたを強く、優しくしてる。""",
    """💬【大丈夫、また恋できるよ】
今、そう思えなくても。
少しずつでいい。
心はちゃんと回復するから。""",
    """💬【失恋直後の自分に言いたいこと】
「今は泣いていい。」
泣きたいだけ泣いていいんだよ。""",
    """💬【恋愛で後悔した時に】
後悔するってことは、
本気で好きだった証拠。
その想いは、本物だったんだ。""",
    """💬【愛された記憶は、消えない】
辛いけど、
あの時、確かに誰かと心が繋がった。
それは奇跡。""",
    """💬【失恋後に一番大事なこと】
「自分を責めないこと。」
恋愛は、いつだって二人のものだから。""",
    """💬【恋愛に疲れたあなたへ】
恋愛って、
頑張りすぎるものじゃないよ。
もっと、ラクでいい。""",
    
    # 自己成長・自己分析系（10本）
    """💬【恋愛がうまくいかない時】
まずは、
自分自身を大切にできてるかをチェックしよう。""",
    """💬【恋愛も仕事も上手くいく人】
「素直に謝れる人」
これだけで人間関係の9割勝てる。""",
    """💬【本当に好きな人を見極める方法】
一緒にいて
「頑張らなくていい」と思える人か？""",
    """💬【恋愛で無理してるなと思ったら】
→ 立ち止まっていい。
恋は、走り続けるだけじゃないから。""",
    """💬【恋愛経験が少なくても大丈夫】
大事なのは数じゃない。
「一度の恋を、どれだけ大切にできたか」""",
    """💬【好きな人ができたら大事にしたいこと】
「相手を変えようとしない」
そのままの相手を受け止める覚悟。""",
    """💬【恋愛における最大の武器】
"自分を好きでいること"
これが、最強で最高の魅力。""",
    """💬【焦って恋愛しないでいい】
恋愛は競争じゃない。
あなたのペースで、大丈夫。""",
    """💬【恋愛の自己肯定感チェック】
✅ 自分の好きなところ、5個言える？
言えなかったら、今から増やしていこう。""",
    """💬【恋愛上手になるために】
たったひとつ
「相手を知ろうとする努力」をやめないこと。
これだけで十分。"""
]

# --- 付与するハッシュタグ ---
HASHTAGS = "#恋愛 #恋愛垢さんと繋がりたい #恋愛心理学"

# --- 使用済みツイート記録ファイル ---
USED_TWEETS_FILE = "used_tweets.json"

# --- OAuth1認証オブジェクト作成 ---
auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# --- ランダム絵文字リスト ---
EMOJIS = ["✨", "🌟", "🔥", "🎯", "💡", "🎉", "📣", "🏆", "🥇", "✅", "🥳", "💥", "🛫", "🏖️", "🍀", "🎶", "📢", "💗", "🎈", "🍭"]

# --- 使用済みツイート読み込み ---
def load_used_tweets():
    if os.path.exists(USED_TWEETS_FILE):
        with open(USED_TWEETS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# --- 使用済みツイート保存 ---
def save_used_tweets(used_indices):
    with open(USED_TWEETS_FILE, "w", encoding="utf-8") as f:
        json.dump(used_indices, f)

# --- 投稿処理 ---
def post_tweet(text):
    url = "https://api.twitter.com/2/tweets"
    payload = {"text": text.strip()}

    response = requests.post(url, auth=auth, json=payload, timeout=30)

    if response.status_code == 201:
        print("✅ 投稿成功:", response.json())
    else:
        print("❌ 投稿失敗:", response.text)
        response.raise_for_status()

# --- メイン ---
if __name__ == "__main__":
    used_indices = load_used_tweets()

    # 使ってないツイートだけ選ぶ
    available_indices = [i for i in range(len(TWEET_CANDIDATES)) if i not in used_indices]

    # 全部使い切ったらリセット
    if not available_indices:
        print("すべてのツイートを使い切ったためリセットします。")
        used_indices = []
        available_indices = list(range(len(TWEET_CANDIDATES)))

    selected_index = random.choice(available_indices)
    selected_text = TWEET_CANDIDATES[selected_index]

    # ハッシュタグ＆ランダム絵文字付与
    emoji = random.choice(EMOJIS)
    final_text = f"{selected_text}\n\n{HASHTAGS} {emoji}"

    # 投稿
    post_tweet(final_text)

    # 使用済み記録を更新
    used_indices.append(selected_index)
    save_used_tweets(used_indices)

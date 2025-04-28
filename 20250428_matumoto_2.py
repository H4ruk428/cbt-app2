# CBTアプリ with 選べるキャラクター＆成長＆バッジシステム
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date

# ←★ここで最初に st.set_page_config を書く
st.set_page_config(page_title="CBT育成アプリ", layout="centered")


# データ保存ファイル
USER_DATA_FILE = "user_data.json"
RECORDS_FILE = "cbt_records.csv"

# キャラクター設定
CHARACTERS = {
    "ふくろう": ["owl_lv1.png", "owl_lv2.png", "owl_lv3.png", "owl_lv4.png"],
    "リス": ["squirrel_lv1.png", "squirrel_lv2.png", "squirrel_lv3.png", "squirrel_lv4.png"],
    "こぐま": ["bear_lv1.png", "bear_lv2.png", "bear_lv3.png", "bear_lv4.png"],
    "ねこ": ["cat_lv1.png", "cat_lv2.png", "cat_lv3.png", "cat_lv4.png"],
}

# 背景画像
BACKGROUNDS = {
    "デフォルト": "bg_default.png",
    "さくら": "bg_sakura.png",
    "ゆき": "bg_snow.png",
    "ほしぞら": "bg_starry.png"
}

# ユーザーデータロード
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "character": None,
            "points": 0,
            "records": 0,
            "badges": [],
            "last_login_date": "",
            "login_days": 0,
            "background": "デフォルト"
        }

# ユーザーデータ保存
def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f)

user_data = load_user_data()

# 初回キャラ選択
if user_data["character"] is None:
    st.title("🌟キャラクターを選んでね！")
    choice = st.selectbox("好きなキャラクターを選んでください", list(CHARACTERS.keys()))
    if st.button("決定！"):
        user_data["character"] = choice
        save_user_data(user_data)
        st.success(f"{choice} を育てよう！")
        st.stop()

# 成長レベル判定
def get_level(records, login_days):
    if records >= 20 and login_days >= 10:
        return 3
    elif records >= 10:
        return 2
    elif records >= 5:
        return 1
    else:
        return 0

# 今日初回ログインならボーナス
today = str(date.today())
if user_data.get("last_login_date") != today:
    user_data["points"] += 1  # ログインボーナス
    user_data["login_days"] += 1
    user_data["last_login_date"] = today
    save_user_data(user_data)
    st.success("🎁 ログインボーナス＋1pt！")

# キャラクター＆背景表示
st.image(BACKGROUNDS.get(user_data["background"], "bg_default.png"), use_container_width=True)

level = get_level(user_data["records"], user_data["login_days"])
char_image = CHARACTERS[user_data["character"]][level]
st.image(char_image, use_container_width=True)  # 修正：use_container_width=Trueに変更
st.write(f"【{user_data['character']}】育成中🌱")
st.write(f"現在のポイント：{user_data['points']}pt / 記録数：{user_data['records']}回 / ログイン日数：{user_data['login_days']}日")

# 背景変更オプション
st.markdown("---")
st.subheader("🎨 背景を変更しよう！（30ptで開放）")
selected_bg = st.selectbox("背景を選ぶ", list(BACKGROUNDS.keys()))
if selected_bg != user_data["background"] and st.button("背景を変更する"):
    if user_data["points"] >= 30:
        user_data["background"] = selected_bg
        user_data["points"] -= 30
        save_user_data(user_data)
        st.success(f"背景を{selected_bg}に変更したよ！")
    else:
        st.error("ポイントが足りません！")

# ------------------------
# 4種類のCBTワーク選択と入力
# ------------------------

st.markdown("---")
st.title("📝 CBTワークに取り組もう！")

cbt_type = st.selectbox(
    "ワークの種類を選んでね",
    ("① 認知再構成法", "② 行動活性化", "③ 問題解決技法", "④ ストレスコーピング")
)

st.write("🌟ワークに取り組むとキャラクターが育ち、ポイントも増えます！")

record_data = {"日付": today, "ワーク": cbt_type}

# それぞれワークごとの内容
if cbt_type == "① 認知再構成法":
    st.subheader("ストレス場面を振り返ろう")
    situation = st.text_input("どんな状況だった？")
    thought = st.selectbox("そのときどんな考えが浮かんだ？", ["失敗するかも", "嫌われたかも", "うまくいかない", "他"])
    evidence = st.text_area("その考えを支える証拠は？")
    alternative = st.text_area("別の見方をすると？")
    
    record_data.update({
        "状況": situation,
        "自動思考": thought,
        "証拠": evidence,
        "別の視点": alternative
    })

elif cbt_type == "② 行動活性化":
    st.subheader("行動予定を立てよう")
    plan = st.text_input("今週やってみたいこと")
    motivation = st.selectbox("やる気度は？", ["低い", "普通", "高い"])
    pleasure = st.selectbox("楽しそう？", ["全く", "まあまあ", "とても楽しみ"])

    record_data.update({
        "行動計画": plan,
        "やる気度": motivation,
        "楽しさ": pleasure
    })

elif cbt_type == "③ 問題解決技法":
    st.subheader("問題を整理してみよう")
    problem = st.text_area("困っていることを書こう")
    ideas = st.text_area("どんな解決策が考えられる？（箇条書きでもOK）")
    action = st.text_area("できそうな行動を一つ決めよう")

    record_data.update({
        "問題": problem,
        "解決案": ideas,
        "実行計画": action
    })

elif cbt_type == "④ ストレスコーピング":
    st.subheader("ストレスを上手に減らそう")
    feeling = st.selectbox("今の気分は？", ["緊張", "不安", "怒り", "悲しみ"])
    coping = st.text_area("どんな対処をしてみた？（呼吸法・リラクゼーションなど）")
    result = st.selectbox("その後の気分は？", ["少し楽になった", "変わらない", "悪化した"])

    record_data.update({
        "感情": feeling,
        "対処法": coping,
        "結果": result
    })

# ------------------------
# ワークの提出
# ------------------------
if st.button("提出する！"):
    if not os.path.exists(RECORDS_FILE):
        records_df = pd.DataFrame()
    else:
        records_df = pd.read_csv(RECORDS_FILE)
    
    records_df = pd.concat([records_df, pd.DataFrame([record_data])], ignore_index=True)
    records_df.to_csv(RECORDS_FILE, index=False)
    
    # 成長
    user_data["records"] += 1
    user_data["points"] += 3  # ワーク提出でポイント加算
    save_user_data(user_data)

    st.success("ワークを提出しました！🎉 ポイント＋3pt")

    # バッジ獲得判定
    new_badges = []
    if user_data["records"] == 1:
        new_badges.append("初ワーク達成！")
    if user_data["records"] == 5:
        new_badges.append("5回提出マスター")
    if user_data["records"] == 10:
        new_badges.append("ワークの達人")
    if user_data["login_days"] >= 7:
        new_badges.append("1週間継続記念")
    if user_data["points"] >= 50:
        new_badges.append("ポイント王")
    
    for badge in new_badges:
        if badge not in user_data["badges"]:
            user_data["badges"].append(badge)
            st.balloons()
            st.success(f"🏅 バッジ獲得！：{badge}")
    
    save_user_data(user_data)
    st.stop()

# ------------------------
# ワーク履歴を表示
# ------------------------
st.markdown("---")
st.subheader("📚 あなたのワーク履歴")

if os.path.exists(RECORDS_FILE):
    records_df = pd.read_csv(RECORDS_FILE)
    st.dataframe(records_df)
else:
    st.write("まだ記録がありません。")
    
# ------------------------
# バッジコレクション表示
# ------------------------
st.markdown("---")
st.subheader("🏅 獲得バッジ一覧")
if user_data["badges"]:
    for badge in user_data["badges"]:
        st.write(f"・{badge}")
else:
    st.write("まだバッジはありません。")

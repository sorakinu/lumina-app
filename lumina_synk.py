import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import os

# --- 設定 ---
DATA_PATH = "shunkan_log.csv"

# ページの設定
st.set_page_config(page_title="Lumina Connect", layout="wide")

# セッション状態（光の演出の管理）の初期化
if 'light_state' not in st.session_state:
    st.session_state.light_state = "none"

# --- ログ保存関数 ---
def save_log(status):
    file_exists = os.path.isfile(DATA_PATH)
    now = datetime.now()
    df = pd.DataFrame([[now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), status]], 
                      columns=["Date", "Time", "Status"])
    df.to_csv(DATA_PATH, mode='a', header=not file_exists, index=False, encoding='utf-8')

# --- 先生用操作パネル ---
st.title("Lumina 管理パネル（先生用）")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("1. 悩み（グレー）"):
        st.session_state.light_state = "thinking"
        save_log("悩み/潜伏")
        st.rerun()

with col2:
    if st.button("2. ヒント（太陽）"):
        st.session_state.light_state = "hint"
        save_log("ヒント（太陽）")
        st.rerun()

with col3:
    if st.button("3. 解決（黄色の星）"):
        st.session_state.light_state = "solved"
        save_log("解決（星空）")
        st.rerun()

with col4:
    if st.button("リセット"):
        st.session_state.light_state = "none"
        st.rerun()

st.divider()

# --- 生徒用受光画面（HTML/JavaScriptの埋め込み） ---
# 先生のボタン操作（light_state）をJavaScriptに伝えます
html_code = f"""
<div id="screen" style="width:100%; height:400px; position:relative; overflow:hidden; border-radius:15px; background-color:#f5f5f5; transition: background 3s ease;">
    <div id="sun" style="position:absolute; top:50%; left:50%; width:20px; height:20px; background:#FFD700; border-radius:50%; transform:translate(-50%,-50%) scale(0); opacity:0; z-index:10;"></div>
    <div id="stars-container"></div>
    <div id="status" style="position:absolute; top:20px; width:100%; text-align:center; font-family:sans-serif; font-size:1.5rem; font-weight:bold; color:#444; z-index:20;"></div>
</div>

<style>
    .sun-animate {{ animation: sun-expand 1.5s ease-out forwards; }}
    @keyframes sun-expand {{
        0% {{ transform: translate(-50%, -50%) scale(0); opacity: 1; }}
        100% {{ transform: translate(-50%, -50%) scale(100); opacity: 0; }}
    }}
    .star {{
        position: absolute; background: #FFEB3B; border-radius: 50%;
        box-shadow: 0 0 8px 2px #FFEB3B; animation: twinkle 2s infinite ease-in-out;
    }}
    @keyframes twinkle {{
        0%, 100% {{ opacity: 0.3; transform: scale(0.6); }}
        50% {{ opacity: 1; transform: scale(1.4); }}
    }}
</style>

<script>
    const screen = document.getElementById('screen');
    const sun = document.getElementById('sun');
    const status = document.getElementById('status');
    const starsContainer = document.getElementById('stars-container');
    const state = "{st.session_state.light_state}";

    if (state === "thinking") {{
        screen.style.backgroundColor = "#d3d3d3";
        status.innerText = "深く考えています...";
    }} else if (state === "hint") {{
        sun.classList.add('sun-animate');
        status.innerText = "先生のヒントが光りました";
    }} else if (state === "solved") {{
        screen.style.backgroundColor = "#E0F7FA";
        status.innerText = "光り輝く突破！";
        for (let i = 0; i < 80; i++) {{
            const star = document.createElement('div');
            star.className = 'star';
            star.style.width = star.style.height = (Math.random() * 5 + 3) + 'px';
            star.style.top = Math.random() * 100 + '%';
            star.style.left = Math.random() * 100 + '%';
            star.style.animationDelay = Math.random() * 2 + 's';
            starsContainer.appendChild(star);
        }}
    }} else {{
        screen.style.backgroundColor = "#f5f5f5";
        status.innerText = "待機中";
    }}
</script>
"""

components.html(html_code, height=450)

# ログ履歴の表示
if st.checkbox("記録を表示"):
    if os.path.exists(DATA_PATH):
        df_display = pd.read_csv(DATA_PATH)
        st.table(df_display.tail(10))
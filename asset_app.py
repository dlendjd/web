import streamlit as st
import matplotlib.pyplot as plt
import os
import platform
import datetime
import pandas as pd

# ✅ 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 18  # 그래프 전체 폰트 크기

# ✅ 현재 연도
current_year = datetime.datetime.now().year

# ✅ 사이드바 입력
st.markdown("<h1 style='font-size: 20pt;'>입력 설정</h1>", unsafe_allow_html=True)
initial_capital = st.sidebar.number_input("초기 투자금 (억 원)", value=1.0, step=0.1)
initial_saving_million = st.sidebar.number_input("연 적립식 투자금 (만원)", value=4000, step=100)
savings_growth = st.sidebar.slider("연 적립식 투자금 증가율 (%)", 0.0, 50.0, 5.0, step=0.5) / 100
annual_return = st.sidebar.slider("연 투자 수익률 (%)", 0.0, 50.0, 10.0, step=0.5) / 100
years = st.sidebar.slider("총 투자 기간 (년)", 1, 100, 30)

# ✅ 단위 변환
initial_saving = initial_saving_million / 10000  # 만원 → 억원

# ✅ 자산 계산
assets = [initial_capital]
total = initial_capital
current_saving = initial_saving

for year in range(1, years + 1):
    total = (total + current_saving) * (1 + annual_return)
    assets.append(total)
    current_saving *= (1 + savings_growth)

# ✅ 연도 라벨
year_labels = list(range(current_year, current_year + years + 1))

# ✅ 본문 출력
st.markdown("<h1 style='font-size: 24pt;'>📈 자산 성장 시뮬레이션-v1.1</h1>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style='font-size: 20pt;'>
        초기 투자금: <b>{initial_capital:.2f}억 원</b>,<br>
        연 적립식 투자금: <b>{initial_saving_million:,}만 원</b>,<br>
        연 투자 수익률: <b>{annual_return*100:.1f}%</b>,<br>
        연 적립식 투자금 증가율: <b>{savings_growth*100:.1f}%</b>
    </div>
    """,
    unsafe_allow_html=True
)

# ✅ 5년 단위 자산 요약 표
summary_years = [current_year] + [current_year + i for i in range(5, years + 1, 5)]
summary_assets = [assets[i - current_year] for i in summary_years if (i - current_year) < len(assets)]
summary_elapsed = ['현재' if (i - current_year) == 0 else f"{i - current_year}년 후"
                   for i in summary_years[:len(summary_assets)]]

summary_df = pd.DataFrame({
    "경과": summary_elapsed,
    "연도": summary_years[:len(summary_assets)],
    "자산 (억원)": [f"{amt:,.2f}" for amt in summary_assets]
})

# ✅ 표 출력 (폰트 사이즈 18pt)
st.markdown("<h2 style='font-size: 18pt;'>📋 5년 단위 자산 요약</h2>", unsafe_allow_html=True)
st.dataframe(
    summary_df.style.set_table_styles([
        {'selector': 'th', 'props': [('font-size', '30pt')]},
        {'selector': 'td', 'props': [('font-size', '30pt')]}
    ]),
    use_container_width=True
)

# ✅ 그래프 그리기
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(year_labels, assets, marker='o', color='blue')
ax.set_title("자산 성장 그래프", fontsize=18)
ax.set_xlabel("연도", fontsize=18)
ax.set_ylabel("자산 (억원)", fontsize=18)
ax.tick_params(axis='x', labelsize=18)
ax.tick_params(axis='y', labelsize=18)
ax.grid(True)
plt.xticks(rotation=45)
st.pyplot(fig)

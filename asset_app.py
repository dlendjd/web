import streamlit as st
import matplotlib.pyplot as plt
# import matplotlib.font_manager as fm
import os
import platform
import datetime
import pandas as pd

# # ✅ NanumGothic 폰트 직접 다운로드 및 설정
# font_url = "https://github.com/park-junha/Nanum-Gothic-Font/raw/main/NanumGothic.ttf"
# font_path = "/tmp/NanumGothic.ttf"


# if not os.path.exists(font_path):
#     import urllib.request
#     urllib.request.urlretrieve(font_url, font_path)

# # ✅ matplotlib에 폰트 등록
# font_prop = fm.FontProperties(fname=font_path)
# plt.rcParams['font.family'] = font_prop.get_name()
# plt.rcParams['axes.unicode_minus'] = False

# ✅ 한글 폰트 설정
# if platform.system() == 'Windows':
#     plt.rcParams['font.family'] = 'Malgun Gothic'
# elif platform.system() == 'Darwin':
#     plt.rcParams['font.family'] = 'AppleGothic'
# else:
#     plt.rcParams['font.family'] = 'NanumGothic'
# plt.rcParams['axes.unicode_minus'] = False
# plt.rcParams['font.family'] = 'NanumGothic'
# plt.rcParams['axes.unicode_minus'] = False


# ✅ 현재 연도
current_year = datetime.datetime.now().year

# ✅ 입력 받기
st.sidebar.title("입력 설정")
initial_capital = st.sidebar.number_input("초기 투자 자본 (억 원)", value=5.0, step=0.1)
initial_saving_million = st.sidebar.number_input("연간 저축액 (만원)", value=8000, step=100)
savings_growth = st.sidebar.slider("연간 저축액 증가율 (%)", 0.0, 50.0, 5.0) / 100
annual_return = st.sidebar.slider("연 투자 수익률 (%)", 0.0, 50.0, 10.0) / 100
years = st.sidebar.slider("총 투자 기간 (년)", 1, 100, 30)

# ✅ 단위 변환
initial_saving = initial_saving_million / 10000  # 만원 → 억원

# ✅ 자산 계산 (2025년 현재 자산 포함)
assets = [initial_capital]  # 현재 자산부터 시작
total = initial_capital
current_saving = initial_saving

for year in range(1, years + 1):
    total = (total + current_saving) * (1 + annual_return)
    assets.append(total)
    current_saving *= (1 + savings_growth)

# ✅ 연도 라벨 만들기
year_labels = list(range(current_year, current_year + years + 1))  # 2025 ~ 2055 등

# ✅ 본문 출력
st.title("📈 자산 성장 시뮬레이션-v1.1")
st.write(
    f"초기 추자 자본: **{initial_capital:.2f}억 원**, "
    f"첫 해 저축: **{initial_saving_million:,}만 원**, "
    f"연 수익률: **{annual_return*100:.1f}%**, "
    f"저축 증가율: **{savings_growth*100:.1f}%**"
)

# ✅ 그래프 그리기
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(year_labels, assets, marker='o', color='blue')
ax.set_title("자산 성장 그래프")
ax.set_xlabel("연도")
ax.set_ylabel("자산 (억원)")
ax.grid(True)
plt.xticks(rotation=45)
st.pyplot(fig)

# ✅ 5년 단위 자산 요약 표 (경과 연도에 '현재' 포함)
summary_years = [current_year] + [current_year + i for i in range(5, years + 1, 5)]
summary_assets = [assets[i - current_year] for i in summary_years if (i - current_year) < len(assets)]
summary_elapsed = ['현재'] + [f"{i - current_year}년 후" for i in summary_years[1:]]

# 경과 표시: 0년 후 → 현재, 그 외는 n년 후
summary_elapsed = ['현재' if (i - current_year) == 0 else f"{i - current_year}년 후"
                   for i in summary_years[:len(summary_assets)]]

summary_df = pd.DataFrame({
    "경과": summary_elapsed,
    "연도": summary_years[:len(summary_assets)],
    "자산 (억원)": [f"{amt:,.2f}" for amt in summary_assets]
})

# ✅ 연도 왼쪽 정렬
styled_df = summary_df.style.set_properties(subset=["연도"], **{'text-align': 'left'})

st.subheader("📋 5년 단위 자산 요약")
st.dataframe(styled_df, use_container_width=True)

#streamlit run asset_app.py
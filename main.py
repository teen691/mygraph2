import pandas as pd
import plotly.express as px
import streamlit as st


# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 전처리: 세로막대 기호(|)로 분리된 장르 중 첫 번째 장르만 선택
    df["genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0])

    return df


df = load_data()

# 웹 앱 제목
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown("---")

# 1. 장르별 영화 편수 (도넛 그래프)
st.header("1. 장르별 영화 편수 분포")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["장르", "영화 수"]

fig_donut = px.pie(
    genre_counts,
    values="영화 수",
    names="장르",
    hole=0.4,
    hover_data=["영화 수"],
    labels={"영화 수": "편수", "장르": "장르"},
)
fig_donut.update_traces(textinfo="percent+label", hovertemplate="%{label}<br>편수: %{value}편<br>비율: %{percent}")

st.plotly_chart(fig_donut, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("박스오피스 상위권 영화 중 특정 장르(예: 드라마, 액션 등)의 비중이 얼마나 차지하는지 한눈에 파악할 수 있습니다.")

st.markdown("---")

# 2. 개봉일 스크린 수와 총 관객 수의 관계 (산점도 그래프)
st.header("2. 개봉일 스크린 수 vs 총 관객 수")

fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "genre": "장르",
    },
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("초기 확보한 스크린 수가 최종 총 관객 수 흥행에 미치는 양의 상관관계와 장르별 분포 양상을 확인할 수 있습니다.")

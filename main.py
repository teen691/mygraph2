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

# ---------------------------------------------------------
# 1. 장르별 영화 편수 (도넛 그래프)
# ---------------------------------------------------------
st.header("1. 장르별 영화 편수 분포")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["장르", "영화 수"]

fig_donut = px.pie(
    genre_counts,
    values="영화 수",
    names="장르",
    hole=0.4,
    labels={"영화 수": "편수", "장르": "장르"},
)
fig_donut.update_traces(
    textinfo="percent+label",
    hovertemplate="%{label}<br>편수: %{value}편<br>비율: %{percent}",
)

st.plotly_chart(fig_donut, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("박스오피스 상위권 영화 중 어떤 장르의 영화가 가장 많이 제작 및 개봉되었는지 장르별 비중을 파악할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 2. 장르 및 영화별 총 관객 수 (트리맵)
# ---------------------------------------------------------
st.header("2. 장르 및 영화별 총 관객 수 분포")

fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체 영화"), "genre", "movieNm"],
    values="total_audi",
    color="genre",
    hover_data={"total_audi": ":,d"},
    labels={"total_audi": "총 관객 수", "genre": "장르", "movieNm": "영화명"},
)

fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,}명<extra></extra>"
)

st.plotly_chart(fig_treemap, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("장르 전체의 총 관객 수 규모와 각 장르 내에서 어떤 영화가 관객 수를 가장 많이 모으며 흥행을 견인했는지 한눈에 비교할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 3. 총 관객 수 분포 (히스토그램)
# ---------------------------------------------------------
st.header("3. 총 관객 수 분포")

fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    labels={"total_audi": "총 관객 수", "count": "영화 수"},
)
fig_hist.update_traces(
    hovertemplate="관객 수 구간: %{x}<br>영화 수: %{y}편<extra></extra>"
)

st.plotly_chart(fig_hist, use_container_width=True)

# 동적 데이터 계산 (가장 관객 수가 많은 영화 추출)
max_movie_row = df.loc[df["total_audi"].idxmax()]
max_movie_name = max_movie_row["movieNm"]
max_audi_val = max_movie_row["total_audi"]

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write(
    f"대부분의 영화가 **총 관객 수 200만 명 이하의 하위 구간**에 밀집되어 있는 L자형 구조를 띠고 있으며, "
    f"가장 관객 수가 많은 영화는 **'{max_movie_name}'**(약 {max_audi_val:,}명)입니다."
)

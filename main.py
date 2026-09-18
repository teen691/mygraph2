import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------
# 데이터 불러오기 및 전처리
# ---------------------------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 결측치는 빈 문자열로 처리하여 장르가 없는 경우 안전하게 제거/처리
    df["genre"] = df["genre"].fillna("").astype(str).apply(lambda x: x.split("|")[0] if x else "기타")
    df["nation"] = df["nation"].fillna("기타").astype(str)

    return df

df = load_data()

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
    textposition="inside",  # 라벨을 조각 내부로 지정 (지시선 제거)
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

st.markdown("---")

# ---------------------------------------------------------
# 4. 개봉일 스크린 수 vs 총 관객 수 (산점도)
# ---------------------------------------------------------
st.header("4. 개봉일 스크린 수 vs 총 관객 수 관계")

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

fig_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린 수: %{x:,}개<br>총 관객 수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("개봉일에 확보한 스크린 수가 많을수록 최종 총 관객 수도 증가하는 양의 상관관계를 보이며, 장르별 스크린 확보 수준 및 흥행 선점 양상을 비교할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 5. 주요 장르별 총 관객 수 분포 (박스플롯)
# ---------------------------------------------------------
st.header("5. 주요 장르별 총 관객 수 분포 (10편 이상 장르)")

# 영화 수 10편 이상인 장르만 필터링
genres_over_10 = df["genre"].value_counts()[lambda x: x >= 10].index
df_filtered = df[df["genre"].isin(genres_over_10)]

fig_box = px.box(
    df_filtered,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",
    hover_name="movieNm",
    labels={
        "genre": "장르",
        "total_audi": "총 관객 수",
    },
)

fig_box.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객 수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig_box, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("주요 장르별 관객 수의 중앙값과 범위를 비교할 수 있으며, 상자 밖의 이상치(Outlier) 점을 통해 해당 장르 내에서 기록적인 흥행을 이뤄낸 대박 영화들을 구분해볼 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 6. 개봉일 스크린 수 vs 총 관객 수 (첫 주 관객 수 버블 그래프)
# ---------------------------------------------------------
st.header("6. 개봉일 스크린 수 vs 총 관객 수 (첫 주 관객 수 버블 그래프)")

fig_bubble = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=40,
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "first_week_audi": "첫 주 관객 수",
        "genre": "장르",
    },
)

fig_bubble.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린 수: %{x:,}개<br>총 관객 수: %{y:,}명<br>첫 주 관객 수: %{customdata[0]:,}명<extra></extra>",
    customdata=df[["first_week_audi"]],
)

st.plotly_chart(fig_bubble, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("개봉일 스크린 수와 최종 총 관객 수의 관계에 더해, **버블의 크기(첫 주 관객 수)**를 통해 개봉 초반 흥행 몰이(초반 집객력)가 최종 총 관객 수에 얼마나 큰 영향을 미쳤는지 한눈에 파악할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 7. 제작 국가 및 장르별 영화 편수 (선버스트 그래프)
# ---------------------------------------------------------
st.header("7. 제작 국가 및 장르별 영화 편수 분포")

fig_sunburst = px.sunburst(
    df,
    path=["nation", "genre"],
    labels={"nation": "제작 국가", "genre": "장르"},
)

fig_sunburst.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 수: %{value}편<extra></extra>"
)

st.plotly_chart(fig_sunburst, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("안쪽 원의 **제작 국가**에서 바깥쪽 원의 **장르**로 이어지는 계층 구조를 통해 각 국가별로 어떤 장르의 영화가 주로 제작·개봉되었는지 영화 편수 비율을 입체적으로 분석할 수 있습니다.")
# ---------------------------------------------------------
# 8. 개봉일 스크린 수 분포 (히스토그램)
# ---------------------------------------------------------
st.header("8. 개봉일 스크린 수 분포")

fig_hist_scrn = px.histogram(
    df,
    x="first_scrn",
    nbins=30,
    labels={"first_scrn": "개봉일 스크린 수", "count": "영화 수"},
)
fig_hist_scrn.update_traces(
    hovertemplate="스크린 수 구간: %{x}개<br>영화 수: %{y}편<extra></extra>"
)

st.plotly_chart(fig_hist_scrn, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("개봉일에 배정받은 스크린 수가 주로 어느 구간에 집중되어 있는지 분포 현황을 파악할 수 있습니다.")

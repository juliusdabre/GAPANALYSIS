import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_excel("GGI Jan 2025.xlsx")
st.set_page_config(page_title="NextRise - Property Investment Dashboard", layout="wide")
st.image("logo.png", width=600)
#st.title("🏡 NextRise: Property Investment Dashboard")

st.sidebar.header(" Filter Suburb Data")

area_options = df['Area'].unique()
selected_areas = st.sidebar.multiselect("Select Area(s)", area_options, default=area_options[:5])

growth_range = st.sidebar.slider("Average Annual Growth (10Y)",
    float(df['Av Annual Growth (10Y)'].min()),
    float(df['Av Annual Growth (10Y)'].max()),
    (float(df['Av Annual Growth (10Y)'].min()), float(df['Av Annual Growth (10Y)'].max()))
)

pop_growth_range = st.sidebar.slider("Population Growth PA",
    float(df['Population Growth PA'].min()),
    float(df['Population Growth PA'].max()),
    (float(df['Population Growth PA'].min()), float(df['Population Growth PA'].max()))
)

growth_6y_range = st.sidebar.slider("6Y Growth Rate from 2014",
    float(df['6Y Growth Rate from 2014'].min()),
    float(df['6Y Growth Rate from 2014'].max()),
    (float(df['6Y Growth Rate from 2014'].min()), float(df['6Y Growth Rate from 2014'].max()))
)

cmgr_range = st.sidebar.slider("CMGR 2014 to 2020",
    float(df['CMGR 2014 to 2020'].min()),
    float(df['CMGR 2014 to 2020'].max()),
    (float(df['CMGR 2014 to 2020'].min()), float(df['CMGR 2014 to 2020'].max()))
)

projected_cmgr_range = st.sidebar.slider("Projected CMGR Today",
    float(df['Projected CMGR Today'].min()),
    float(df['Projected CMGR Today'].max()),
    (float(df['Projected CMGR Today'].min()), float(df['Projected CMGR Today'].max()))
)

growth_gap_dollar_range = st.sidebar.slider("Growth gap ($)",
    float(df['Growth gap ($)'].min()),
    float(df['Growth gap ($)'].max()),
    (float(df['Growth gap ($)'].min()), float(df['Growth gap ($)'].max()))
)

growth_gap_pct_range = st.sidebar.slider("Growth gap (%)",
    float(df['Growth gap (%)'].min()),
    float(df['Growth gap (%)'].max()),
    (float(df['Growth gap (%)'].min()), float(df['Growth gap (%)'].max()))
)

rank_range = st.sidebar.slider("Rank",
    int(df['Rank'].min()),
    int(df['Rank'].max()),
    (int(df['Rank'].min()), int(df['Rank'].max()))
)

filtered_df = df[
    (df['Area'].isin(selected_areas)) &
    (df['Av Annual Growth (10Y)'].between(*growth_range)) &
    (df['Population Growth PA'].between(*pop_growth_range)) &
    (df['6Y Growth Rate from 2014'].between(*growth_6y_range)) &
    (df['CMGR 2014 to 2020'].between(*cmgr_range)) &
    (df['Projected CMGR Today'].between(*projected_cmgr_range)) &
    (df['Growth gap ($)'].between(*growth_gap_dollar_range)) &
    (df['Growth gap (%)'].between(*growth_gap_pct_range)) &
    (df['Rank'].between(*rank_range))
]

st.subheader("📊 Filtered Suburb Data")
st.dataframe(filtered_df, use_container_width=True)

st.subheader("📉 Growth Gap by Area")
fig = px.bar(filtered_df, x='Area', y='Growth gap ($)', color='Av Annual Growth (10Y)')
st.plotly_chart(fig, use_container_width=True)

st.subheader("🕸️ Radar Chart of Key Metrics")
radar_metrics = ['Av Annual Growth (10Y)', 'Population Growth PA', '6Y Growth Rate from 2014', 'CMGR 2014 to 2020']
radar_fig = go.Figure()
for _, row in filtered_df.iterrows():
    radar_fig.add_trace(go.Scatterpolar(
        r=[row[metric] for metric in radar_metrics],
        theta=radar_metrics,
        fill='toself',
        name=row['Area']
    ))
radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
st.plotly_chart(radar_fig, use_container_width=True)

st.subheader("🧠 AI Investment Summary")
for _, row in filtered_df.iterrows():
    st.markdown(f'''
### 📍 {row['Area']}
- 📈 **10Y Avg Annual Growth:** {row['Av Annual Growth (10Y)']:.2%}
- 👥 **Population Growth PA:** {row['Population Growth PA']:.2%}
- 📊 **6Y Growth from 2014:** {row['6Y Growth Rate from 2014']:.2%}
- 📉 **CMGR 2014–2020:** {row['CMGR 2014 to 2020']:.4f}
- 🔮 **Projected CMGR Today:** {row['Projected CMGR Today']:.0f}
- 💵   Growth Gap $:  {row['Growth gap ($)']:.0f}
- 📉 **Growth Gap (%):** {row['Growth gap (%)']:.2%}
- 🏅 **Rank:** {row['Rank']}

This suburb shows strong fundamentals with a {row['Av Annual Growth (10Y)']:.2%} annual price increase over a decade,
coupled with population growth of {row['Population Growth PA']:.2%} per annum.
The growth gap of ${row['Growth gap ($)']:.0f} indicates an investment opportunity due to undervaluation.
Its historical performance and projected growth make **{row['Area']}** a strong candidate for strategic investment.
''')

st.download_button("📥 Download Filtered Data", data=filtered_df.to_csv(index=False), file_name="filtered_ggi_data.csv")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set page config
st.set_page_config(page_title="Tips Dashboard", layout="wide")

# Load data with error handling
try:
    tips_df = pd.read_csv("tips.csv")
except FileNotFoundError:
    st.error("File not found. Please upload the correct file.")
    st.stop()
except pd.errors.EmptyDataError:
    st.error("File is empty. Please upload a valid CSV file.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred: {e}")
    st.stop()

# Sidebar
st.sidebar.header("Tips Dashboard")
st.sidebar.image("tips.jpg")
st.sidebar.write("This dashboard uses the Tips dataset from Seaborn for educational purposes.")

# Sidebar color picker
primary_color = st.sidebar.color_picker("Pick a Primary Color", "#4CAF50")
secondary_color = st.sidebar.color_picker("Pick a Secondary Color", "#f0f2f6")

# Custom CSS for styling
st.markdown(f"""
    <style>
    .sidebar .sidebar-content {{
        background-color: {secondary_color};
    }}
    .stButton>button {{
        color: white;
        background-color: {primary_color};
    }}
    .stMetric {{
        background-color: {secondary_color};
        padding: 10px;
        border-radius: 10px;
    }}
    .stPlotlyChart {{
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 10px;
        transition: transform 0.2s;
    }}
    .stPlotlyChart:hover {{
        transform: scale(1.05);
    }}
    .stTitle {{
        font-size: 2.5em;
        font-weight: bold;
        color: {primary_color};
        padding: 10px;
        border-bottom: 2px solid {primary_color};
    }}
    </style>
    """, unsafe_allow_html=True)

cat_filter = st.sidebar.selectbox("Categorical Filtering", [None, 'sex', 'smoker', 'day', 'time'])
num_filter = st.sidebar.selectbox("Numerical Filtering", [None, 'total_bill', 'tip'])
row_filter = st.sidebar.selectbox("Row Filtering", [None, 'sex', 'smoker', 'day', 'time'])
col_filter = st.sidebar.selectbox("Column Filtering", [None, 'sex', 'smoker', 'day', 'time'])

st.sidebar.write("")
st.sidebar.markdown("made with :heart_eyes: by Eng. Alaa Elsaid")

# Dashboard body
st.markdown("<h1 class='stTitle'> Tips Dashboard</h1>", unsafe_allow_html=True)

# Max & Min metrics
a1, a2, a3, a4 = st.columns(4)
a1.metric("Max. Total Bill", tips_df['total_bill'].max())
a2.metric("Max. Tip", tips_df['tip'].max())
a3.metric("Min. Total Bill", tips_df['total_bill'].min())
a4.metric("Min. Tip", tips_df['tip'].min())

# Scatter plot
st.subheader("Total Bills Vs. Tips")
if cat_filter:
    fig = px.scatter(tips_df, x='total_bill', y='tip', color=cat_filter, size=num_filter, facet_col=col_filter, facet_row=row_filter)
else:
    fig = px.scatter(tips_df, x='total_bill', y='tip')
st.plotly_chart(fig, use_container_width=True, className="stPlotlyChart")

# Bar and Pie charts
c1, c2, c3 = st.columns((4, 3, 3))
with c1:
    st.text("Sex Vs. Total Bills")
    fig = px.bar(tips_df, x='sex', y='total_bill', color=cat_filter)
    st.plotly_chart(fig, use_container_width=True, className="stPlotlyChart")
with c2:
    st.text("Smoker / Non-Smoker Vs. Tips")
    fig = px.pie(tips_df, names='smoker', values='tip', color=cat_filter)
    st.plotly_chart(fig, use_container_width=True, className="stPlotlyChart")
with c3:
    st.text("Days Vs. Tips")
    fig = px.pie(tips_df, names='day', values='tip', color=cat_filter, hole=0.4)
    st.plotly_chart(fig, use_container_width=True, className="stPlotlyChart")

# Heatmap
st.subheader("Correlation Heatmap")
numeric_cols = tips_df.select_dtypes(include=['float64', 'int64']).columns
corr = tips_df[numeric_cols].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Box plot
st.subheader("Box Plot of Tips by Day")
fig = px.box(tips_df, x='day', y='tip', color='day')
st.plotly_chart(fig, use_container_width=True, className="stPlotlyChart")

# Summary statistics
st.subheader("Summary Statistics")
st.write(tips_df.describe())

# Feedback section
st.sidebar.subheader("Feedback")
feedback = st.sidebar.text_area("Your feedback", "")
if st.sidebar.button("Submit"):
    st.sidebar.write("Thank you for your feedback!")

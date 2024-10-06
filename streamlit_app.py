import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
@st.cache_data
def load_data():
    github_df = pd.read_csv('github_dataset.csv')
    return github_df

df = load_data()

# Title
st.title('GitHub Repositories Dashboard')

# Display raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)

# Top repositories by stars
st.subheader('Top 10 Repositories by Stars')
top_repos = df.sort_values('stars_count', ascending=False).head(10)
fig = px.bar(top_repos, x='repositories', y='stars_count', title='Top 10 Repositories by Stars')
st.plotly_chart(fig)

# Language distribution
st.subheader('Primary Language Distribution')
lang_counts = df['language'].value_counts()
fig = px.pie(values=lang_counts.values, names=lang_counts.index, title='Primary Language Distribution')
st.plotly_chart(fig)

# Scatter plot: Stars vs Forks
st.subheader('Stars vs Forks')
fig = px.scatter(df, x='stars_count', y='forks_count', hover_name='repositories',
                 title='Stars vs Forks', log_x=True, log_y=True)
st.plotly_chart(fig)

# Histogram of pull requests
st.subheader('Distribution of Pull Requests')
fig = px.histogram(df, x='pull_requests', title='Distribution of Pull Requests')
st.plotly_chart(fig)

# Top repositories by issues count
st.subheader('Top 10 Repositories by Issues Count')
top_issues = df.sort_values('issues_count', ascending=False).head(10)
fig = px.bar(top_issues, x='repositories', y='issues_count', title='Top 10 Repositories by Issues Count')
st.plotly_chart(fig)

# Distribution of contributors
st.subheader('Distribution of Contributors')
fig = px.histogram(df, x='contributors', title='Distribution of Contributors', log_x=True)
st.plotly_chart(fig)

# Correlation heatmap
st.subheader('Correlation Heatmap')
numeric_cols = ['stars_count', 'forks_count', 'issues_count', 'pull_requests', 'contributors']
corr = df[numeric_cols].corr()
fig = px.imshow(corr, title='Correlation Heatmap')
st.plotly_chart(fig)

# Top languages used
st.subheader('Top 10 Most Used Languages')
language_counts = df['language'].value_counts().head(10)
fig = px.bar(x=language_counts.index, y=language_counts.values, title='Top 10 Most Used Languages')
fig.update_xaxes(title='Language')
fig.update_yaxes(title='Count')
st.plotly_chart(fig)

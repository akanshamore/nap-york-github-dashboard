import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


# Load the data
@st.cache_data
def load_data():
    github_df = pd.read_csv('github_dataset.csv')
    repo_df = pd.read_csv('repository_data.csv')

    # Merge the datasets
    merged_df = pd.merge(github_df, repo_df, left_on='repositories', right_on='name', how='outer')

    # Convert created_at to datetime
    merged_df['created_at'] = pd.to_datetime(merged_df['created_at'])

    return merged_df


df = load_data()

# Title
st.title('GitHub Repositories Dashboard')

# Display raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)

# Top repositories by stars
st.subheader('Top 10 Repositories by Stars')
top_repos = df.sort_values('stars_count_x', ascending=False).head(10)
fig = px.bar(top_repos, x='repositories', y='stars_count_x', title='Top 10 Repositories by Stars')
st.plotly_chart(fig)

# Language distribution
st.subheader('Primary Language Distribution')
lang_counts = df['primary_language'].value_counts()
fig = px.pie(values=lang_counts.values, names=lang_counts.index, title='Primary Language Distribution')
st.plotly_chart(fig)

# Scatter plot: Stars vs Forks
st.subheader('Stars vs Forks')
fig = px.scatter(df, x='stars_count_x', y='forks_count_x', hover_name='repositories',
                 title='Stars vs Forks', log_x=True, log_y=True)
st.plotly_chart(fig)

# Histogram of pull requests
st.subheader('Distribution of Pull Requests')
fig = px.histogram(df, x='pull_requests_y', title='Distribution of Pull Requests')
st.plotly_chart(fig)

# Top repositories by commit count
st.subheader('Top 10 Repositories by Commit Count')
top_commits = df.sort_values('commit_count', ascending=False).head(10)
fig = px.bar(top_commits, x='repositories', y='commit_count', title='Top 10 Repositories by Commit Count')
st.plotly_chart(fig)

# Repository creation over time
st.subheader('Repository Creation Over Time')
df['created_year'] = df['created_at'].dt.year
year_counts = df['created_year'].value_counts().sort_index()
fig = px.line(x=year_counts.index, y=year_counts.values, title='Repository Creation by Year')
fig.update_xaxes(title='Year')
fig.update_yaxes(title='Number of Repositories')
st.plotly_chart(fig)

# Top languages used
st.subheader('Top 10 Most Used Languages')
all_languages = df['languages_used'].str.split(',', expand=True).stack()
language_counts = all_languages.value_counts().head(10)
fig = px.bar(x=language_counts.index, y=language_counts.values, title='Top 10 Most Used Languages')
fig.update_xaxes(title='Language')
fig.update_yaxes(title='Count')
st.plotly_chart(fig)

# Correlation heatmap
st.subheader('Correlation Heatmap')
numeric_cols = ['stars_count_x', 'forks_count_x', 'issues_count', 'pull_requests_x', 'contributors', 'watchers',
                'commit_count']
corr = df[numeric_cols].corr()
fig = px.imshow(corr, title='Correlation Heatmap')
st.plotly_chart(fig)

# Watchers vs Stars
st.subheader('Watchers vs Stars')
fig = px.scatter(df, x='watchers', y='stars_count_x', hover_name='repositories',
                 title='Watchers vs Stars', log_x=True, log_y=True)
st.plotly_chart(fig)

# Top 10 repositories by issues count
st.subheader('Top 10 Repositories by Issues Count')
top_issues = df.sort_values('issues_count', ascending=False).head(10)
fig = px.bar(top_issues, x='repositories', y='issues_count', title='Top 10 Repositories by Issues Count')
st.plotly_chart(fig)

# Distribution of contributors
st.subheader('Distribution of Contributors')
fig = px.histogram(df, x='contributors', title='Distribution of Contributors', log_x=True)
st.plotly_chart(fig)
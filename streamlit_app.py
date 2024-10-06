import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Load the data
@st.cache_data
def load_data():
    github_df = pd.read_csv('github_dataset.csv')
    return github_df

df = load_data()

st.title('GitHub Repositories Dashboard')

# Display raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)

# General Insights Section
st.header('General Insights')

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

# Distribution of Contributors
st.subheader('Distribution of Contributors')
df['contributors_numeric'] = pd.to_numeric(df['contributors'], errors='coerce')
fig = px.histogram(df, x='contributors_numeric', title='Distribution of Contributors', log_x=True)
fig.update_xaxes(title='Number of Contributors')
fig.update_yaxes(title='Count')
st.plotly_chart(fig)

# Correlation heatmap
st.subheader('Correlation Heatmap')
numeric_cols = ['stars_count', 'forks_count', 'issues_count', 'pull_requests', 'contributors_numeric']
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

# Popularity vs. Engagement Analysis Section
st.header('Popularity vs. Engagement Analysis')

st.write("""
This analysis explores the relationship between a repository's popularity (measured by stars) 
and its community engagement (forks) and potential challenges (issues).
""")

# Create log-transformed columns for stars, forks, and issues
df['log_stars'] = np.log1p(df['stars_count'])
df['log_forks'] = np.log1p(df['forks_count'])
df['log_issues'] = np.log1p(df['issues_count'])

# Scatter plot: Stars vs Forks (log scale)
st.subheader('Relationship between Stars and Forks')
fig = px.scatter(df, x='log_stars', y='log_forks', 
                 hover_name='repositories', 
                 hover_data=['stars_count', 'forks_count'],
                 labels={'log_stars': 'Log(Stars + 1)', 'log_forks': 'Log(Forks + 1)'},
                 title='Stars vs Forks (Log Scale)')

# Add trendline
fig.add_trace(go.Scatter(x=df['log_stars'], y=np.poly1d(np.polyfit(df['log_stars'], df['log_forks'], 1))(df['log_stars']),
                         mode='lines', name='Trendline'))

st.plotly_chart(fig)

st.write("""
We observe a strong positive correlation between stars and forks. 
As repositories become more popular (more stars), they tend to be forked more often, 
indicating increased community engagement and potential for collaborative development.
""")

# Scatter plot: Stars vs Issues (log scale)
st.subheader('Relationship between Stars and Issues')
fig = px.scatter(df, x='log_stars', y='log_issues', 
                 hover_name='repositories', 
                 hover_data=['stars_count', 'issues_count'],
                 labels={'log_stars': 'Log(Stars + 1)', 'log_issues': 'Log(Issues + 1)'},
                 title='Stars vs Issues (Log Scale)')

# Add trendline
fig.add_trace(go.Scatter(x=df['log_stars'], y=np.poly1d(np.polyfit(df['log_stars'], df['log_issues'], 1))(df['log_stars']),
                         mode='lines', name='Trendline'))

st.plotly_chart(fig)

st.write("""
Interestingly, we also see a positive correlation between stars and issues. 
More popular projects tend to have more open issues. This could be due to:
1. Increased usage leading to more bug discoveries
2. More feature requests from a larger user base
3. Potentially more complex codebases in popular projects
""")

# Calculate the ratio of issues to stars, handling division by zero
df['issues_per_star'] = df.apply(lambda row: row['issues_count'] / row['stars_count'] if row['stars_count'] > 0 else 0, axis=1)

# Top 10 repositories with highest issues per star ratio
st.subheader('Top 10 Repositories with Highest Issues per Star Ratio')

# Filter out repositories with zero stars and sort
top_issues_per_star = df[df['stars_count'] > 0].sort_values('issues_per_star', ascending=False).head(10)

if not top_issues_per_star.empty:
    fig = px.bar(top_issues_per_star, x='repositories', y='issues_per_star', 
                 hover_data=['stars_count', 'issues_count'],
                 title='Top 10 Repositories: Issues per Star')
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)

    st.write("""
    This chart highlights repositories that have a high number of issues relative to their star count. 
    These projects might be facing challenges in managing their issue backlog or could be 
    in active development phases with many ongoing discussions and feature requests.
    """)
else:
    st.write("No repositories found with both stars and issues.")

# Display the data for these repositories
st.subheader('Data for Top 10 Repositories with Highest Issues per Star Ratio')
st.write(top_issues_per_star[['repositories', 'stars_count', 'issues_count', 'issues_per_star']])


# Conclusion
st.subheader('Key Insights')
st.write("""
1. Popular repositories (those with many stars) tend to have more forks, indicating higher community engagement.
2. However, popular repositories also tend to have more open issues, which could indicate active development, 
   a large user base reporting bugs, or challenges in issue management.
3. Some repositories have a high ratio of issues to stars, which might indicate projects that need additional 
   maintainer support or are in particularly active phases of development and discussion.
4. The primary language distribution shows the prevalence of certain programming languages in popular GitHub projects.
5. The distribution of pull requests and contributors gives insight into the level of community participation across projects.

These insights can help both project maintainers and contributors understand the dynamics of open-source 
projects and the challenges they may face as they grow.
""")

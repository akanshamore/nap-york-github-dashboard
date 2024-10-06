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

st.title('GitHub Repository Insights: Stars, Forks, and Issues')

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

# Calculate the ratio of issues to stars
df['issues_per_star'] = df['issues_count'] / df['stars_count']

# Top 10 repositories with highest issues per star ratio
st.subheader('Top 10 Repositories with Highest Issues per Star Ratio')
top_issues_per_star = df.sort_values('issues_per_star', ascending=False).head(10)
fig = px.bar(top_issues_per_star, x='repositories', y='issues_per_star', 
             hover_data=['stars_count', 'issues_count'],
             title='Top 10 Repositories: Issues per Star')
st.plotly_chart(fig)

st.write("""
This chart highlights repositories that have a high number of issues relative to their star count. 
These projects might be facing challenges in managing their issue backlog or could be 
in active development phases with many ongoing discussions and feature requests.
""")

# Conclusion
st.subheader('Key Insights')
st.write("""
1. Popular repositories (those with many stars) tend to have more forks, indicating higher community engagement.
2. However, popular repositories also tend to have more open issues, which could indicate active development, 
   a large user base reporting bugs, or challenges in issue management.
3. Some repositories have a high ratio of issues to stars, which might indicate projects that need additional 
   maintainer support or are in particularly active phases of development and discussion.

These insights can help both project maintainers and contributors understand the dynamics of popular open-source 
projects and the challenges they may face as they grow.
""")

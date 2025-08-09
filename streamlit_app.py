import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🏏 IPL Data Visualization Dashboard")
st.write("Interactive analysis of IPL cricket data (2008-2017)")

try:
    # Load data
    matches = pd.read_csv('matches.csv')
    deliveries = pd.read_csv('deliveries.csv')
    
    # Overview metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Matches", len(matches))
    with col2:
        st.metric("Total Deliveries", len(deliveries))
    with col3:
        st.metric("Teams", matches['team1'].nunique())
    
    # Team wins visualization
    st.subheader("🏆 Top Winning Teams")
    win_counts = matches['winner'].value_counts().head(10)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(win_counts.index, win_counts.values)
    ax.set_title('Top 10 Winning Teams')
    ax.set_xlabel('Team')
    ax.set_ylabel('Number of Wins')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    
    # Show raw data
    if st.checkbox("Show Raw Data"):
        st.subheader("Matches Dataset")
        st.dataframe(matches.head())
        
        st.subheader("Deliveries Dataset")
        st.dataframe(deliveries.head())
    
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.write("Please make sure the CSV files are in the same directory as this app.")

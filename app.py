import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Page configuration
st.set_page_config(
    page_title="IPL Data Visualization Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f4e79;
    text-align: center;
    margin-bottom: 2rem;
}
.section-header {
    font-size: 1.5rem;
    color: #2c5aa0;
    margin-top: 2rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">🏏 IPL Data Visualization Dashboard (2008-2017)</h1>', unsafe_allow_html=True)

st.markdown("""
This interactive dashboard provides comprehensive analysis of Indian Premier League cricket data spanning from 2008 to 2017.
Explore team performances, player statistics, and match insights through dynamic visualizations.
""")

# Load data with caching for better performance
@st.cache_data
def load_data():
    try:
        # Load the datasets
        matches = pd.read_csv('matches.csv')
        deliveries = pd.read_csv('deliveries.csv')
        player_stats = pd.read_csv('most_runs_average_strikerate.csv')
        
        return matches, deliveries, player_stats
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}")
        st.stop()

# Load data
matches, deliveries, player_stats = load_data()

# Sidebar for navigation
st.sidebar.title("🏏 Navigation")
analysis_type = st.sidebar.selectbox(
    "Choose Analysis Type",
    ["Overview", "Team Performance", "Player Statistics", "Seasonal Trends", "Match Analysis"]
)

# Overview section
if analysis_type == "Overview":
    st.markdown('<h2 class="section-header">📊 Dataset Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Matches", len(matches))
    with col2:
        st.metric("Total Deliveries", len(deliveries))
    with col3:
        st.metric("Teams", matches['team1'].nunique())
    
    # Dataset info
    with st.expander("📁 Dataset Information"):
        st.write("**Matches Dataset:**")
        st.write(f"- Shape: {matches.shape}")
        st.write(f"- Columns: {', '.join(matches.columns)}")
        
        st.write("**Deliveries Dataset:**")
        st.write(f"- Shape: {deliveries.shape}")
        st.write(f"- Date Range: 2008-2017")

# Team Performance section
elif analysis_type == "Team Performance":
    st.markdown('<h2 class="section-header">🏆 Team Performance Analysis</h2>', unsafe_allow_html=True)
    
    # Team wins analysis
    st.subheader("Top Winning Teams")
    
    # Calculate wins
    win_counts = matches['winner'].value_counts().head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.Set3(np.linspace(0, 1, len(win_counts)))
    bars = ax.bar(win_counts.index, win_counts.values, color=colors)
    
    ax.set_title('Top 10 Winning Teams', fontsize=16, fontweight='bold')
    ax.set_xlabel('Team', fontsize=12)
    ax.set_ylabel('Number of Wins', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{int(height)}', ha='center', va='bottom')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Team performance metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Top 5 Teams by Wins:**")
        for i, (team, wins) in enumerate(win_counts.head().items(), 1):
            st.write(f"{i}. {team}: {wins} wins")
    
    with col2:
        # Toss decision analysis
        toss_decision = matches['toss_decision'].value_counts()
        st.write("**Toss Decision Preference:**")
        for decision, count in toss_decision.items():
            percentage = (count / len(matches)) * 100
            st.write(f"{decision.title()}: {count} ({percentage:.1f}%)")

# Player Statistics section
elif analysis_type == "Player Statistics":
    st.markdown('<h2 class="section-header">👤 Player Statistics</h2>', unsafe_allow_html=True)
    
    if not player_stats.empty:
        st.subheader("Top Performers")
        
        # Display player statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Top Run Scorers:**")
            if 'batsman' in player_stats.columns and 'total_runs' in player_stats.columns:
                top_scorers = player_stats.nlargest(10, 'total_runs')[['batsman', 'total_runs']]
                st.dataframe(top_scorers, hide_index=True)
        
        with col2:
            st.write("**Best Strike Rates:**")
            if 'strikerate' in player_stats.columns:
                best_sr = player_stats.nlargest(10, 'strikerate')[['batsman', 'strikerate']]
                st.dataframe(best_sr, hide_index=True)

# Seasonal Trends section
elif analysis_type == "Seasonal Trends":
    st.markdown('<h2 class="section-header">📈 Seasonal Trends</h2>', unsafe_allow_html=True)
    
    # Convert date column to datetime if it exists
    if 'date' in matches.columns:
        # Create a copy to avoid modifying the cached data
        matches_copy = matches.copy()
        
        try:
            # Handle DD-MM-YYYY format
            matches_copy['date'] = pd.to_datetime(matches_copy['date'], format='%d-%m-%Y', errors='coerce')
            matches_copy['year'] = matches_copy['date'].dt.year
        except Exception as e:
            try:
                # Fallback to automatic parsing with error handling
                matches_copy['date'] = pd.to_datetime(matches_copy['date'], dayfirst=True, errors='coerce')
                matches_copy['year'] = matches_copy['date'].dt.year
            except Exception as e2:
                st.error(f"Error parsing dates: {e2}")
                st.write("Sample date values:", matches_copy['date'].head().tolist())
                st.stop()
        
        # Matches per season
        seasonal_matches = matches_copy.groupby('year').size()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(seasonal_matches.index, seasonal_matches.values, marker='o', linewidth=2, markersize=8)
        ax.set_title('Matches Played Per Season', fontsize=16, fontweight='bold')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Number of Matches', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Season statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Peak Season", seasonal_matches.idxmax(), f"{seasonal_matches.max()} matches")
        with col2:
            st.metric("Lowest Season", seasonal_matches.idxmin(), f"{seasonal_matches.min()} matches")
        with col3:
            st.metric("Average per Season", "", f"{seasonal_matches.mean():.1f} matches")

# Match Analysis section
elif analysis_type == "Match Analysis":
    st.markdown('<h2 class="section-header">⚡ Match Analysis</h2>', unsafe_allow_html=True)
    
    # Venue analysis
    if 'venue' in matches.columns:
        st.subheader("Top Venues")
        venue_counts = matches['venue'].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.barh(venue_counts.index, venue_counts.values)
        ax.set_title('Top 10 Venues by Number of Matches', fontsize=16, fontweight='bold')
        ax.set_xlabel('Number of Matches', fontsize=12)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    # Match results
    col1, col2 = st.columns(2)
    
    with col1:
        if 'result' in matches.columns:
            result_counts = matches['result'].value_counts()
            st.subheader("Match Results Distribution")
            for result, count in result_counts.items():
                percentage = (count / len(matches)) * 100
                st.write(f"{result}: {count} ({percentage:.1f}%)")
    
    with col2:
        if 'win_by_runs' in matches.columns and 'win_by_wickets' in matches.columns:
            st.subheader("Win Margins")
            runs_wins = matches[matches['win_by_runs'] > 0]['win_by_runs']
            wicket_wins = matches[matches['win_by_wickets'] > 0]['win_by_wickets']
            
            if not runs_wins.empty:
                st.write(f"Average win by runs: {runs_wins.mean():.1f}")
                st.write(f"Highest win by runs: {runs_wins.max()}")
            
            if not wicket_wins.empty:
                st.write(f"Average win by wickets: {wicket_wins.mean():.1f}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
📊 IPL Data Visualization Dashboard | Data Period: 2008-2017 | 
Built with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)

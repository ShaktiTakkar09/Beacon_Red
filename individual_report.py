import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

# Print the version of Seaborn
print("Seaborn Version:", sns.__version__)

# Define the download_figure function
def download_figure(figure, filename):
    buffer = BytesIO()
    figure.savefig(buffer, format="png")
    buffer.seek(0)
    st.download_button(label="Download", data=buffer, file_name=filename, mime="image/png")

# Load the data
dashboard_df = pd.read_excel('./Dashboard_Data.xlsx')


# Convert 'Date' column to date data type
dashboard_df['Date'] = pd.to_datetime(dashboard_df['Date']).dt.date

# Set Seaborn style
sns.set(style="whitegrid")
sns.set(font_scale=0.8)

# Streamlit app
st.set_page_config(
    page_title="Individual Report",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title
st.markdown("<h1 style='font-size: 24px;'>Individual Report</h1>", unsafe_allow_html=True)

# Dropdown to select candidate
candidate_ids = dashboard_df['ID'].unique()
selected_candidate = st.selectbox("Select Candidate", candidate_ids)

# Filter data for the selected candidate
candidate_data = dashboard_df[dashboard_df['ID'] == selected_candidate]

if not candidate_data.empty:
    candidate_data = candidate_data.iloc[0]

    # Section 1: Candidate Overview
    st.markdown("<h2 style='font-size: 20px;'>1. Candidate Overview</h2>", unsafe_allow_html=True)
    st.write(f"**ID:** {candidate_data['ID']}")
    st.write(f"**Gender:** {candidate_data['Gender']}")
    st.write(f"**Age:** {candidate_data['Age']}")
    st.write(f"**Position:** {candidate_data['Position']}")

# Section 2: Cognitive Ability
st.markdown("<h2 style='font-size: 20px;'>2. Cognitive Ability</h2>", unsafe_allow_html=True)


# Define the cognitive columns
cognitive_columns = ['Attention to Detail', 'Logical Reasoning', 'Numerical Reasoning', 'Verbal Reasoning']

candidate_data = dashboard_df[dashboard_df['ID'] == selected_candidate]

if not candidate_data.empty:
    # Extract the cognitive scores for the selected candidate
    selected_cognitive_scores = candidate_data[cognitive_columns]

    # Create a DataFrame for visualization
    cognitive_df = pd.DataFrame({'Cognitive Ability': cognitive_columns, 'Score': selected_cognitive_scores.values[0]})

    # Set up the plot
    plt.figure(figsize=(12, 4))
    sns.set_palette("pastel")

    # Create a bar plot for cognitive abilities
    sns.barplot(data=cognitive_df, x='Cognitive Ability', y='Score')
    plt.xlabel("Cognitive Ability")
    plt.ylabel("Score")
    plt.title("Cognitive Ability Breakdown")
    plt.xticks(rotation=45)

    # Display the plot using Streamlit
    st.pyplot(plt.gcf())

# Section 3: Performance benchmarking
st.markdown("<h2 style='font-size: 20px;'>2. Performance Benchmarking</h2>", unsafe_allow_html=True)


if not candidate_data.empty:
    # Extract the overall score for the selected candidate
    selected_overall_score = candidate_data['Overall'].mean()

    # Calculate the average overall score for all candidates
    average_overall_score = dashboard_df['Overall'].mean()

    # Set up the plot
    plt.figure(figsize=(12, 4))
    sns.set_palette("pastel")

    # Create a bar plot for benchmarking
    ax = sns.barplot(data=pd.DataFrame({'Performance': ['Selected Candidate', 'Average Candidate'],
                                        'Score': [selected_overall_score, average_overall_score]}),
                     x='Performance', y='Score')
    plt.xlabel("Performance")
    plt.ylabel("Score")
    plt.title("Performance Benchmarking")
    plt.ylim(0, 100)  # Assuming the score is on a percentage scale
    plt.xticks(rotation=45)

    # Display average scores above the bars
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    # Display the plot using Streamlit
    st.pyplot(plt.gcf())
# Section 4: Personality Traits
st.markdown("<h2 style='font-size: 20px;'>4. Personality Traits</h2>", unsafe_allow_html=True)

# Filter data for the selected candidate
candidate_personality_data = dashboard_df[dashboard_df['ID'] == selected_candidate]

if not candidate_personality_data.empty:
    # Extract personality trait scores for the selected candidate
    personality_columns = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
    selected_personality_scores = candidate_personality_data[personality_columns]

    # Create a DataFrame for visualization
    personality_df = pd.DataFrame({'Personality Trait': personality_columns, 'Score': selected_personality_scores.values[0]})

    # Set up the plot
    plt.figure(figsize=(12, 4))
    sns.set_palette("pastel")

    # Create a bar plot for personality traits
    sns.barplot(data=personality_df, x='Personality Trait', y='Score')
    plt.xlabel("Personality Trait")
    plt.ylabel("Score")
    plt.title("Personality Traits Analysis")
    plt.ylim(0, 100)  # Assuming the score is on a percentage scale
    plt.xticks(rotation=45)

    # Display the plot using Streamlit
    st.pyplot(plt.gcf())
else:
    st.write("No data available for the selected candidate.")

# Section 5: IQ Score Analysis
st.markdown("<h2 style='font-size: 20px;'>5. IQ Score Analysis</h2>", unsafe_allow_html=True)

# Filter input for position
selected_position_iq = st.selectbox("Select Position for IQ Score Analysis", dashboard_df['Position'].unique(), key="iq_position")

# Filter data for the selected candidate and position
filtered_candidate_data_iq = dashboard_df[(dashboard_df['ID'] == selected_candidate) & (dashboard_df['Position'] == selected_position_iq)]

# Display IQ score analysis for the selected candidate and position
if not filtered_candidate_data_iq.empty:
    candidate_iq_score = filtered_candidate_data_iq['IQ'].iloc[0]  # Access the scalar value
    average_iq_score = filtered_candidate_data_iq['IQ'].mean()

    st.write(f"**Candidate's IQ Score:** {candidate_iq_score}")
    st.write(f"**Average IQ Score for Position '{selected_position_iq}':** {average_iq_score}")

# Section 6: Recommendation Status
st.markdown("<h2 style='font-size: 20px;'>6. Recommendation Status</h2>", unsafe_allow_html=True)

# Filter input for position and threshold
selected_position_recommendation = st.selectbox("Select Position for Recommendation", dashboard_df['Position'].unique(), key="recommendation_position")
threshold = st.slider("Set Threshold for Recommendation", min_value=0, max_value=100, value=80, key="recommendation_threshold")

# Filter data for the selected candidate and position
filtered_candidate_data_recommendation = dashboard_df[(dashboard_df['ID'] == selected_candidate) & (dashboard_df['Position'] == selected_position_recommendation)]

# Display recommendation status for the selected candidate and position
if not filtered_candidate_data_recommendation.empty:
    candidate_overall_score = filtered_candidate_data_recommendation['Overall'].iloc[0]  # Access the scalar value

    if candidate_overall_score >= threshold:
        recommendation_status = "Recommended"
    else:
        recommendation_status = "Not Recommended"

    st.write(f"Based on the threshold of {threshold}, the candidate for position '{selected_position_recommendation}' is **{recommendation_status}**.")


import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

# Define the download_figure function
def download_figure(figure, filename):
    buffer = BytesIO()
    figure.savefig(buffer, format="png")
    buffer.seek(0)
    st.download_button(label="Download", data=buffer, file_name=filename, mime="image/png")

# Load the data
dashboard_df = pd.read_excel('./Dashboard_Data.xlsx')



# Set Seaborn style
sns.set(style="whitegrid")

# Streamlit app
st.set_page_config(
    page_title="Individual Report",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

primaryColor = '#FF8C02' # Bright Orange

backgroundColor = '#00325B' # Dark Blue

secondaryBackgroundColor = '#55B2FF' # Lighter Blue

st.title("Individual Report")
# Sidebar filters
st.sidebar.header("Filters")

# Dropdown to select candidate
candidate_ids = dashboard_df['ID'].unique()
selected_candidate = st.sidebar.selectbox("Select Candidate", candidate_ids)

# Filter data for the selected candidate
candidate_data = dashboard_df[dashboard_df['ID'] == selected_candidate]

if not candidate_data.empty:
    candidate_data = candidate_data.iloc[0]

    # Display candidate overview
    st.header("Candidate Overview")
    st.write(f"**ID:** {candidate_data['ID']}")
    st.write(f"**Gender:** {candidate_data['Gender']}")
    st.write(f"**Age:** {candidate_data['Age']}")
    st.write(f"**Position:** {candidate_data['Position']}")

    # Create containers for different visualizations
    container_1 = st.container()
    container_2 = st.container()
    container_3 = st.container()
    container_4 = st.container()
    container_5 = st.container()
    container_6 = st.container()

    # Visualization 1: Cognitive Ability Comparison
    with container_1:
        st.header("Cognitive Ability Comparison")
        
        # Filter inputs
        min_age, max_age = st.sidebar.slider("Select Age Range", min_value=dashboard_df['Age'].min(), max_value=dashboard_df['Age'].max(), value=(dashboard_df['Age'].min(), dashboard_df['Age'].max()))
        selected_positions = st.sidebar.multiselect("Select Positions", dashboard_df['Position'].unique())
        selected_genders = st.sidebar.multiselect("Select Genders", dashboard_df['Gender'].unique())

        # Apply filters
        filtered_data = dashboard_df[
            (dashboard_df['Age'] >= min_age) & (dashboard_df['Age'] <= max_age) &
            (dashboard_df['Position'].isin(selected_positions)) &
            (dashboard_df['Gender'].isin(selected_genders))
        ]

        # Extract cognitive ability scores for the selected candidate
        cognitive_columns = ['Logical Reasoning', 'Numerical Reasoning', 'Verbal Reasoning']
        selected_cognitive_scores = candidate_data[cognitive_columns].values[0]

        # Calculate average cognitive ability scores of all candidates
        average_cognitive_scores = filtered_data[cognitive_columns].mean()

        # Create a DataFrame to hold the scores for plotting
        comparison_df = pd.DataFrame({'Cognitive Ability': cognitive_columns,
                                      'Selected Candidate': selected_cognitive_scores,
                                      'Average Candidate': average_cognitive_scores})

        # Create a bar plot
        plt.figure(figsize=(8, 4))
        sns.set_palette("pastel")
        sns.barplot(data=comparison_df, x='Cognitive Ability', y='Selected Candidate', label='Selected Candidate')
        sns.barplot(data=comparison_df, x='Cognitive Ability', y='Average Candidate', label='Average Candidate', alpha=0.5)
        plt.xlabel("Cognitive Ability")
        plt.ylabel("Score")
        plt.title("Cognitive Ability Comparison")
        plt.legend()

        # Pass the figure to st.pyplot()
        st.pyplot(plt.gcf())

        # Download the figure
        download_figure(plt.gcf(), "cognitive_ability_comparison.png")
# Visualization 2: Performance Benchmarking
with container_2:
    st.header("Performance Benchmarking")
    
    # Apply filters to data
    filtered_data = dashboard_df[
        (dashboard_df['Age'] >= min_age) & (dashboard_df['Age'] <= max_age) &
        (dashboard_df['Position'].isin(selected_positions)) &
        (dashboard_df['Gender'].isin(selected_genders))
    ]
    
    # Calculate average scores for each cognitive ability
    average_scores = filtered_data[['Logical Reasoning', 'Numerical Reasoning', 'Verbal Reasoning']].mean()
    
    # Create a bar plot for benchmarking
    plt.figure(figsize=(8,4))
    sns.set_palette("pastel")
    sns.barplot(data=average_scores.reset_index(), x='index', y=0)
    plt.xlabel("Cognitive Ability")
    plt.ylabel("Average Score")
    plt.title("Performance Benchmarking")
    plt.xticks(rotation=45)
    
    # Pass the figure to st.pyplot()
    st.pyplot(plt.gcf())
    
    # Download the figure
    download_figure(plt.gcf(), "performance_benchmarking.png")

# Visualization 3: Personality Traits
with container_3:
    st.header("Personality Traits")
    
    # Apply filters to data
    filtered_data = dashboard_df[
        (dashboard_df['Age'] >= min_age) & (dashboard_df['Age'] <= max_age) &
        (dashboard_df['Position'].isin(selected_positions)) &
        (dashboard_df['Gender'].isin(selected_genders))
    ]
    
    # Create a bar plot for personality traits
    personality_traits = candidate_data[['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']]
    plt.figure(figsize=(8,4))
    sns.set_palette("pastel")
    sns.barplot(data=personality_traits.reset_index(), x='index', y=0)
    plt.xlabel("Personality Trait")
    plt.ylabel("Score")
    plt.title("Personality Traits")
    plt.xticks(rotation=45)
    
    # Pass the figure to st.pyplot()
    st.pyplot(plt.gcf())
    
    # Download the figure
    download_figure(plt.gcf(), "personality_traits.png")

# Visualization 4: IQ Score Analysis
with container_4:
    st.header("IQ Score Analysis")

    # Apply filters to data based on age, gender, and position
    filtered_data_age = dashboard_df[
        (dashboard_df['Age'] >= min_age) & (dashboard_df['Age'] <= max_age)
    ]
    
    filtered_data_gender = dashboard_df[
        (dashboard_df['Gender'] == candidate_data['Gender'])
    ]
    
    filtered_data_position = dashboard_df[
        (dashboard_df['Position'] == candidate_data['Position'])
    ]

    
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    sns.set_palette("pastel")
    
    for ax, filter_name, filtered_data in zip(axes, ['Age', 'Gender', 'Position'], [filtered_data_age, filtered_data_gender, filtered_data_position]):
        sns.histplot(data=filtered_data, x='IQ', bins=10, kde=True, ax=ax)
        ax.set_title(f"{filter_name} Filter", fontsize=12)
        ax.set_xlabel("IQ Score", fontsize=10)
        ax.set_ylabel("Frequency", fontsize=10)
        ax.tick_params(axis='both', which='major', labelsize=8)
    
    plt.tight_layout()
    st.pyplot(fig)
    download_figure(fig, "iq_score_distribution_filters.png")

    # Create a histogram for IQ scores in the dataset with position filter
    plt.figure(figsize=(10, 6))
    sns.set_palette("pastel")
    sns.histplot(data=filtered_data_position, x='IQ', bins=10, kde=True)


        # Visualization 5: Recommendation Status
# Visualization 5: Recommendation Status
with container_5:
    st.header("Recommendation Summary")
    
    # Apply filters
    filtered_data = dashboard_df[
        (dashboard_df['Age'] >= min_age) & (dashboard_df['Age'] <= max_age) &
        (dashboard_df['Position'].isin(selected_positions)) &
        (dashboard_df['Gender'].isin(selected_genders))
    ]
    
    # Filter input for threshold
    threshold = st.slider("Set Threshold for Recommendation", min_value=0, max_value=100, value=80)
    
    # Display recommendation status
    if candidate_data['Overall'] >= threshold:
        recommendation_status = "Recommended"
    else:
        recommendation_status = "Not Recommended"
    
    st.write(f"Based on the threshold of {threshold}, the candidate is **{recommendation_status}** for the role.")

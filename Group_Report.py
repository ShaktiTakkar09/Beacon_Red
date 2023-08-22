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


# Convert 'Date' column to date data type
dashboard_df['Date'] = pd.to_datetime(dashboard_df['Date']).dt.date

# Set Seaborn style
sns.set(style="whitegrid")

# Streamlit app
st.set_page_config(
    page_title="Group Report",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# title
st.markdown("<h1 style='font-size: 24px;'>Group Report</h1>", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("Filters")


# Date Range Filter
st.sidebar.subheader("Date Filter")
start_date = st.sidebar.date_input("Start Date", dashboard_df['Date'].min(), max_value=dashboard_df['Date'].max())
end_date = st.sidebar.date_input("End Date", dashboard_df['Date'].max(), min_value=start_date)

# Age Range Filter
st.sidebar.subheader("Age Filter")
start_age = st.sidebar.slider("Start Age", min_value=dashboard_df['Age'].min(), max_value=dashboard_df['Age'].max(), value=dashboard_df['Age'].min())
end_age = st.sidebar.slider("End Age", min_value=dashboard_df['Age'].min(), max_value=dashboard_df['Age'].max(), value=dashboard_df['Age'].max())

# Filter by role
st.sidebar.subheader("Role Filter")
selected_roles = st.sidebar.multiselect("Select Roles", dashboard_df['Position'].unique())

# Filter by gender
st.sidebar.subheader("Gender Filter")
selected_genders = st.sidebar.multiselect("Select Genders", dashboard_df['Gender'].unique())


# Apply filters to the DataFrame
filtered_data = dashboard_df[
    (dashboard_df['Position'].isin(selected_roles)) &
    (dashboard_df['Gender'].isin(selected_genders)) &
    (dashboard_df['Date'] >= start_date) & (dashboard_df['Date'] <= end_date)
]
### Performance Distribution
# Set font size
sns.set(font_scale=0.8)

# Create subplots for the three distributions
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
sns.set_palette("pastel")

# Plot 1: Performance Distribution by Age
sns.histplot(data=filtered_data, x='Overall', bins=10, kde=True, ax=axes[0])
axes[0].set_title("By Age")
axes[0].set_xlabel("Overall Performance Score")
axes[0].set_ylabel("Frequency")

# Plot 2: Performance Distribution by Gender
sns.histplot(data=filtered_data, x='Overall', bins=10, kde=True, hue='Gender', multiple='stack', ax=axes[1])
axes[1].set_title("By Gender")
axes[1].set_xlabel("Overall Performance Score")
axes[1].set_ylabel("Frequency")

# Plot 3: Performance Distribution by Position
sns.histplot(data=filtered_data, x='Overall', bins=10, kde=True, hue='Position', multiple='stack', ax=axes[2])
axes[2].set_title("By Position")
axes[2].set_xlabel("Overall Performance Score")
axes[2].set_ylabel("Frequency")
axes[2].legend(title="Position", fontsize=8)
axes[2].tick_params(axis='x', rotation=45)

# Adjust layout
plt.tight_layout()
st.pyplot(fig)

# Download the combined plot
download_figure(fig, "performance_distribution_combined.png")

### Cognitive Ability Comparison
cognitive_columns = ['Logical Reasoning', 'Numerical Reasoning', 'Verbal Reasoning']

# Calculate average cognitive ability scores by age
average_cognitive_scores_age = filtered_data.groupby('Age')[cognitive_columns].mean().reset_index()

# Calculate average cognitive ability scores by gender
average_cognitive_scores_gender = filtered_data.groupby('Gender')[cognitive_columns].mean().reset_index()

# Calculate average cognitive ability scores by position
average_cognitive_scores_position = filtered_data.groupby('Position')[cognitive_columns].mean().reset_index()

# Visualization: Cognitive Ability Comparison
st.header("Cognitive Ability Comparison")

# Create subplots for each comparison
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
sns.set_palette("pastel")

# Plot for age comparison
sns.barplot(data=average_cognitive_scores_age, x='Age', y='Logical Reasoning', label='Logical Reasoning', ax=axes[0])
sns.barplot(data=average_cognitive_scores_age, x='Age', y='Numerical Reasoning', label='Numerical Reasoning', ax=axes[0])
sns.barplot(data=average_cognitive_scores_age, x='Age', y='Verbal Reasoning', label='Verbal Reasoning', ax=axes[0])
axes[0].set_xlabel("Age")
axes[0].set_ylabel("Average Score")
axes[0].set_title("By Age")
axes[0].legend()

# Plot for gender comparison
sns.barplot(data=average_cognitive_scores_gender, x='Gender', y='Logical Reasoning', label='Logical Reasoning', ax=axes[1])
sns.barplot(data=average_cognitive_scores_gender, x='Gender', y='Numerical Reasoning', label='Numerical Reasoning', ax=axes[1])
sns.barplot(data=average_cognitive_scores_gender, x='Gender', y='Verbal Reasoning', label='Verbal Reasoning', ax=axes[1])
axes[1].set_xlabel("Gender")
axes[1].set_ylabel("Average Score")
axes[1].set_title("By Gender")
axes[1].legend()

# Plot for position comparison
sns.barplot(data=average_cognitive_scores_position, x='Position', y='Logical Reasoning', label='Logical Reasoning', ax=axes[2])
sns.barplot(data=average_cognitive_scores_position, x='Position', y='Numerical Reasoning', label='Numerical Reasoning', ax=axes[2])
sns.barplot(data=average_cognitive_scores_position, x='Position', y='Verbal Reasoning', label='Verbal Reasoning', ax=axes[2])
axes[2].set_xlabel("Position")
axes[2].set_ylabel("Average Score")
axes[2].set_title("By Position")
axes[2].legend()

# Adjust layout
plt.tight_layout()
st.pyplot(fig)

# Download the combined plot
download_figure(fig, "cognitive_ability_comparison.png")
# Personality Trait Insights
st.markdown("<h2>3. Personality Trait Insights:</h2>", unsafe_allow_html=True)

# Apply filters to the DataFrame for Personality Trait Insights
filtered_data_traits = dashboard_df[
    (dashboard_df['Position'].isin(selected_roles)) &
    (dashboard_df['Gender'].isin(selected_genders)) &
    (dashboard_df['Age'] >= start_age) & (dashboard_df['Age'] <= end_age)  # Use the age_range filter here
]
# Calculate the average personality trait scores
average_traits = filtered_data_traits[['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']].mean()

# Create a bar plot for personality trait distribution
plt.figure(figsize=(8, 5))
sns.set_palette("pastel")
sns.barplot(x=average_traits.index, y=average_traits.values)
plt.xlabel("Personality Traits")
plt.ylabel("Average Score")
plt.title("Personality Trait Insights")
plt.ylim(0, 100)  # Set y-axis range to 0-100
st.pyplot(plt.gcf())
download_figure(plt.gcf(), "personality_trait_insights.png")

# Performance Trend Over Time
st.markdown("<h2>Performance Trend Over Time:</h2>", unsafe_allow_html=True)

# Group data by Date and calculate the average performance
average_performance_by_date = filtered_data.groupby('Date')['Overall'].mean().reset_index()

# Visualization: Performance Trend Over Time
plt.figure(figsize=(10, 5))
sns.set_palette("pastel")
sns.lineplot(data=average_performance_by_date, x='Date', y='Overall')
plt.xlabel("Date")
plt.ylabel("Average Performance Score")
plt.title("Performance Trend Over Time")
plt.xticks(rotation=45)
st.pyplot(plt.gcf())
download_figure(plt.gcf(), "performance_trend_over_time.png")

# Group IQ Analysis
st.markdown("<h2>5. Group IQ Analysis:</h2>", unsafe_allow_html=True)

# Filtered data for IQ analysis
filtered_iq_data = dashboard_df[
    (dashboard_df['Position'].isin(selected_roles)) &
    (dashboard_df['Gender'].isin(selected_genders)) &
    (dashboard_df['Age'] >= start_age) & (dashboard_df['Age'] <= end_age)  # Use the age_range filter here
]

if not filtered_iq_data.empty:
    # Visualization: Group IQ Analysis
    plt.figure(figsize=(8, 4))
    sns.set_palette("pastel")
    sns.histplot(data=filtered_iq_data, x='IQ', bins=10, kde=True)
    plt.xlabel("IQ Score")
    plt.ylabel("Frequency")
    plt.title("Group IQ Analysis")
    st.pyplot(plt.gcf())
    download_figure(plt.gcf(), "group_iq_analysis.png")
else:
    st.markdown("No data available for the selected filters.", unsafe_allow_html=True)
    
   # Recommendation Summary
st.markdown("<h2>6. Recommendation Summary:</h2>", unsafe_allow_html=True)

# Filter input for threshold
threshold = st.slider("Set Threshold for Recommendation", min_value=0, max_value=100, value=80)

# Calculate the recommendation status based on the threshold
filtered_data['Recommendation'] = filtered_data['Overall'] >= threshold

# Calculate the count of "Recommended" and "Not Recommended" candidates
recommendation_counts = filtered_data['Recommendation'].value_counts()
recommended_count = recommendation_counts.get(True, 0)
not_recommended_count = recommendation_counts.get(False, 0)

# Display recommendation summary
st.write(f"Number of Recommended Candidates: {recommended_count}")
st.write(f"Number of Not Recommended Candidates: {not_recommended_count}")


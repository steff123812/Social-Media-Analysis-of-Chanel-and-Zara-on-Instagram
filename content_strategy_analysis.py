# MSc Business Analytics Project – Exploratory analysis script
# Note: This script reflects an iterative academic workflow.
# Some sections are exploratory/commented and not intended as a production pipeline.

# %%
# This section imports the required data analysis library (Pandas)
# and loads the Instagram post data from an Excel file.
# The Excel file contains two sheets:
# - Sheet 1: Zara Instagram posts
# - Sheet 2: Chanel Instagram posts
# Each sheet is loaded into a separate table (DataFrame) so that
# both brands can be analysed and compared independently.

import pandas as pd

# Load Excel file with two sheets
import os

file_name = "zara_posts_raw(AutoRecovered)-2.xlsx"   # e.g. "zara_chanel_dataset.xlsx"
file_path = os.path.join("/Users/steff/Downloads", file_name)
zara_df = pd.read_excel(file_path, sheet_name=0)
chanel_df = pd.read_excel(file_path, sheet_name=1)

# %%
# This section performs an initial inspection of the datasets.
# The first few rows are displayed to verify that the data
# has been loaded correctly and to understand the structure.
# Missing values are then counted for each column to identify
# any data quality issues that may affect the analysis.

# Preview datasets
print(zara_df.head())
print(chanel_df.head())

# Check for missing values
print(zara_df.isnull().sum())
print(chanel_df.isnull().sum())


# %%
# This step cleans the data by removing posts that do not have
# a defined content type (for example: reel, image, carousel).
# Content type is a critical variable for this analysis,
# so rows missing this information are excluded to ensure
# reliable and meaningful comparisons.

zara_df = zara_df.dropna(subset=['content_type'])
chanel_df = chanel_df.dropna(subset=['content_type'])

# %%
# This section calculates how frequently each type of content
# appears in the Instagram posts of Zara and Chanel.
# It helps identify each brand’s content strategy by showing
# whether they rely more on reels, images, or other formats.
# The results are printed for transparent inspection.
 
zara_content_counts = zara_df['content_type'].value_counts()
chanel_content_counts = chanel_df['content_type'].value_counts()

print("Zara Content Types:\n", zara_content_counts)
print("\nChanel Content Types:\n", chanel_content_counts)

# %%
# This section visualises the distribution of content types
# using bar charts.
# Two charts are shown side-by-side to enable an easy visual
# comparison between Zara and Chanel.
# Visualisation is used here to make patterns and differences
# in content strategy more intuitive and accessible.

import matplotlib.pyplot as plt

# Plot side-by-side bar charts
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
zara_content_counts.plot(kind='bar', title='Zara Content Types')
plt.ylabel("Number of Posts")

plt.subplot(1, 2, 2)
chanel_content_counts.plot(kind='bar', color='orange', title='Chanel Content Types')

plt.tight_layout()
plt.show()

# %%
# This section performs a simple text analysis on post captions
# to identify the most commonly used keywords by each brand.
# Captions are converted to lowercase, cleaned, and filtered
# to retain meaningful words (minimum four letters).
# The most frequent keywords provide insight into the themes
# and messaging priorities of Zara and Chanel.

from collections import Counter
import re

def get_keywords(captions):
    words = " ".join(captions.dropna()).lower()
    words = re.findall(r'\b[a-z]{4,}\b', words)  # only words with 4+ letters
    return Counter(words).most_common(15)

# This final step prints the most frequently used keywords
# for both brands.
# The output supports qualitative interpretation by highlighting
# recurring themes in brand communication.

print("Zara Top Words:", get_keywords(zara_df['caption_text']))
print("Chanel Top Words:", get_keywords(chanel_df['caption_text']))

# %%
# This section imports the plotting library used to create charts.
# Visualisation helps present patterns in the data in a way that
# is easy to interpret for non-technical audiences.

import matplotlib.pyplot as plt
# Brand labels are added to each dataset so that posts from
# Zara and Chanel can be clearly distinguished after merging.
# This enables a direct comparison between the two brands
# within a single combined dataset.

# Add brand labels
zara_df['Brand'] = 'Zara'
chanel_df['Brand'] = 'Chanel'

# The two datasets are merged into one unified table.
# Combining the data simplifies comparative analysis and
# allows grouping, counting, and visualisation across brands
# using a consistent structure.

# Combine datasets
df = pd.concat([zara_df, chanel_df], ignore_index=True)

# This step specifies the column that indicates the type of
# influencer associated with each post.
# A validation check is performed to ensure that the expected
# column exists in the dataset before proceeding.

# Rename influencer column if needed (make sure it matches your actual sheet column name)
influencer_col = 'Influencer Type'  # Adjust if needed
if influencer_col not in df.columns:
    print("Check the exact column name for influencer type in your file.")
else:
    # Influencer types are stored as numeric codes in the dataset.
    # These codes are converted into human-readable labels
    # (None, Influencer, Celebrity) to improve interpretability
    # for analysis and reporting.

    # Convert influencer type to readable labels
    influencer_map = {0: 'None', 1: 'Influencer', 2: 'Celebrity'}
    df['Influencer_Label'] = df[influencer_col].map(influencer_map)

    # The data is grouped by brand and influencer type to calculate
    # how many posts fall into each category.
    # This quantifies the extent to which each brand relies on
    # influencers or celebrities in their content strategy.

    # Group and count
    counts = df.groupby(['Brand', 'Influencer_Label']).size().unstack(fill_value=0)

    # A bar chart is created to visually compare influencer usage
    # between Zara and Chanel.
    # This visual representation highlights strategic differences
    # in brand communication and endorsement approaches.

    # Plot
    counts.plot(kind='bar', figsize=(8, 6))
    plt.title('Influencer Type Distribution by Brand')
    plt.ylabel('Number of Posts')
    plt.xlabel('Brand')
    plt.xticks(rotation=0)
    plt.legend(title='Influencer Type')
    plt.tight_layout()
    plt.show()

# %%
import pandas as pd
import os

file_name = "zara_posts_raw(AutoRecovered)-2.xlsx"   # e.g. "zara_chanel_dataset.xlsx"
file_path = os.path.join("/Users/steff/Downloads", file_name)

comments_df = pd.read_excel(file_path)
comments_df.head()


# %%
import re

# Function to clean text
def clean_text(text):
    if pd.isnull(text):
        return ""
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.lower()                  # Lowercase
    return text

# Apply to Zara comments column (assume column name is 'Comments' or similar)
comments_df['clean_comment'] = comments_df['comments'].apply(clean_text)


# %%
from textblob import TextBlob

# Calculate sentiment polarity for each comment
comments_df['sentiment'] = comments_df['clean_comment'].apply(lambda x: TextBlob(x).sentiment.polarity)

# Average sentiment score
avg_sentiment = comments_df['sentiment'].mean()
print("Average Zara Sentiment Score:", avg_sentiment)

# %%
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Combine all cleaned comments
all_words = " ".join(comments_df['clean_comment'].dropna())

# Generate word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_words)

# Display word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Common Words in Zara Comments")
plt.show()

# %%
import emoji
from collections import Counter
import pandas as pd

def extract_emojis(s):
    if pd.isna(s):
        return ""
    s = str(s)  # ensures it's iterable
    return ''.join(c for c in s if c in emoji.EMOJI_DATA)

comments_df['emojis'] = comments_df['comments'].apply(extract_emojis)

emoji_counter = Counter("".join(comments_df['emojis']))
print("Most common emojis:", emoji_counter.most_common(10))

# %%
# --- RQ2: What type of content drives the most engagement or emotional response in the comments? ---

# Sentiment Analysis
from textblob import TextBlob

def get_sentiment(text):
    return TextBlob(str(text)).sentiment.polarity

zara_df['sentiment_score'] = zara_df['comments'].apply(get_sentiment)

zara_df['sentiment_label'] = zara_df['sentiment_score'].apply(
    lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'neutral'))

# Count the sentiment labels
print("Sentiment distribution:")
print(zara_df['sentiment_label'].value_counts())

# %%
# Visualize Sentiment Distribution
import seaborn as sns
import matplotlib.pyplot as plt

sns.countplot(x='sentiment_label', data=zara_df)
plt.title('Sentiment Distribution in Zara Comments')
plt.xlabel('Sentiment')
plt.ylabel('Number of Comments')
plt.show()

# %%
# Optional: Topic Modeling to extract common themes
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Vectorize cleaned comments
vectorizer = CountVectorizer(stop_words='english', max_df=0.9, min_df=2)
doc_term_matrix = vectorizer.fit_transform(zara_df['comments'].dropna())

lda = LatentDirichletAllocation(n_components=3, random_state=42)
lda.fit(doc_term_matrix)

# Print top words per topic
for idx, topic in enumerate(lda.components_):
    print(f"Topic #{idx + 1}:")
    print([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-10:]])

# %%
# Correlate sentiment with likes (if 'likes' column is present)
if 'likes' in zara_df.columns:
    sns.scatterplot(data=zara_df, x='sentiment_score', y='likes')
    plt.title("Zara Post Likes vs Comment Sentiment")
    plt.show()

    print("Average likes per sentiment category:")
    print(zara_df.groupby('sentiment_label')['likes'].mean())

# %%
# -- LDA Topic Modeling on Zara Comments --
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Preprocess comments
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
zara_comments_clean = zara_df['comments'].dropna().astype(str).str.lower()

vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words=stop_words)
dtm = vectorizer.fit_transform(zara_comments_clean)

lda = LatentDirichletAllocation(n_components=3, random_state=42)
lda.fit(dtm)

# Show top words per topic
def display_topics(model, feature_names, no_top_words):
    for idx, topic in enumerate(model.components_):
        print(f"Topic {idx + 1}:")
        print(" | ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))

display_topics(lda, vectorizer.get_feature_names_out(), 10)


# %%
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
from sklearn.decomposition import LatentDirichletAllocation

# 1) Pick the text column you want
# Change 'clean_comment' to your actual column name if needed
texts = comments_df["clean_comment"].fillna("").astype(str)

# 2) Vectorize (document-term matrix)
vectorizer = CountVectorizer(
    stop_words=list(ENGLISH_STOP_WORDS),
    max_df=0.95,
    min_df=2
)
dtm = vectorizer.fit_transform(texts)

# 3) Fit LDA (choose number of topics)
n_topics = 8
lda = LatentDirichletAllocation(
    n_components=n_topics,
    random_state=42,
    learning_method="batch"
)
lda.fit(dtm)

# 4) Visualize with pyLDAvis
import pyLDAvis
import pyLDAvis.lda_model

pyLDAvis.enable_notebook()
lda_vis = pyLDAvis.lda_model.prepare(lda, dtm, vectorizer)
lda_vis

# %%
import pyLDAvis
import pyLDAvis.sklearn
pyLDAvis.enable_notebook()

panel = pyLDAvis.sklearn.prepare(lda, dtm, vectorizer)
panel


# %%
import pyLDAvis
import pyLDAvis.lda_model

lda_vis = pyLDAvis.lda_model.prepare(lda, dtm, vectorizer)
lda_vis

# %%
pyLDAvis.save_html(lda_vis, "lda_vis.html")

# %%
# Assuming sentiment is already calculated in zara_df['sentiment']
import seaborn as sns
import matplotlib.pyplot as plt

sns.boxplot(data=zara_df, x='content_type', y='sentiment')
plt.title("Sentiment by Content Type for Zara")
plt.show()

# %%
import seaborn as sns
import matplotlib.pyplot as plt

sns.boxplot(data=zara_df, x="content_type", y="sentiment_score")
plt.title("Sentiment by Content Type for Zara")
plt.show()

# %%

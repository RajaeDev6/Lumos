import os
from dotenv import load_dotenv
from google import genai
import csv
import io
import pandas as pd

# Load variables from .env
load_dotenv()

# Functions
def generate_csv_template(topics_list):
    """
    Creates a CSV template string based on topics.
    Example input: ["Reading", "Grammar"]
    Output CSV:
    student,Reading,Grammar
    """
    output = io.StringIO()
    writer = csv.writer(output)

    header = ["student"] + topics_list
    writer.writerow(header)

    return output.getvalue()

def convert_csv_to_topic_scores(csv_path):
    # Load the CSV the teacher filled in
    df = pd.read_csv(csv_path)

    # The first column MUST be "student"
    # The rest are topic names
    topic_columns = df.columns[1:]  # Skip “student”

    topics_list = []

    # Loop through each topic (Reading, Grammar, etc.)
    for topic in topic_columns:
        # Drop NaN and convert all scores to a list
        scores = df[topic].dropna().tolist()

        topics_list.append({
            "topic": topic,
            "scores": scores
        })

    return topics_list

# Access the API key
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words"
)

print(response.text)

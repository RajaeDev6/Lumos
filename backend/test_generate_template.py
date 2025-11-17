import os
import json
from dotenv import load_dotenv
from google import genai
import csv
import io
from config.settings import settings
from utils.app_logger import logger

# --- AI CONFIG ---
client = genai.Client(api_key=settings.GEMINI_API_KEY)

def extract_questions_with_topics(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    prompt = """
    Extract all exam questions from this PDF.

    Return ONLY valid JSON array:
    [
      {
        "number": <number>,
        "question": "<exact text>",
        "image_description": "<short description or null>",
        "topic": "<detected topic>"
      }
    ]
    """

    pdf_input = {
        "inline_data": {
            "mime_type": "application/pdf",
            "data": pdf_bytes
        }
    }

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[{"text": prompt}, pdf_input],
        config={"response_mime_type": "application/json"}
    )

    return json.loads(response.text)


def extract_unique_topics(questions):
    topics = set()
    for q in questions:
        if q.get("topic"):
            topics.add(q["topic"].strip())
    return list(topics)


def generate_csv_template_from_topics(topics):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["student"] + topics)
    return output.getvalue()


def generate_template_from_pdf(pdf_path):
    logger.info("📤 Extracting questions + topics...")

    questions = extract_questions_with_topics(pdf_path)

    topics = extract_unique_topics(questions)
    logger.info("📌 Topics detected:", topics)

    csv_data = generate_csv_template_from_topics(topics)

    out_path = "generated_template.csv"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(csv_data)

    logger.info(f"✅ CSV saved at: {out_path}")
    return out_path


# MAIN for testing
if __name__ == "__main__":
    pdf_path = input("Enter PDF path: ").strip()
    generate_template_from_pdf(pdf_path)

import base64
import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
import csv
import io
from config.settings import settings
from utils.app_logger import logger

# --- AI CONFIG ---
client = genai.Client(api_key=settings.GEMINI_API_KEY)


# -------------------------------------------------------
# Utility: load PDF or text file into Gemini-compatible Part
# -------------------------------------------------------
def load_file(path):
    ext = path.lower()

    # PDF INPUT
    if ext.endswith(".pdf"):
        with open(path, "rb") as f:
            data = f.read()

        return types.Part(
            inline_data=types.Blob(
                mime_type="application/pdf",
                data=data  # IMPORTANT: raw bytes, NOT base64
            )
        )

    # TEXT INPUT
    with open(path, "r", encoding="utf-8") as f:
        return types.Part(text=f.read())


# -------------------------------------------------------
# 1. Extract Questions + Topics
# -------------------------------------------------------
def extract_questions_with_topics(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    pdf_input = types.Part(
        inline_data=types.Blob(
            mime_type="application/pdf",
            data=pdf_bytes
        )
    )

    prompt = """
You are an expert educational examiner and curriculum specialist.
Your task is to analyze the exam paper and extract:

- Question number
- Exact question text (NO rewriting)
- The most appropriate academic topic/subtopic

Your output MUST be ONLY valid JSON.

---------------------
RULES FOR EXTRACTION
---------------------
1. Preserve the exact wording of every question. Do NOT rewrite or summarize.
2. Determine the most specific topic possible (e.g. “Algebra — Linear Equations”, 
   “Grammar — Past Tense”, “Reading Comprehension — Inference”).
3. Topics must be meaningful, skill-based, and curriculum-aligned.
4. DO NOT invent topics unrelated to the question.
5. If a question contains multiple skills, choose the PRIMARY one.
6. If the topic is unclear, infer the closest reasonable topic.

---------------------
STRICT FORMAT:
---------------------
[
  {
    "number": <question number>,
    "question": "<exact question text>",
    "topic": "<topic or subtopic>"
  }
]

Return ONLY the JSON array. No explanations.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[types.Part(text=prompt), pdf_input],
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    return json.loads(response.text)


# -------------------------------------------------------
# 2. Compare Teacher vs Student Answers
# -------------------------------------------------------
def compare_answers(questions, teacher_file, student_file):
    teacher_part = load_file(teacher_file)
    student_part = load_file(student_file)

    prompt = f"""
You will compare TEACHER answers with STUDENT answers.

QUESTIONS:
{json.dumps(questions, indent=2)}

-------------------------
STRICT OUTPUT FORMAT:
-------------------------
Return ONLY JSON:
[
  {{
    "question_number": <num>,
    "topic": "<topic>",
    "teacher_answer": "<text>",
    "student_answer": "<text>",
    "correct": true/false
  }}
]

RULES:
- Match answers by question number
- Mark TRUE if answers are logically equivalent
- Mark FALSE if wrong, missing, empty, or ambiguous
- Do NOT solve questions, only compare
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part(text=prompt),
            types.Part(text="TEACHER ANSWERS:"), teacher_part,
            types.Part(text="STUDENT ANSWERS:"), student_part
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    return json.loads(response.text)


# -------------------------------------------------------
# 3. Build Topic Performance Table
# -------------------------------------------------------
def compute_topic_scores(results):
    topic_stats = {}

    for item in results:
        topic = item["topic"]
        correct = item["correct"]

        if topic not in topic_stats:
            topic_stats[topic] = {"correct": 0, "incorrect": 0}

        topic_stats[topic]["correct" if correct else "incorrect"] += 1

    return topic_stats


# -------------------------------------------------------
# Main pipeline
# -------------------------------------------------------
def process_exam(question_pdf, teacher_ans, student_ans):
    logger.info("📄 Extracting questions...")
    questions = extract_questions_with_topics(question_pdf)

    logger.info("📝 Comparing answers...")
    results = compare_answers(questions, teacher_ans, student_ans)

    logger.info("📊 Computing topic performance...")
    stats = compute_topic_scores(results)

    return {
        "questions": questions,
        "comparison": results,
        "topic_stats": stats
    }


# -------------------------------------------------------
# TESTING CLI
# -------------------------------------------------------
if __name__ == "__main__":
    qp = input("Question Paper PDF: ").strip().strip('"')
    tp = input("Teacher Answers (PDF or txt): ").strip().strip('"')
    sp = input("Student Answers (PDF or txt): ").strip().strip('"')

    output = process_exam(qp, tp, sp)
    print(json.dumps(output, indent=2))

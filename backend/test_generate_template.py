import base64
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

# -------------------------
# Utility: load PDF or text
# -------------------------
def load_file(path):
    ext = path.lower()

    if ext.endswith(".pdf"):
        with open(path, "rb") as f:
            data = f.read()
        return types.Part(
            inline_data=types.Blob(
                mime_type="application/pdf",
                data=base64.b64encode(data).decode("utf-8")
            )
        )

    else:
        with open(path, "r", encoding="utf-8") as f:
            return types.Part(text=f.read())


# -------------------------
# 1. Extract Questions + Topics
# -------------------------
def extract_questions_with_topics(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    pdf_input = types.Part(
        inline_data=types.Blob(
            mime_type="application/pdf",
            data=base64.b64encode(pdf_bytes).decode("utf-8")
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
FORMAT STRICTLY REQUIRED:
---------------------
[
  {
    "number": <question number>,
    "question": "<exact question text>",
    "topic": "<topic or subtopic>"
  }
]

Example topics:
- Mathematics: Algebra, Geometry, Trigonometry, Calculus, Statistics, Measurement
- English: Reading Comprehension, Vocabulary, Grammar — Tenses, Writing Skills
- Science: Physics — Forces, Chemistry — Acids, Biology — Cells
- Other subjects: use clear, curriculum-based terms.

Do NOT output commentary, reasoning, or explanation.
Return ONLY the JSON array.
"""


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[types.Part(text=prompt), pdf_input],
        config=types.GenerateContentConfig(response_mime_type="application/json")
    )

    return json.loads(response.text)


# -------------------------
# 2. Compare Teacher vs Student Answers
# -------------------------
def compare_answers(questions, teacher_file, student_file):
    teacher_part = load_file(teacher_file)
    student_part = load_file(student_file)

    prompt = f"""
    You will compare teacher answers vs student answers.

    QUESTIONS:
    {json.dumps(questions, indent=2)}

    STRICT OUTPUT FORMAT:
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
    - Match answers based on question number.
    - Correct if logically equivalent.
    - If ambiguous, choose FALSE.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part(text=prompt),
            types.Part(text="TEACHER ANSWERS:"), teacher_part,
            types.Part(text="STUDENT ANSWERS:"), student_part
        ],
        config=types.GenerateContentConfig(response_mime_type="application/json")
    )

    return json.loads(response.text)


# -------------------------
# 3. Convert to Topic Performance
# -------------------------
def compute_topic_scores(results):
    topic_stats = {}

    for item in results:
        topic = item["topic"]
        correct = item["correct"]

        if topic not in topic_stats:
            topic_stats[topic] = {"correct": 0, "incorrect": 0}

        if correct:
            topic_stats[topic]["correct"] += 1
        else:
            topic_stats[topic]["incorrect"] += 1

    return topic_stats


# -------------------------
# Main pipeline
# -------------------------
def process_exam(question_pdf, teacher_ans, student_ans):
    print("📄 Extracting questions...")
    questions = extract_questions_with_topics(question_pdf)

    print("📝 Comparing answers...")
    results = compare_answers(questions, teacher_ans, student_ans)

    print("📊 Computing topic performance...")
    stats = compute_topic_scores(results)

    return {
        "questions": questions,
        "comparison": results,
        "topic_stats": stats
    }


# TESTING
if __name__ == "__main__":
    qp = input("Question Paper PDF: ").strip()
    tp = input("Teacher Answers (PDF or txt): ").strip()
    sp = input("Student Answers (PDF or txt): ").strip()

    output = process_exam(qp, tp, sp)

    print(json.dumps(output, indent=2))

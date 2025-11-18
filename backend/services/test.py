import sys, os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

print("PYTHONPATH:", BASE_DIR)

import json
from utils.app_logger import logger
from AI_engine import process_exam_full

print("\n=== AI Exam Processor CLI Test ===\n")

def fix_path(path_str):
    path_str = path_str.strip().strip('"')
    # If user enters absolute path → use as is
    if os.path.isabs(path_str):
        return path_str
    # Else convert relative to absolute
    return os.path.abspath(os.path.join(BASE_DIR, path_str))

q_pdf = fix_path(input("Enter Question Paper PDF path: "))
t_ans = fix_path(input("Enter Teacher Answer file (PDF or TXT): "))
s_ans = fix_path(input("Enter Student Answer file (PDF or TXT): "))


print("\n⏳ Running full AI processing...\n")

result = process_exam_full(q_pdf, t_ans, s_ans)

print("\n=== FINAL OUTPUT ===\n")
print(json.dumps(result, indent=2))

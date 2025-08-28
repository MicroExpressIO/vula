# security_agent_checker.py

import json
from typing import List, Dict
import os
import openai  # For OpenAI integration
import google.generativeai as genai  # For Gemini integration
import logging
from datetime import datetime

# Setup logging
log_file = f"security_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 1. Build local security programming standard knowledge base
security_kb = [
    {"id": "SEC001", "rule": "All user passwords must be hashed using bcrypt or Argon2."},
    {"id": "SEC002", "rule": "Do not store plaintext credentials in code or config files."},
    {"id": "SEC003", "rule": "Use HTTPS for all data transmissions."},
    {"id": "SEC004", "rule": "Input validation must be performed on all external inputs."},
    {"id": "SEC005", "rule": "Use parameterized queries to prevent SQL injection."}
]

# 2. Mock a user design document with use cases
mock_user_doc = [
    {
        "title": "User login system",
        "description": "Passwords are stored in plaintext for quick access.",
        "has_security_section": True
    },
    {
        "title": "Payment gateway",
        "description": "The system uses HTTPS and input validation.",
        "has_security_section": True
    },
    {
        "title": "Email service integration",
        "description": "Service connects using HTTP.",
        "has_security_section": False
    },
    {
        "title": "User registration",
        "description": "Password is hashed using bcrypt and input is validated.",
        "has_security_section": True
    },
    {
        "title": "Admin report system",
        "description": "SQL queries are built using user input directly.",
        "has_security_section": False
    }
]

# 3. Use LLM to evaluate design doc description against knowledge base
openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def llm_check_against_kb(description: str, kb: List[Dict], method: str = "openai") -> List[str]:
    rules = "\n".join([f"{item['id']}: {item['rule']}" for item in kb])
    prompt = f"""
    Here is a list of security rules:
    {rules}

    Below is a system design description. List any rules that are violated:
    """
    input_text = prompt + f"\n\nDescription:\n{description}"

    try:
        if method == "openai":
            response = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=[
                    {"role": "system", "content": "You are a security compliance checker."},
                    {"role": "user", "content": input_text}
                ],
                temperature=0.2,
            )
            return [response.choices[0].message['content']]

        elif method == "gemini":
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(input_text)
            return [response.text]

    except Exception as e:
        return [f"[LLM error]: {str(e)}"]

# 4. External search (OpenAI or Gemini)
def external_search_solution(issue: str, method: str = "openai") -> str:
    if method == "openai":
        return call_openai_solution(issue)
    elif method == "gemini":
        return call_gemini_solution(issue)
    else:
        return f"[Manual Lookup] {issue} => Please consult OWASP guidelines."

def call_openai_solution(issue: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": "You are a security advisor."},
                {"role": "user", "content": f"Give security best practices or mitigation steps for: {issue}"}
            ],
            temperature=0.3,
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"[OpenAI Error] {str(e)}"

def call_gemini_solution(issue: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Give security best practices or mitigation steps for: {issue}")
        return response.text
    except Exception as e:
        return f"[Gemini Error] {str(e)}"

# 5. AI Agent Review with Logging and Report

def ai_agent_review(design_docs: List[Dict], kb: List[Dict], method: str = "openai"):
    results = []
    for doc in design_docs:
        title = doc["title"]
        print(f"\n[Reviewing: {title}]")
        violations = llm_check_against_kb(doc["description"], kb, method)

        if violations:
            print("Violations Detected:")
            for v in violations:
                print("-", v)
                logging.info(f"{title} - VIOLATION: {v}")
                solution = external_search_solution(v, method)
                print("Suggestion:", solution)
                logging.info(f"{title} - SUGGESTION: {solution}")
        else:
            print("No Issues Detected.")
            logging.info(f"{title} - COMPLIANT")

        results.append({"title": title, "violations": violations})

    with open("security_review_report.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\n[Review Completed] Report saved to security_review_report.json and log file.")

# 6. Entry Point

def main():
    print("[AI Security Agent] Starting security review of user designs...\n")
    method = os.getenv("AI_PROVIDER", "openai")  # 'openai' or 'gemini'
    ai_agent_review(mock_user_doc, security_kb, method)

if __name__ == "__main__":
    main()

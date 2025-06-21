# security_agent_checker.py

import json
from typing import List, Dict
import os
import sys
import openai  # For OpenAI integration
#import google.generativeai as genai  # For Gemini integration
from google import genai
from google.genai import types

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)
from config.config import config

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

# 3. Check against knowledge base (rule-based)
def check_security_compliance(doc: Dict, kb: List[Dict]) -> List[str]:
    findings = []
    desc = doc["description"].lower()
    title = doc["title"]

    for rule in kb:
        if rule["id"] == "SEC001" and "hashed" not in desc:
            findings.append(f"{title}: {rule['rule']}")
        elif rule["id"] == "SEC002" and "plaintext" in desc:
            findings.append(f"{title}: {rule['rule']}")
        elif rule["id"] == "SEC003" and "https" not in desc:
            findings.append(f"{title}: {rule['rule']}")
        elif rule["id"] == "SEC004" and "validation" not in desc:
            findings.append(f"{title}: {rule['rule']}")
        elif rule["id"] == "SEC005" and "sql" in desc and "parameterized" not in desc:
            findings.append(f"{title}: {rule['rule']}")

    return findings

# 4. Simulated external search tool (mocked or LLM powered)
#def external_search_solution(issue: str, method: str = "openai") -> str:
def external_search_solution(issue: str, method: str = "openai") -> str:
    if method == "openai":
        return call_openai_solution(issue)
    elif method == "gemini":
        return call_gemini_solution(issue)
    else:
        print(f"[Tool] Searching external solution for: {issue}")
        return f"[External Solution] Best practice for: {issue} -> Visit OWASP documentation."

# 4A. Function calling: OpenAI API integration

openai.api_key = os.getenv("OPENAI_API_KEY")

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
        return f"[Error fetching solution from OpenAI]: {str(e)}"


# 4B. Gemini integration via Google Generative AI SDK
#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def call_gemini_solution(issue: str) -> str:
    try:
        client = genai.Client(api_key=config.key)
        user_content = f"Give security best practices or mitigation steps for: {issue}"
        response = client.models.generate_content(
            model=config.model,
            contents=user_content
        )
        
        return response.text
    except Exception as e:
        return f"[Error fetching solution from Gemini]: {str(e)}"

# 5. Main AI Agent Routine
def ai_agent_review(design_docs: List[Dict], kb: List[Dict], method: str = "openai"):
    all_findings = []
    for doc in design_docs:
        violations = check_security_compliance(doc, kb)
        if violations:
            print(f"\n[Security Issues Found in '{doc['title']}']")
            for v in violations:
                print("-", v)
                solution = external_search_solution(v, method)
                print(solution)
        else:
            print(f"\n[No Issues] '{doc['title']}' complies with all known security standards.")

# 6. Entry Point
def main():
    print("[AI Security Agent] Starting security review of user designs...\n")
    #method = os.getenv("AI_PROVIDER", "openai")  # 'openai' or 'gemini'
    method = config.ai_provider
    ai_agent_review(mock_user_doc, security_kb, method)

if __name__ == "__main__":
    main()

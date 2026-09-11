
from langchain_core.prompts import PromptTemplate

from langchain_groq import ChatGroq

from .retriever import retrieve_schema

import os
from dotenv import load_dotenv

load_dotenv()


# Configure the Groq model via environment so it can be changed without edits.
DEFAULT_GROQ_MODEL = "openai/gpt-oss-20b"


def _create_llm():
    model_name = os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL)
    api_key = os.getenv("GROQ_API_KEY")
    return ChatGroq(model=model_name, temperature=0, api_key=api_key)




# Prompt Template
prompt = PromptTemplate(
    template="""
You are an SQL expert.

Your job is to convert user questions into a valid SQLite SQL query.

User question:
{question}

Schema:
{schema}

-------------------------
RULES:
-------------------------

- Use only the given tables and columns.
- Table names must be used EXACTLY as provided in the schema.
  Do NOT rename, modify, or correct table names.
- Column names must EXACTLY match the schema.
- Use ONLY SQLite syntax.
- Output ONLY the SQL query.
- Do NOT include explanations, markdown, or backticks.
- Do NOT generate DELETE, UPDATE, INSERT, or SET queries.
-While using attendance table use "attendance_attendence" . 

-------------------------
IMPORTANT COLUMN RULE:
-------------------------

- If you need to display employee identifier, use:
    employees_employee.employee_id
- Do NOT use "employee" column (it does not exist).

-------------------------
FOREIGN KEY RULES:
-------------------------

- Foreign keys are stored as <field>_id.
- Use JOIN when querying related tables.
# - Always join using:
#     parent_table.id = child_table.<field>_id

- NEVER join using:
    employee_id = employee_id (wrong)

-------------------------
JOIN EXAMPLE:
-------------------------

Correct:
SELECT e.employee_id, bd.bank_name
FROM employees_employee e
JOIN onboarding_bankdetails bd
ON bd.employee_id = e.id;

Wrong:
SELECT e.employee_id
FROM employees_employee e
JOIN onboarding_bankdetails bd
ON bd.employee_id = e.employee_id;

-------------------------
NOT EXISTS RULE:
-------------------------

When finding missing records, use NOT EXISTS:

SELECT e.employee_id
FROM employees_employee e
WHERE NOT EXISTS (
    SELECT 1
    FROM onboarding_laptopallocation la
    WHERE la.employee_id = e.id
);

-------------------------
GENERAL GUIDELINES:
-------------------------

- Use table aliases (e, bd, ip, la, etc.)
- Prefer explicit JOINs over implicit joins
- Ensure all columns exist in schema
- Ensure joins use correct primary key (id)

-------------------------
Now generate the SQL query.
"""
)



def generate_query_plan(question):

    schema_context, _ = retrieve_schema(question, k=3)

    print(schema_context)

    final_prompt = prompt.format(
        schema=schema_context,
        question=question
    )

    try:
        llm = _create_llm()
    except Exception as e:
        raise Exception(f"Failed to initialize LLM: {e}")

    try:
        response = llm.invoke(final_prompt)
    except Exception as e:
        msg = str(e)
        if "does not exist" in msg or "model" in msg:
            hint = (
                "Groq model not found or inaccessible. Set `GROQ_MODEL` to a valid "
                "model name and ensure your GROQ_API_KEY has access."
            )
            raise Exception(f"Groq API error: {msg}. {hint}")
        raise Exception(f"Groq API error: {e}")

    raw = response.content

    return raw











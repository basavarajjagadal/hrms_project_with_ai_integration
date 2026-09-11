from django.shortcuts import render
# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import sqlite3
from .query_planner import generate_query_plan

@csrf_exempt
def ai_query(request):

    question = request.GET.get("q")

    if not question:
        return JsonResponse({"error": "No question provided"})

    try:
        # Step 1: Generate plan
        plan = generate_query_plan(question)

        def clean_sql(raw_sql: str) -> str:
            return raw_sql.replace("```sql", "").replace("```", "").strip()

        plan = clean_sql(plan)
        print("PLAN:", plan)

        db_path = 'db.sqlite3'
        results = []

        try:
            # Step 2: Connect and execute
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(plan)

                # Step 3: Fetch rows
                rows = cursor.fetchall()

                # Step 4: Get column names
                columns = [col[0] for col in cursor.description] if cursor.description else []

                # Step 5: Convert to list of dicts for JSON
                results = [dict(zip(columns, row)) for row in rows]

                # Optional: print for debug
                for row in results:
                    print(row)
                    print("---------------------------------------------------")

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return JsonResponse({"error": f"Database error: {e}", "plan": plan})

        # Step 6: Format answer text (optional)
        answer_text = ""
        if results:
            # Example: join first column values
            # first_col = columns[0] if columns else None
            # if first_col:
            #     answer_text = ", ".join(str(r[first_col]) for r in results)
            # else:
            answer_text = f"{len(results)} rows returned."
        else:
            answer_text = "No results found."

        return JsonResponse({
            "question": question,
            "plan": plan,
            "results": results,
            "answer": answer_text
        })

    except Exception as e:
        print("FINAL ERROR:", str(e))
        return JsonResponse({
            "error": str(e),
            "question": question
        })




def chat_ui(request):
    return render(request, "ai_assistant/chat.html")
from datetime import date, timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

from services.ai_service import AIServiceError, generate_weekly_summary  # noqa: E402
from services.supabase_client import get_supabase  # noqa: E402

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/ai/weekly-summary", methods=["POST"])
def weekly_summary():
    user_id = (request.get_json(silent=True) or {}).get("user_id")
    if not user_id:
        return jsonify(error="Falta user_id"), 400

    try:
        sb = get_supabase()
        since = (date.today() - timedelta(days=60)).isoformat()

        habits = sb.table("habits").select("id,name").eq("user_id", user_id).execute().data
        ids = [h["id"] for h in habits]
        logs = []
        if ids:
            logs = (
                sb.table("habit_logs")
                .select("habit_id,date,completed,note")
                .in_("habit_id", ids)
                .gte("date", since)
                .execute()
                .data
            )
    except Exception as e:
        print(f"[Supabase error] {type(e).__name__}: {e}")
        return jsonify(error="No pude leer tus datos. Revisa el user_id, las tablas y tu SUPABASE_URL."), 500

    try:
        message, stats = generate_weekly_summary(habits, logs)
    except AIServiceError as e:
        return jsonify(error=str(e)), 503

    return jsonify(message=message, stats=stats)


if __name__ == "__main__":
    app.run(debug=True)
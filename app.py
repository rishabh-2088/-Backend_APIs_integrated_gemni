from flask import Flask, request, jsonify, Response
import pandas as pd
import io
import csv
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# In-memory stores
offer_data = {}
leads_data = []
scored_results = []

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Scoring thresholds
AI_SCORE_MAPPING = {
    "high": 50,
    "medium": 30,
    "low": 10
}

# -------------------- Rule-Based Scoring -------------------- #
def score_lead_rules(lead, offer):
    score = 0

    # Role relevance
    role = lead.get("role", "").lower()
    decision_maker_keywords = ["head of", "director", "vp", "chief", "founder"]
    if any(keyword in role for keyword in decision_maker_keywords):
        score += 20
    elif "senior" in role or "manager" in role:
        score += 10

    # Industry match
    lead_industry = lead.get("industry", "").lower()
    ideal_cases = [case.lower() for case in offer.get("ideal_use_cases", [])]
    if any(industry in lead_industry for industry in ideal_cases):
        score += 20

    # Data completeness
    required_fields = ["name", "role", "company", "industry", "location", "linkedin_bio"]
    if all(lead.get(field) for field in required_fields):
        score += 10

    return score

# -------------------- AI-Based Scoring -------------------- #
def score_lead_ai(lead, offer):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = (
            f"Given the following product offer and a prospect's profile, "
            f"classify the prospect's buying intent as 'High', 'Medium', or 'Low' "
            f"and provide a 1-2 sentence reasoning.\n\n"
            f"Product Offer:\n"
            f"Name: {offer.get('name')}\n"
            f"Value Propositions: {', '.join(offer.get('value_props', []))}\n"
            f"Ideal Use Cases: {', '.join(offer.get('ideal_use_cases', []))}\n\n"
            f"Prospect Profile:\n"
            f"Name: {lead.get('name')}\n"
            f"Role: {lead.get('role')}\n"
            f"Company: {lead.get('company')}\n"
            f"Industry: {lead.get('industry')}\n"
            f"Bio: {lead.get('linkedin_bio')}\n\n"
            f"Classification (High/Medium/Low) and Reasoning:"
        )

        response = model.generate_content(prompt)
        text_response = response.text.strip().lower()

        intent = "low"
        if "high" in text_response:
            intent = "high"
        elif "medium" in text_response:
            intent = "medium"

        ai_score = AI_SCORE_MAPPING[intent]
        return ai_score, response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return 0, "AI classification failed due to an error."

# -------------------- API Endpoints -------------------- #

@app.route('/offer', methods=['POST'])
def receive_offer():
    global offer_data
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        required_keys = ["name", "value_props", "ideal_use_cases"]
        if not all(key in data for key in required_keys):
            return jsonify({"error": "Missing required fields"}), 400

        offer_data = data
        return jsonify({"message": "Offer data received successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/leads/upload', methods=['POST'])
def upload_leads():
    global leads_data

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        df = pd.read_csv(io.StringIO(file.stream.read().decode('utf-8')))
        required_columns = ["name", "role", "company", "industry", "location", "linkedin_bio"]
        if not all(col in df.columns for col in required_columns):
            return jsonify({"error": "CSV is missing required columns"}), 400

        leads_data = df.to_dict('records')
        return jsonify({"message": "Leads CSV uploaded and processed successfully", "count": len(leads_data)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/score', methods=['POST'])
def score_leads():
    global scored_results

    if not offer_data or not leads_data:
        return jsonify({"error": "Offer and leads data must be uploaded first"}), 400

    scored_results = []
    for lead in leads_data:
        rule_score = score_lead_rules(lead, offer_data)
        ai_score, ai_reasoning = score_lead_ai(lead, offer_data)

        final_score = rule_score + ai_score
        intent = "High" if final_score >= 70 else "Medium" if final_score >= 40 else "Low"

        scored_results.append({
            "name": lead.get("name"),
            "role": lead.get("role"),
            "company": lead.get("company"),
            "intent": intent,
            "score": final_score,
            "reasoning": ai_reasoning
        })

    return jsonify({"message": "Scoring complete. Results are ready."}), 200


@app.route('/results', methods=['GET'])
def get_results():
    if not scored_results:
        return jsonify({"error": "No results available. Run the /score endpoint first."}), 400
    return jsonify(scored_results), 200


@app.route('/results/export', methods=['GET'])
def export_results_as_csv():
    if not scored_results:
        return jsonify({"error": "No results to export. Run the /score endpoint first."}), 400

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(scored_results[0].keys())
    for row in scored_results:
        cw.writerow(row.values())

    output = si.getvalue()
    response = Response(output, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=lead_scores.csv'
    return response

# -------------------- Run App -------------------- #

if __name__ == '__main__':
    app.run(debug=True)

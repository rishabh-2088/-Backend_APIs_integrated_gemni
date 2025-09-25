 Backend Engineer Hiring Assignment
This project is a backend service for lead qualification, scoring each lead's buying intent using a combination of rule-based logic and AI reasoning. The application is built with Flask and integrates with the Google Gemini API.

🚀 Features
Input APIs: Endpoints to accept product/offer details and a CSV file of leads.

Scoring Pipeline: A two-tiered scoring system combining a static rule layer and dynamic AI reasoning.

Output APIs: Endpoints to retrieve the final scored results as a JSON array or a downloadable CSV file.

Unit Tests: Unit tests for the rule-based scoring layer using pytest.

Dockerization: The application is containerized using Docker for easy portability and deployment.

⚙️ Setup and Installation
Clone the Repository:

Bash

git clone [https://github.com/rishabh-2088/-Backend_APIs_integrated_gemni.git]

cd Backend-Engineer-Assignment [project name]
Create and Activate a Virtual Environment:

Bash

python -m venv venv
.\venv\Scripts\Activate.ps1   # For Windows PowerShell
Install Dependencies:

Bash

pip install -r requirements.txt
Set Up API Keys:
Create a file named .env in the root directory and add your Gemini API key:

GEMINI_API_KEY="AIzaSyBgbDM9ZoHI0rtlu6yOyLRJeClam7snaIk"

Run the Application:

Bash

python app.py
The application will run on http://127.0.0.1:5000.

🐳 Docker Setup 
You can also run this application using Docker.

Build the Docker Image:

Bash

docker build -t kuvaka-tech-app .
Run the Docker Container:

Bash

docker run -p 5000:5000 -e GEMINI_API_KEY=$env:GEMINI_API_KEY kuvaka-tech-app
The application will be accessible at http://127.0.0.1:5000.

🧪 API Usage Examples (using curl.exe)
To test the full pipeline, run the following commands in sequence in a new terminal.

POST /offer: Send product/offer details.

Bash

curl.exe -X POST -H "Content-Type: application/json" -d @data/offer_payload.json http://127.0.0.1:5000/offer
POST /leads/upload: Upload a CSV file of leads.

Bash

curl.exe -X POST -F "file=@data/leads.csv" http://127.0.0.1:5000/leads/upload
POST /score: Run the scoring pipeline.

Bash

curl.exe -X POST http://127.0.0.1:5000/score
GET /results: Retrieve results as JSON.

Bash

curl.exe http://127.0.0.1:5000/results
GET /results/export: Download results as CSV.

Bash

curl.exe http://127.0.0.1:5000/results/export

🧠 Explanation of Logic and Prompts
Rule Logic: The rule-based scoring function score_lead_rules() assigns points based on predefined criteria such as role relevance (+10 or +20), industry match (+20), and data completeness (+10).

AI Prompt: The AI prompt is crafted to provide rich context to the Gemini model by including the product's name, value propositions, and ideal use cases, along with the prospect's full profile. This allows the AI to provide a nuanced intent classification and a specific reasoning.

✅ Unit Tests
To run the unit tests for the rule-based scoring layer, use the pytest command in your terminal:

Bash

pytest
This will confirm that the scoring logic is working as intended.

☁️ Deployment
Live API Base URL: [ https://backend-ap-is-integrated-gemni.vercel.app/ ]

🧑‍💻 Author
Rishabh Singh
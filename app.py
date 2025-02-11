from flask import Flask, render_template, request
import pandas as pd
import os

# Explicitly set the correct template folder path
app = Flask(__name__, template_folder="backend/templates")

# Define CSV path
csv_path = os.path.join(os.getcwd(), "MERGED_FOOD_DATA_WITH_GRAMS.csv")

# Check if the CSV file exists
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"❌ ERROR: CSV file not found at {csv_path}")

# Load CSV data
df = pd.read_csv(csv_path, encoding="utf-8")

# Determine the correct column name for food items
if "food_name" in df.columns:
    food_column = "food_name"
elif "food" in df.columns:
    food_column = "food"
else:
    raise KeyError(f"❌ ERROR: No valid 'food' column found in CSV. Available columns: {df.columns}")

# Define homepage route
@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    if request.method == "POST":
        query = request.form.get("query", "").strip().lower()
        if query:
            results = df[df[food_column].str.lower().str.contains(query, na=False)]

    return render_template("index.html", results=results)

# Run Flask app using Waitress
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)

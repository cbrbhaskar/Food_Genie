from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Define CSV path
csv_path = r"D:\Project food Genie\MERGED_FOOD_DATA_WITH_GRAMS.csv"

# Load CSV data
df = pd.read_csv(csv_path, encoding="utf-8")

# Get actual column names
actual_columns = df.columns.tolist()
print("📊 Actual Column Names in CSV:", actual_columns)

# Use the correct column name
if "food_name" in df.columns:
    food_column = "food_name"
elif "food" in df.columns:
    food_column = "food"
else:
    raise KeyError(f"❌ ERROR: No valid 'food' column found in CSV. Available columns: {df.columns}")

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    if request.method == "POST":
        query = request.form.get("query", "").strip().lower()
        if query:
            results = df[df[food_column].str.lower().str.contains(query, na=False)]
    return render_template("index.html", results=results)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)

from flask import Flask, render_template, request, send_file
import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
MODEL_FILE = "groundwater_rf_model.pkl"
PREDICTIONS_FILE = "predicted_results.csv"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def train_model(csv_file):
    """Train a Random Forest model using uploaded data."""
    df = pd.read_csv(csv_file)

    # DEBUG: Print dataset summary
    print("\n🔍 Training Dataset Summary:")
    print(df.head())

    if "Water_Level_1 (cm)" in df.columns and "Water_Level_3 (cm)" in df.columns and "Predicted_Borewell_Depth (cm)" in df.columns:
        X = df[["Water_Level_1 (cm)", "Water_Level_3 (cm)"]]
        y = df["Predicted_Borewell_Depth (cm)"]

        # Check for NaN values
        if X.isnull().sum().sum() > 0 or y.isnull().sum() > 0:
            print("\n⚠️ Warning: Dataset contains NaN values. Cleaning...")
            df = df.dropna()

        # Train Random Forest
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        with open(MODEL_FILE, "wb") as f:
            pickle.dump(model, f)

        print("\n✅ Model trained and saved!")

def predict_depth(water1, water3):
    """Predict borewell depth using the trained Random Forest model."""
    if not os.path.exists(MODEL_FILE):
        return "Model not trained yet."

    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)

    prediction = model.predict([[water1, water3]])[0]
    
    # DEBUG: Print predictions
    print(f"\n🔍 Predicting for Water1: {water1}, Water3: {water3} --> Predicted Depth: {prediction}")
    
    return round(prediction, 2)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    prediction = None

    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            if file.filename.endswith(".csv"):
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)

                train_model(file_path)
                message = "✅ Dataset uploaded and Random Forest model trained successfully!"
            else:
                message = "❌ Invalid file format. Please upload a CSV file."

        elif "water1" in request.form and "water3" in request.form:
            water1 = float(request.form["water1"])
            water3 = float(request.form["water3"])
            prediction = predict_depth(water1, water3)

            df_pred = pd.DataFrame([[water1, water3, prediction]], 
                                   columns=["Water_Level_1 (cm)", "Water_Level_3 (cm)", "Predicted_Borewell_Depth (cm)"])
            df_pred.to_csv(PREDICTIONS_FILE, index=False)

        elif "batch_file" in request.files:
            batch_file = request.files["batch_file"]
            if batch_file.filename.endswith(".csv"):
                batch_path = os.path.join(UPLOAD_FOLDER, batch_file.filename)
                batch_file.save(batch_path)

                df = pd.read_csv(batch_path)

                if "Water_Level_1 (cm)" in df.columns and "Water_Level_3 (cm)" in df.columns:
                    df["Predicted_Borewell_Depth (cm)"] = df.apply(
                        lambda row: predict_depth(row["Water_Level_1 (cm)"], row["Water_Level_3 (cm)"]), axis=1
                    )
                    df.to_csv(PREDICTIONS_FILE, index=False)
                    message = "✅ Batch predictions generated successfully!"
                else:
                    message = "❌ Invalid dataset format. Ensure it contains 'Water_Level_1 (cm)' and 'Water_Level_3 (cm)' columns."

    return render_template("index.html", message=message, prediction=prediction)

@app.route("/download")
def download():
    return send_file(PREDICTIONS_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

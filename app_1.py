import os
import pandas as pd
import folium
from flask import Flask, render_template

app = Flask(__name__)

# Define CSV file path (make sure it exists)
csv_filename = r"E:/mini proo main/miniP/map/data/borewell_data.csv"

# Define map file path inside the templates folder
map_filepath = "templates/map.html"

def create_map():
    """Function to create an interactive map with borewell data."""
    
    # Ensure the templates folder exists
    os.makedirs("templates", exist_ok=True)

    # ✅ Check if the CSV file exists before proceeding
    if not os.path.exists(csv_filename):
        raise FileNotFoundError(f"Error: The file '{csv_filename}' does not exist. Check the path.")

    # ✅ Read the CSV file with the correct variable
    df = pd.read_csv(csv_filename)

    # ✅ Strip spaces from column names
    df.columns = df.columns.str.strip()

    # ✅ Ensure the expected column exists
    expected_column = "Recommended_Borewell_Depth"
    for col in df.columns:
        if "Recommended_Borewell_Depth" in col:
            df.rename(columns={col: expected_column}, inplace=True)
            break

    if expected_column not in df.columns:
        raise KeyError(f"Missing required column: {expected_column}. Available columns: {df.columns.tolist()}")

    # ✅ Create a base map centered at a default location
    borewell_map = folium.Map(location=[17.3850, 78.4867], zoom_start=7)

    # ✅ Add markers for each borewell location
    for _, row in df.iterrows():
        lat, lon = row["Latitude"], row["Longitude"]
        depth = row[expected_column]

        popup_text = f"""
        <b>Location:</b> {row['District']}<br>
        <b>Land Type:</b> {row['Land_Type']}<br>
        <b>Recommended Borewell Depth:</b> {depth} ft
        """
        folium.Marker(
            location=[lat, lon],
            popup=popup_text,
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(borewell_map)

    # ✅ Save the map inside templates folder
    borewell_map.save(map_filepath)

@app.route("/")
def index():
    """Render the map in a Flask template."""
    create_map()
    return render_template("map.html")

if __name__ == "__main__":
    app.run(debug=True)

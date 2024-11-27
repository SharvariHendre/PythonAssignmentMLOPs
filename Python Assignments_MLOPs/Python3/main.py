import pandas as pd
import matplotlib.pyplot as plt
import os
from fastapi import FastAPI
from pydantic import BaseModel

# Define the WineDataFilter class
class WineDataFilter:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def filter_by_quality(self, quality: int):
        filtered_data = self.data[self.data['quality'] == quality]
        return filtered_data

    def visualize_feature_distribution(self, features: list, output_dir="images"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for feature in features:
            plt.figure(figsize=(8, 6))
            self.data[feature].hist(bins=20)
            plt.title(f"Distribution of {feature}")
            plt.xlabel(feature)
            plt.ylabel("Frequency")
            plt.savefig(f"{output_dir}/{feature}_distribution.png")
            plt.close()

# Create FastAPI app
app = FastAPI()

# Instantiate WineDataFilter
wine_filter = WineDataFilter("winequality-red.csv")

# Define request model for quality filtering
class WineQualityRequest(BaseModel):
    quality: int

# Endpoint to filter wine by quality
@app.post("/filter-wine")
async def filter_wine(data: WineQualityRequest):
    filtered_data = wine_filter.filter_by_quality(data.quality)
    return filtered_data.to_dict(orient="records")

# Endpoint to visualize feature distributions
@app.get("/visualize")
async def visualize_features():
    features = ['alcohol', 'pH', 'sulphates']  # List of features to visualize
    wine_filter.visualize_feature_distribution(features)
    return {"message": "Visualizations created", "files": [f"{feature}_distribution.png" for feature in features]}
import os
from flask import Flask, request, render_template
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
  context = {}
  if request.method == "POST":
    bedrooms = int(request.form["bedrooms"])
    bathrooms = int(request.form["bathrooms"])
    sqft_living = float(request.form["sqft_living"])
    sqft_lot = float(request.form["sqft_lot"])
    floors = int(request.form["floors"])
    waterfront = int(request.form["waterfront"])
    view = int(request.form["view"])

    df = pd.read_csv("Housing.csv")
    X = df[["bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "waterfront", "view"]]
    y = df["price"]
    regr = LinearRegression()
    regr.fit(X, y)
    input_data = pd.DataFrame([[bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, view]], columns=["bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "waterfront", "view"])
    predicted_price = regr.predict(input_data)
    context["prediction"] = predicted_price[0]
  return render_template("index.html", context=context)

if __name__ == "__main__":
  host = os.getenv("IP", "0.0.0.0")
  port = int(os.getenv("PORT", 5000))
  app.run(host=host, port=port)
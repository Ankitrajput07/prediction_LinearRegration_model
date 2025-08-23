from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import re
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Load dataset and train model for experience vs salary
df1 = pd.read_csv("Experience-Salary.csv")
model1 = LinearRegression()
model1.fit(df1[["exp(in months)"]], df1["salary(in thousands)"])

# Load dataset and train model for study hours vs exam score
df2 = pd.read_csv("student_scores.csv")
model2 = LinearRegression()
model2.fit(df2[['Hours']], df2['Scores'])

# --- Model 3: Car Age vs. Resale Value ---
try:
    df3 = pd.read_csv("used_car_prices.csv")

    def clean_price(price_str):
        if isinstance(price_str, str):
            cleaned_str = re.sub(r'[^\d.]', '', price_str)
            if cleaned_str:
                return float(cleaned_str)
        return np.nan

    df3['Price'] = df3['Average price'].apply(clean_price)
    df3['Model Year'] = df3['Car Model'].str.extract(r'(\b\d{4}\b)').astype(float)
    df3['Sale Year'] = pd.to_datetime(df3['Month/Year'], format='%Y-%m', errors='coerce').dt.year

    df3.dropna(subset=['Price', 'Model Year', 'Sale Year'], inplace=True)

    df3['Age'] = (df3['Sale Year'] - df3['Model Year']) + 1
    df3 = df3[df3['Age'] > 0]

    if not df3.empty:
        model3 = LinearRegression()
        model3.fit(df3[['Age']], df3['Price'])
    else:
        print("Warning: No valid data for car resale model after cleaning.")
        model3 = None

except FileNotFoundError:
    print("Warning: 'used_car_prices.csv' not found. Car resale prediction will not work.")
    model3 = None
except Exception as e:
    print(f"An error occurred while preparing the car resale model: {e}")
    model3 = None

# --- Model 4: Advertising Budget vs. Sales ---
try:
    df4 = pd.read_csv("Advertising.csv")
    # For this model, we'll create a 'Total_Budget' feature by summing the ad channels
    df4['Total_Budget'] = df4['TV'] + df4['radio'] + df4['newspaper']
    model4 = LinearRegression()
    # We will predict 'sales' based on the combined 'Total_Budget'
    model4.fit(df4[['Total_Budget']], df4['sales'])
except FileNotFoundError:
    print("Warning: 'Advertising.csv' not found. Sales prediction will not work.")
    model4 = None
except KeyError as e:
    print(f"Warning: Column error in 'Advertising.csv': {e}. Sales prediction will not work.")
    model4 = None
except Exception as e:
    print(f"An error occurred while preparing the advertising vs sales model: {e}")
    model4 = None


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/experience-salary', methods=['GET', 'POST'])
def experience_salary():
    prediction = None
    if request.method == 'POST':
        try:
            exp_months = float(request.form['experience'])
            prediction = round(model1.predict([[exp_months]])[0], 2)
        except ValueError:
            prediction = "Invalid input. Please enter a number."
    return render_template('experience_salary.html', prediction=prediction)

@app.route('/study-score', methods=['GET', 'POST'])
def study_score():
    prediction = None
    if request.method == 'POST':
        try:
            study_hours = float(request.form['study_hours'])
            prediction = round(model2.predict([[study_hours]])[0], 2)
        except ValueError:
            prediction = "Invalid input. Please enter a number."
    return render_template('study_score.html', prediction=prediction)

@app.route('/car_resale', methods=['GET', 'POST'])
def car_resale():
    """Handles car age vs. resale value prediction."""
    prediction = None
    if request.method == 'POST':
        if model3 is not None:
            try:
                car_age = float(request.form['car_age'])
                raw_prediction = model3.predict([[car_age]])[0]
                # Format the prediction as currency
                prediction = f"{raw_prediction:,.2f} EGP"
            except (ValueError, KeyError):
                prediction = "Invalid input. Please enter a number."
        else:
            prediction = "Model not available."
    return render_template('car_resale.html', prediction=prediction)

@app.route('/advertising_sales', methods=['GET', 'POST'])
def advertising_sales():
    """Handles advertising budget vs. sales prediction."""
    prediction = None
    if request.method == 'POST':
        if model4 is not None:
            try:
                total_budget = float(request.form['total_budget'])
                # The prediction will be in the same scale as the 'sales' column (e.g., thousands of units)
                raw_prediction = model4.predict([[total_budget]])[0]
                prediction = f"{raw_prediction:.2f} (in sales units)"
            except (ValueError, KeyError):
                prediction = "Invalid input. Please enter a number."
        else:
            prediction = "Model not available."
    return render_template('advertising_sales.html', prediction=prediction)



if __name__ == '__main__':
    app.run(debug=True)


# 📈 Linear Regression Model Showcase

This project is a web application that demonstrates the power of simple linear regression through four distinct prediction tools. Each tool is built using a Python Flask backend, where a machine learning model has been trained on a specific dataset to make real-world predictions. The frontend is a clean, modern interface that allows users to interact with each model.

![Image of the Linear Regression Model Showcase UI]

---

## 🚀 Features

This application includes four predictive models:

-   **Experience vs. Salary**: Predicts a potential salary based on years of professional experience.
-   **Study Hours vs. Exam Score**: Estimates a student's exam score based on the number of hours they studied.
-   **Car Age vs. Resale Value**: Determines the likely resale value of a car given its age.
-   **Advertising Budget vs. Sales**: Forecasts product sales based on the advertising budget.

---

## 🛠️ How It Works

The core of this project is the application of machine learning. For each of the four tools, a simple linear regression model was trained on a corresponding CSV dataset.

1.  **Data Loading & Preprocessing**: The Python backend, powered by the **Flask** framework, uses the **Pandas** library to load data from the `.csv` files.
2.  **Model Training**: The **Scikit-learn** library is used to build and train a unique linear regression model for each dataset.
3.  **Prediction API**: Flask exposes simple API endpoints that take a user's input.
4.  **Web Interface**: The user interacts with a clean **HTML** and **Tailwind CSS** frontend, enters a value, and the application sends a request to the backend.
5.  **Displaying Results**: The trained model processes the input and returns a prediction, which is then displayed to the user on the web page.

---

## 💻 Tech Stack

-   **Backend**: Python, Flask
-   **Machine Learning**: Scikit-learn, Pandas
-   **Frontend**: HTML, Tailwind CSS
-   **Datasets**: CSV

---

## 📂 File Structure

The project is organized as follows:

```
.
├── templates/
│   ├── advertising_sales.html
│   ├── car_resale.html
│   ├── experience_Salary.html
│   ├── index.html
│   └── study_score.html
│
├── app.py                  # Main Flask application, model training, and API logic
├── Advertising

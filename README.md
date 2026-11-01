# SupportFlow AI

A support ticket management API built with **Python, FastAPI, and SQLite**, with a Machine Learning model for automatic ticket classification.

The project started as a backend REST API and was later extended with a text classifier using **TF-IDF and Logistic Regression**.

## Features

**Ticket management**
- Create, list, update, and delete support tickets
- Store tickets in SQLite
- Validate requests with Pydantic
- Handle HTTP errors and invalid requests

**Machine Learning**
- Classify tickets based on title and description
- Predict one of four categories: `access`, `billing`, `technical_issue`, or `other`
- Use TF-IDF for text vectorization and Logistic Regression for classification
- Save and load the trained model with joblib
- Run predictions through a dedicated API endpoint

The classifier currently suggests categories without changing the tickets stored in the database.

## Tech Stack

- **Python** — Application logic
- **FastAPI** — REST API
- **SQLite** — Data storage
- **Pydantic** — Request validation
- **scikit-learn** — Text vectorization and classification
- **joblib** — Model persistence
- **Pytest** — Automated testing

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/tickets` | List all tickets |
| GET | `/tickets/{id}` | Get a ticket by ID |
| POST | `/tickets` | Create a ticket |
| PATCH | `/tickets/{id}` | Update ticket status |
| DELETE | `/tickets/{id}` | Delete a ticket |
| POST | `/tickets/classify` | Predict a ticket category |

### Classification Example

**POST `/tickets/classify`**

Request:

```json
{
  "title": "Não consigo acessar minha conta",
  "description": "Minha senha não funciona"
}
```

Response:

```json
{
  "predicted_category": "access"
}
```

This endpoint loads the trained classifier and returns a prediction without creating a ticket.

## How the Classifier Works

The classification pipeline is straightforward:

1. Combine the ticket title and description into a single text.
2. Transform the text into numerical features using a fitted TF-IDF vectorizer.
3. Pass the resulting vector to a Logistic Regression model.
4. Return the predicted category through the API.

The vectorizer and classifier are saved together using joblib, so the API can make predictions without retraining the model for every request.

### Initial Evaluation

The first version was trained on **12 labeled synthetic tickets**, with three examples per category.

I tested the model on eight additional synthetic examples that were not part of the training data.

| Metric | Result |
|---|---|
| Training samples | 12 |
| Test samples | 8 |
| Correct predictions | 6 |
| Accuracy on this test set | 75% |

**Limitations:** This is an early prototype with a very small dataset. The reported accuracy only describes this initial experiment and should not be interpreted as real-world performance.

The next step for the classifier is to expand the dataset and evaluate it on more representative support requests.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/renatocandido0/supportflow_ai.git
cd supportflow_ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Prepare the classifier

The API uses a trained model stored at:

`models/supportflow_classifier.joblib`

If the model file is not available, generate it from the training dataset:

```bash
python ml/train_model.py
```

Only load joblib model files from trusted sources.

### 5. Run the API

```bash
python -m uvicorn main:app --reload
```

Open the Swagger UI to explore and test the endpoints:

http://127.0.0.1:8000/docs

## Tests

Install the development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the tests:

```bash
python -m pytest -q
```

Latest local result:

```text
12 passed
```

The test suite covers ticket operations, request validation, error handling, and the classification endpoint. It also includes an integration test that performs a prediction using the saved model.

These tests verify application behavior; they do not measure the classifier's overall predictive performance.

## Next Steps

- Expand the training dataset and improve model evaluation
- Add AI-assisted ticket prioritization
- Prepare the application for deployment

## Status

**Version 2 — Backend API with Machine Learning classification**

The backend and classification endpoint are functional. The ML component is still experimental and will be improved as the project evolves.
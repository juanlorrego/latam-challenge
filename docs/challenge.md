# Challenge Documentation

## Overview

This document provides comprehensive documentation for the development process of the Latam Challenge. The challenge involves creating an API for predicting flight delays using FastAPI, deploying it on Google Cloud Platform (GCP), implementing CI/CD pipelines, and submitting the challenge for evaluation.

## Development Steps

### 0. Files and Model preparations

The file exploration.jpynb has been provided with the work of a Data Scientist, with predictions using XGBoost and LogisticRegression with and without balancing and top_10_features (6 models in total).

- The function sns.barplot was nos working without specifying the kwarg x and y. Was corrected by including them in the code.
- Mistakes were found in the Feature Generation (2.a Period of day): The limit were given as more o less, and must be more or equal, or less or equal.
- Mistakes were found in the Data Analysis: Second Sight (How is the delay rate across columns?): the variable rates[names] that is a percentage was calculated as round(total / delays[name]), the correct way is round(delays[name] / total, 2)*100
- Was neccesary to select one model between XGBoost and LogisticRegression, both trained with the top 10 features and class balancing. Both model present similar perfomance in the metrics. The selection must depends on other factors such as intrepetability or the trainging and prediction speed.
	- The LogisticRegression has an easier interpretability than XGBoost
	- The LogisticRegression has a training time of 0.055 seconds. XGboost has a traing time of 0.071 seconds
	- The LogisticRegression has a prediction time of 0.002 seconds. XGboost has a prediction time of 0.011 seconds
	- The LogisticRegression is the selected model.

- The exploration.jpynb original file is saved as exploration_prev.jpynb
- The current exploration.jpynb has a better coding and presentation practices.
- Some files such as model.py, api.py and data.csv were copied in other folder in order to be used by the tests.

### 1. API Development

The API was developed using FastAPI in Python. The primary files involved in this process are:

- **api.py**: Contains the FastAPI application with endpoints for health checks and flight delay predictions.

- **model.py**: Implements the DelayModel class responsible for preprocessing data, training a logistic regression model, and making predictions.

- **test_api.py**: Includes test cases for API endpoints using the FastAPI TestClient.

### 2. Model Save/Load Implementation

The `DelayModel` class now incorporates functionality for saving and loading the trained logistic regression model using the `joblib` library. The relevant changes were made in the `fit` and `predict` methods.

### 3. API Deployment on GCP

The API was deployed on GCP using the following steps:

- Created the `app.yaml` file specifying the runtime and entry point.
- Used the `gcloud app deploy` command to deploy the application to GCP App Engine.

### 4. CI/CD Implementation

The CI/CD implementation involves two YAML files:

#### ci.yml

```yaml
name: 'Continuous Integration'

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run tests
      run: |
        python -m pytest
```

#### cd.yml

```yaml
name: 'Continuous Delivery'

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Deploy to GCP
      run: |
        gcloud app deploy
```

### 5. Challenge Submission

To submit the challenge, a POST request must be made to the provided endpoint with the following JSON payload:

```json
data = {
    "name": "Juan Luis Orrego Henao",
    "mail": "juanorrego9@hotmail.com",
    "github_url": "https://github.com/juanlorrego/latam-challenge.git",
    "api_url": "https://latam-challenge-406819.rj.r.appspot.com/"
}
```

The file POST_request.jpynb was created in order to make the POST.

## Conclusion

This documentation covers the entire development process, from creating the FastAPI application to deploying it on GCP, implementing CI/CD, and preparing for submission. Each step was meticulously followed to ensure a robust and well-documented solution for the Latam Challenge.
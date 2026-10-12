# AI Based Dynamic Patient Queue And Waiting Time Prediction System

An academic full-stack project that combines a web application,
real-time queue updates, and a machine-learning model to estimate
patient waiting times.

> **Research limitation:** The current ML experiments use a synthetic
> dataset. Model metrics describe evaluation on that dataset and do not
> establish accuracy in real hospitals or clinical validation. Predicted
> waiting times are estimates, not guarantees.

## Project objectives

-   Register patients and assign queue tokens.
-   Display queue position and status.
-   Estimate patient waiting time using machine learning.
-   Update queue information in real time.
-   Provide separate workflows for patients, doctors, and staff.
-   Keep prediction, queue operations, and user access controlled by the
    backend.

## Technology stack

  -----------------------------------------------------------------------
  Component                           Technology
  ----------------------------------- -----------------------------------
  Frontend                            React

  Backend API                         Node.js, Express

  Database                            MongoDB, Mongoose

  ML service                          Python, scikit-learn and trained
                                      tree-based models

  ML API                              FastAPI, Uvicorn

  Real-time communication             Socket.IO

  Testing                             Python/pytest and backend/frontend
                                      tests as configured in the
                                      repository
  -----------------------------------------------------------------------

## Architecture

``` text
React frontend
    |
    | REST API / authenticated Socket.IO connection
    v
Node.js + Express backend
    |                    |
    |                    +---- MongoDB
    |
    +---- HTTP request ----> FastAPI ML service
                                  |
                                  +---- Saved preprocessing pipeline
                                  |
                                  +---- Saved ML model
```

The React application should communicate with the Node.js backend. The
backend coordinates database operations and calls the ML service when a
prediction is needed.

## Repository structure

The following is a representative structure. Use the actual files in the
repository as the source of truth.

``` text
dynamic-patient-queue-system/
├── backend/                 # Express API, Mongoose models, routes and middleware
├── frontend/                # React application, if present
├── ml-services/             # Python prediction module and FastAPI service
│   ├── data/
│   ├── models/
│   ├── preprocessed/
│   ├── reports/
│   ├── src/
│   ├── main.py
│   ├── test_main.py
│   └── requirements.txt
├── docs/                    # Requirements, architecture, decisions, security and test plan
├── .gitignore
└── README.md
```

## Current ML component

The reported ML workflow includes:

-   A synthetic dataset with 20,000 rows and 26 columns.
-   Preprocessing and saved feature-transformation artifacts.
-   Baseline experiments with Linear Regression, Random Forest, XGBoost,
    and LightGBM.
-   Chronological validation and evaluation reports.
-   A saved LightGBM model and Python prediction module.
-   A FastAPI service with health, prediction, and model-information
    endpoints.
-   Automated tests and verification reports.

Reported temporal validation for LightGBM: **MAE 8.01 minutes, R²
0.9451**. These results should be described as synthetic-data evaluation
results, not real-world hospital performance.

## Application functionality

The intended end-to-end workflow is:

1.  A user signs in with an authorized role.
2.  A patient is registered and assigned a queue token.
3.  The backend maintains queue ordering and status.
4.  The backend obtains an estimated waiting time from the ML service.
5.  Queue changes and predictions are persisted by the backend.
6.  Authorized clients receive real-time updates.
7.  Patients, doctors, and staff see the information relevant to their
    roles.

Features should be marked complete only after their implementation and
tests have been verified in the current repository.

## Prerequisites

Install the tools required by the parts of the project you intend to
run:

-   Git
-   Node.js and npm
-   MongoDB (local instance or a configured MongoDB deployment)
-   Python compatible with `ml-services/requirements.txt`

The backend, frontend, and ML service may have separate dependency
files. Install dependencies from each component's own directory.

## Setup

### 1. Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd dynamic-patient-queue-system
```

Replace the placeholder with your actual repository URL.

### 2. Configure environment variables

Inspect the backend's `.env.example` and create a local `.env` with your
own values. Do not commit the `.env` file.

The backend configuration may include values such as:

``` env
NODE_ENV=development
PORT=5000
MONGODB_URI=mongodb://127.0.0.1:27017/dynamic-patient-queue
JWT_SECRET=replace_with_a_secure_local_secret
JWT_EXPIRES_IN=1d
CLIENT_URL=http://localhost:5173
ML_SERVICE_URL=http://127.0.0.1:8000
CORS_ORIGIN=http://localhost:5173
```

Adjust variable names and values to match the actual backend
configuration. These are examples, not production credentials. Never use
the placeholder JWT secret in a deployed environment.

### 3. Start MongoDB

Ensure MongoDB is running and that `MONGODB_URI` points to the intended
database. Confirm the connection using the backend's existing connection
logic.

### 4. Start the ML service

In a terminal:

``` powershell
cd ml-services
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

If the virtual environment already exists, activate it rather than
creating another.

When running locally, check:

-   API root: http://127.0.0.1:8000/
-   Health check: http://127.0.0.1:8000/health
-   API documentation: http://127.0.0.1:8000/docs

### 5. Start the backend

Open another terminal:

``` powershell
cd backend
npm install
npm run dev
```

Use the scripts listed in `backend/package.json`; if `dev` is not
defined, use the configured start script.

### 6. Start the frontend

If a frontend directory exists, open another terminal:

``` powershell
cd frontend
npm install
npm run dev
```

Use the scripts defined in the actual frontend `package.json`. The
development URL is shown by the frontend tool.

## Testing

Run tests from each component using its configured test commands.

### ML service

From `ml-services`:

``` powershell
python -m pytest test_main.py -v
```

If present, the prediction verification script can also be run:

``` powershell
python verify_prediction_module.py
```

### Backend and frontend

Inspect their `package.json` scripts and run the configured test, lint,
and build commands. Do not report tests as passing unless they were
executed successfully.

## API and real-time design

The intended backend responsibilities include:

-   Authentication and role-based authorization.
-   Patient and doctor records.
-   Token assignment and queue-state transitions.
-   Calling the ML service and validating prediction responses.
-   Persisting queue changes and estimated waiting times.
-   Publishing authorized Socket.IO events after successful database
    changes.

The ML service should not be called directly by the React frontend. It
should receive only the features supported by the saved preprocessing
pipeline; never send the target `waiting_time_minutes` as an input or
use `previous_patient_service_time` as a prediction feature.

## Security and data handling

-   Keep `.env`, credentials, tokens, and private keys out of Git.
-   Commit `.env.example` only when it contains placeholders.
-   Enforce authorization on the backend and on Socket.IO room
    subscriptions.
-   Validate all incoming data on the server.
-   Do not expose password hashes, secrets, stack traces, or unnecessary
    patient information.
-   Review large model and dataset files before pushing to GitHub.
-   Do not commit virtual environments, `node_modules`, caches, or
    generated build directories.
-   Follow `docs/SECURITY.md` and the current project decisions.

## Limitations

-   The ML model was evaluated on synthetic data, not real hospital
    records.
-   Results may not generalize to real-world queue behavior.
-   Predictions are estimates and can be wrong.
-   The project does not diagnose conditions, prescribe treatment, or
    make clinical decisions.
-   Do not claim clinical validation, production readiness, or
    guaranteed waiting-time accuracy.

## Project documentation

Review the `docs/` directory for the project requirements, architecture,
design decisions, implementation rules, security requirements, test
plan, task tracking, and current project state. Consult those documents
before changing the architecture or adding features.

## Contributing and development workflow

1.  Inspect the existing implementation before creating new files.
2.  Work on one phase at a time.
3.  Reuse existing models, services, and test helpers.
4.  Run relevant tests after changes.
5.  Update documentation when behavior or configuration changes.
6.  Review `git status` before committing.
7.  Never commit `.env` or other secrets.

## License

Add a license file if you intend to publish or distribute this project.
Until a license is included, do not assume others have permission to
reuse it.

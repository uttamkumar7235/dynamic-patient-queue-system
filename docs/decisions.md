# Architecture Decisions

## AI-Based Dynamic Patient Queue and Waiting Time Prediction System

**Document Version:** 1.0\
**Status:** Active\
**Purpose:** Source of truth for important technical and architectural
decisions.

------------------------------------------------------------------------

# 1. Purpose of This Document

This document records important technical decisions made for the
project.

These decisions should be treated as the project's **source of truth**.

Future implementation should follow these decisions unless a new
decision is explicitly added to this document.

The purpose is to prevent:

-   Random technology changes
-   Unnecessary architecture changes
-   Inconsistent implementation
-   Repeated discussions about already-settled decisions
-   AI-generated code from changing the project's technical direction
    without approval

------------------------------------------------------------------------

# 2. Decision Rules

1.  Existing decisions must not be changed silently.
2.  A technology should not be replaced just because another technology
    is available.
3.  New architectural decisions must be added as a new ADR.
4.  Existing ADRs should remain unchanged unless they are explicitly
    superseded.
5.  If a new requirement conflicts with an existing decision, explain
    the conflict before changing the architecture.
6.  The simplest solution that satisfies the project requirements should
    be preferred.
7.  The project must remain consistent with the approved PRD,
    architecture, design, and rules documents.

------------------------------------------------------------------------

# 3. ADR-001 --- Use MERN Stack for the Main Web Application

**Status:** Accepted

## Decision

Use the **MERN stack** as the primary technology stack for the web
application.

``` text
MongoDB
Express.js
React.js
Node.js
```

## Reason

The project requires:

-   A responsive web frontend
-   REST APIs
-   Database interaction
-   Queue management
-   Authentication
-   Real-time communication
-   A maintainable JavaScript-based application

MERN provides a consistent JavaScript/Node.js ecosystem for the main web
application.

## Consequences

### Positive

-   One primary language across frontend and backend.
-   Large ecosystem.
-   Good support for REST APIs.
-   React provides component-based UI development.
-   MongoDB integrates naturally with Node.js through Mongoose.

### Negative

-   The ML component still requires a separate Python service.
-   The team must maintain both JavaScript and Python environments.

------------------------------------------------------------------------

# 4. ADR-002 --- Use React for the Frontend

**Status:** Accepted

## Decision

Use **React.js** for the frontend.

## Reason

The application contains multiple interactive interfaces:

-   Patient registration
-   Patient dashboard
-   Doctor dashboard
-   Staff dashboard
-   Queue status
-   Real-time updates

React's component-based architecture is suitable for these interfaces.

## Consequences

Frontend code will be organized around reusable React components.

Examples:

``` text
QueueCard
TokenCard
StatusBadge
DoctorDashboard
PatientDashboard
```

------------------------------------------------------------------------

# 5. ADR-003 --- Use Node.js and Express.js for the Backend

**Status:** Accepted

## Decision

Use **Node.js + Express.js** as the main backend.

## Reason

The backend needs to handle:

-   REST APIs
-   Authentication
-   Authorization
-   Queue business logic
-   MongoDB operations
-   Socket.io communication
-   Communication with the Python ML service

Node.js provides a suitable runtime, while Express.js provides a
lightweight API framework.

## Consequences

The Node.js backend will act as the **central application coordinator**.

``` text
React
  ↓
Node.js + Express
  ↓
MongoDB / ML Service
```

------------------------------------------------------------------------

# 6. ADR-004 --- Use MongoDB as the Primary Database

**Status:** Accepted

## Decision

Use **MongoDB** as the primary application database.

## Reason

The application contains document-oriented entities such as:

-   Users
-   Patients
-   Doctors
-   Queue entries

MongoDB provides flexible document storage and integrates well with
Node.js through Mongoose.

## Consequences

The main application data will be persisted in MongoDB.

The React frontend must not access MongoDB directly.

``` text
React
  ↓
Express Backend
  ↓
Mongoose
  ↓
MongoDB
```

------------------------------------------------------------------------

# 7. ADR-005 --- Use Mongoose for MongoDB Interaction

**Status:** Accepted

## Decision

Use **Mongoose** as the MongoDB object modeling library.

## Reason

Mongoose provides:

-   Schema definitions
-   Validation
-   Model abstraction
-   MongoDB references
-   Query support

## Consequences

MongoDB schemas should be defined through Mongoose models in the Node.js
backend.

------------------------------------------------------------------------

# 8. ADR-006 --- Use Socket.io for Real-Time Queue Updates

**Status:** Accepted

## Decision

Use **Socket.io** for real-time communication.

## Reason

Patient queues can change frequently.

Examples:

-   New patient joins.
-   Patient is called.
-   Consultation starts.
-   Consultation completes.
-   Patient cancels.
-   Doctor availability changes.
-   Waiting-time prediction changes.

Manual page refreshes would provide a poor user experience.

## Consequences

Socket.io will be used for real-time events such as:

``` text
patient:registered
queue:updated
patient:called
consultation:started
consultation:completed
patient:cancelled
doctor:availabilityChanged
prediction:updated
```

REST APIs will still be used for normal CRUD and initial data retrieval.

------------------------------------------------------------------------

# 9. ADR-007 --- Use REST APIs Alongside Socket.io

**Status:** Accepted

## Decision

Use both:

``` text
REST API
+
Socket.io
```

## Reason

REST is appropriate for:

-   Registration
-   Login
-   Retrieving data
-   Updating resources
-   Standard CRUD operations

Socket.io is appropriate for:

-   Live queue updates
-   Real-time status changes
-   Real-time prediction updates

## Consequences

The application follows:

``` text
REST API
    ↓
Initial/standard data

Socket.io
    ↓
Live changes
```

Socket.io should not unnecessarily replace REST APIs.

------------------------------------------------------------------------

# 10. ADR-008 --- Use Python for Machine Learning

**Status:** Accepted

## Decision

Use **Python** for the machine learning component.

## Reason

Python provides a mature machine learning ecosystem, including:

-   Pandas
-   NumPy
-   Scikit-learn
-   XGBoost
-   LightGBM
-   Joblib
-   SHAP

The project requires training and serving a waiting-time prediction
model.

## Consequences

The project will contain a separate Python ML component.

The main application remains MERN-based.

------------------------------------------------------------------------

# 11. ADR-009 --- Keep the ML Component as a Separate Service

**Status:** Accepted

## Decision

The machine learning prediction component will be separated from the
Node.js backend.

Architecture:

``` text
React
  ↓
Node.js + Express
  ↓
Python ML API
  ↓
Trained Model
```

## Reason

The Python ML ecosystem is different from the Node.js application
ecosystem.

A separate service provides:

-   Clear separation of responsibilities
-   Easier ML development
-   Independent model updates
-   Cleaner backend architecture
-   Easier testing

## Consequences

The Node.js backend communicates with the Python service through an API.

The React frontend does not directly communicate with the ML service.

------------------------------------------------------------------------

# 12. ADR-010 --- Use FastAPI or Flask for the Python Prediction API

**Status:** Accepted

## Decision

The Python ML service may use **FastAPI or Flask**.

The final framework can be selected during implementation based on
project requirements.

## Reason

Both frameworks can expose the trained model through a lightweight HTTP
API.

Example:

``` text
POST /predict
```

## Consequences

The ML service must maintain a stable API contract regardless of the
selected Python web framework.

------------------------------------------------------------------------

# 13. ADR-011 --- Use a Synthetic Dataset

**Status:** Accepted

## Decision

Use a **synthetic dataset** for machine learning development and
evaluation.

## Reason

The project is an academic prototype and does not rely on real hospital
patient data.

Using synthetic data avoids representing real patient information as
project training data.

## Consequences

All reports and presentations must clearly state that:

-   The dataset is synthetic.
-   Model results are experimental.
-   Results are not clinical validation.
-   Synthetic-data performance should not be presented as real hospital
    performance.

------------------------------------------------------------------------

# 14. ADR-012 --- ML Target Is Waiting Time

**Status:** Accepted

## Decision

The machine learning model will predict **patient waiting time in
minutes**.

## Reason

Waiting-time prediction is the core AI functionality of the project.

The model is not intended to perform medical diagnosis or treatment
recommendation.

## Consequences

The ML target variable should represent waiting time.

The application should display the output as:

``` text
Estimated Waiting Time
```

or

``` text
Predicted Waiting Time
```

------------------------------------------------------------------------

# 15. ADR-013 --- Use Regression Models for Waiting-Time Prediction

**Status:** Accepted

## Decision

Treat waiting-time prediction as a **regression problem**.

Candidate models include:

``` text
Linear Regression
Random Forest Regressor
XGBoost Regressor
LightGBM Regressor
```

## Reason

Waiting time is a continuous numerical value.

For example:

``` text
10 minutes
23 minutes
47 minutes
```

This is naturally represented as a regression target.

## Consequences

Evaluation may use:

-   MAE
-   MSE
-   RMSE
-   R² Score

------------------------------------------------------------------------

# 16. ADR-014 --- Select the Final ML Model Based on Evaluation

**Status:** Accepted

## Decision

Do not assume a particular model is the final model before evaluation.

The final model will be selected after comparing candidate models using
documented evaluation results.

## Reason

Different models may behave differently depending on the synthetic
dataset.

## Consequences

The project may experiment with:

``` text
Linear Regression
Random Forest
XGBoost
LightGBM
```

The selected model and reasoning should be documented after
experimentation.

------------------------------------------------------------------------

# 17. ADR-015 --- Do Not Retrain the Model During Prediction Requests

**Status:** Accepted

## Decision

Training and prediction must be separate processes.

``` text
Training
   ↓
Saved Model
   ↓
Prediction Service
   ↓
Predictions
```

## Reason

Training a model for every patient request would be inefficient and
architecturally incorrect for the intended workflow.

## Consequences

The prediction service should load the trained model and use it for
inference.

------------------------------------------------------------------------

# 18. ADR-016 --- Use Joblib for Python Model Serialization Where Appropriate

**Status:** Accepted

## Decision

Use **Joblib** for serializing compatible Python/scikit-learn models
where appropriate.

Example:

``` text
model.pkl
```

## Reason

Joblib is commonly used for persisting Python machine learning models
and preprocessing objects.

## Consequences

The ML service must load the saved model during startup or
initialization.

------------------------------------------------------------------------

# 19. ADR-017 --- Use Server-Side Queue Management

**Status:** Accepted

## Decision

Queue state must be controlled by the backend.

The frontend must not directly determine or modify authoritative queue
state.

## Reason

Queue state affects:

-   Token order
-   Patient position
-   Consultation status
-   Waiting-time prediction

These values must be controlled centrally.

## Consequences

The backend is responsible for validating queue transitions.

Example:

``` text
WAITING
   ↓
CALLED
   ↓
IN_CONSULTATION
   ↓
COMPLETED
```

------------------------------------------------------------------------

# 20. ADR-018 --- Use Registration Order for the Initial Queue

**Status:** Accepted

## Decision

The initial queue will generally follow patient registration/queue-entry
order for a selected doctor.

Example:

``` text
Token 101
Token 102
Token 103
```

## Reason

A simple deterministic queue is easier to implement, test, explain, and
demonstrate.

## Consequences

Advanced prioritization is outside the initial MVP unless explicitly
added through a new decision.

------------------------------------------------------------------------

# 21. ADR-019 --- Use Role-Based Access Control

**Status:** Accepted

## Decision

The system will support role-based access.

Initial roles:

``` text
PATIENT
DOCTOR
STAFF
```

## Reason

Different users require different permissions.

Examples:

``` text
Patient → View own queue
Doctor  → Manage consultation queue
Staff   → Operational queue functions
```

## Consequences

Authorization must be enforced on the backend, not only by hiding
frontend pages.

------------------------------------------------------------------------

# 22. ADR-020 --- Use Basic Authentication with Secure Password Handling

**Status:** Accepted

## Decision

The application will implement authentication using secure password
hashing and an appropriate session/JWT-based authentication mechanism.

## Reason

Protected dashboards and APIs require authenticated users.

Passwords must never be stored as plain text.

## Consequences

Authentication secrets must be stored in environment variables.

------------------------------------------------------------------------

# 23. ADR-021 --- Use Environment Variables for Secrets

**Status:** Accepted

## Decision

Sensitive configuration must be stored using environment variables.

Examples:

``` text
MONGODB_URI
JWT_SECRET
ML_SERVICE_URL
CLIENT_URL
API_KEYS
```

## Reason

Secrets must not be hard-coded into source code or committed to GitHub.

## Consequences

The project should include:

``` text
.env
.env.example
```

`.env` must be included in `.gitignore`.

------------------------------------------------------------------------

# 24. ADR-022 --- Use Layered Backend Architecture

**Status:** Accepted

## Decision

The backend will use a modular layered structure:

``` text
Routes
   ↓
Controllers
   ↓
Services
   ↓
Models / External Services
```

Supporting layers:

``` text
Middleware
Utilities
Socket Handlers
```

## Reason

This improves:

-   Maintainability
-   Testability
-   Readability
-   Separation of concerns

## Consequences

Business logic should not be unnecessarily placed directly inside route
definitions.

------------------------------------------------------------------------

# 25. ADR-023 --- React Must Not Access MongoDB Directly

**Status:** Accepted

## Decision

The frontend must communicate with MongoDB only through the backend API.

## Reason

Direct database access from the browser would expose database
credentials and bypass backend validation and authorization.

Correct:

``` text
React
  ↓
Express API
  ↓
MongoDB
```

Incorrect:

``` text
React
  ↓
MongoDB
```

------------------------------------------------------------------------

# 26. ADR-024 --- Queue Predictions Must Be Dynamic

**Status:** Accepted

## Decision

Waiting-time predictions should be recalculated when important queue
conditions change.

Examples:

``` text
New patient
Patient completed
Patient cancelled
Doctor availability changed
Relevant consultation state changed
```

## Reason

A static prediction becomes less useful as the queue changes.

## Consequences

The backend should trigger the prediction workflow after relevant queue
events.

------------------------------------------------------------------------

# 27. ADR-025 --- Display Waiting Time as an Estimate

**Status:** Accepted

## Decision

The application will display ML output as an estimate rather than a
guaranteed time.

Preferred:

``` text
Estimated waiting time: 38 minutes
```

## Reason

Machine learning predictions contain uncertainty and actual consultation
duration may vary.

## Consequences

The UI and documentation should not promise an exact consultation time
based only on the prediction.

------------------------------------------------------------------------

# 28. ADR-026 --- No Clinical Decision-Making

**Status:** Accepted

## Decision

The system will not provide:

-   Medical diagnosis
-   Treatment recommendations
-   Prescription recommendations
-   Clinical decision support

## Reason

The project's scope is patient queue and waiting-time prediction.

## Consequences

Any future healthcare-related feature must not expand the system into
clinical decision-making without a separate approved architectural and
project-scope decision.

------------------------------------------------------------------------

# 29. ADR-027 --- No Real Hospital Integration in the Initial Version

**Status:** Accepted

## Decision

The initial project will not integrate with real hospital information
systems.

## Reason

The project is an academic prototype with limited scope and uses
synthetic data.

## Consequences

The system will demonstrate the workflow using its own database and
synthetic data.

Real hospital integration is a potential future enhancement.

------------------------------------------------------------------------

# 30. ADR-028 --- Use Responsive Web Design

**Status:** Accepted

## Decision

The React application must support:

``` text
Mobile
Tablet
Laptop
Desktop
```

## Reason

Patients may access the queue interface from different devices.

## Consequences

Important information should remain easy to understand on small screens.

------------------------------------------------------------------------

# 31. ADR-029 --- REST for Standard CRUD, Socket.io for Live Updates

**Status:** Accepted

## Decision

Use:

``` text
REST → Standard data operations
Socket.io → Real-time events
```

## Reason

This provides a clear division of responsibilities.

Examples:

``` text
POST /api/patients
GET /api/queue/:doctorId
PATCH /api/queue/:id/status
```

for standard operations.

Socket.io handles:

``` text
queue:updated
prediction:updated
patient:called
```

for live updates.

------------------------------------------------------------------------

# 32. ADR-030 --- Keep the MVP Focused

**Status:** Accepted

## Decision

The initial MVP will focus on:

1.  Patient registration
2.  Doctor selection
3.  Token generation
4.  Queue management
5.  Patient dashboard
6.  Doctor dashboard
7.  Waiting-time prediction
8.  Socket.io real-time updates
9.  MongoDB persistence
10. Authentication/authorization
11. Responsive UI

## Reason

The project has a limited academic development timeline.

## Consequences

Optional features such as SMS, mobile applications, advanced analytics,
and hospital integration should not delay the core MVP.

------------------------------------------------------------------------

# 33. ADR-031 --- Use Synthetic Data Limitations in Academic Reporting

**Status:** Accepted

## Decision

All ML results must be presented in the context of the synthetic
dataset.

## Reason

Synthetic data may not represent real-world hospital queue behavior.

## Consequences

Reports and presentations should distinguish:

``` text
Experimental ML Performance
```

from:

``` text
Real-World Clinical Performance
```

------------------------------------------------------------------------

# 34. ADR-032 --- Documentation Is Part of the Architecture

**Status:** Accepted

## Decision

Important architecture and technical decisions must be documented.

Core documentation:

``` text
prd.md
architecture.md
design.md
rules.md
tasks.md
decisions.md
```

## Reason

The project involves multiple technologies and development stages.
Written decisions reduce inconsistency.

## Consequences

When a significant technical decision changes, this document should be
updated.

------------------------------------------------------------------------

# 35. ADR-033 --- Do Not Change Accepted Decisions Silently

**Status:** Accepted

## Decision

An accepted architectural decision must not be replaced silently.

If a change is necessary:

1.  Identify the existing ADR.
2.  Explain why it no longer satisfies the requirement.
3.  Create a new ADR.
4.  Mark the old ADR as superseded if appropriate.
5.  Document the migration impact.

## Example

``` text
ADR-001
MERN Stack
     ↓
New Requirement
     ↓
ADR-034
New Architecture
     ↓
ADR-001 marked SUPSERSEDED
```

The typo-free status value should be:

``` text
SUPERSEDED
```

------------------------------------------------------------------------

# 36. ADR-034 --- Use This Document as the Technical Source of Truth

**Status:** Accepted

## Decision

`decisions.md` is the authoritative record of important technical
decisions for this project.

## Reason

AI-assisted development can otherwise introduce inconsistent
technologies, libraries, architecture patterns, or workflows.

## Consequences

Before making a significant technical change, check this document.

If the proposed change conflicts with an accepted decision, the change
should not be made automatically.

A new ADR should be created when the architecture genuinely needs to
change.

------------------------------------------------------------------------

# 37. How to Add a New Decision

Use this template:

``` markdown
## ADR-XXX — Decision Title

**Status:** Proposed / Accepted / Superseded / Rejected

## Decision

Describe the decision.

## Reason

Explain why the decision was made.

## Alternatives Considered

List important alternatives if relevant.

## Consequences

### Positive

- Benefit 1
- Benefit 2

### Negative

- Trade-off 1
- Trade-off 2
```

------------------------------------------------------------------------

# 38. Decision Status Definitions

  Status       Meaning
  ------------ ---------------------------------
  Proposed     Under consideration
  Accepted     Approved and should be followed
  Rejected     Considered but not selected
  Superseded   Replaced by a newer decision

------------------------------------------------------------------------

# 39. Current Technology Baseline

The currently approved technology baseline is:

  Area                  Decision
  --------------------- ------------------------------------------------
  Frontend              React.js
  Main Backend          Node.js + Express.js
  Database              MongoDB
  ODM                   Mongoose
  Real-Time             Socket.io
  ML Language           Python
  ML API                FastAPI or Flask
  ML Libraries          Scikit-learn, XGBoost and/or LightGBM
  Model Serialization   Joblib where appropriate
  Dataset               Synthetic
  Authentication        Secure password hashing + session/JWT approach
  Architecture          Modular layered client-server architecture
  Queue                 Server-controlled registration-order queue
  ML Target             Waiting time in minutes
  Main AI Function      Waiting-time prediction

------------------------------------------------------------------------

# 40. Final Architecture Rule

The approved architecture is:

``` text
                    USERS
                      |
                      v
              +---------------+
              | React Frontend|
              +-------+-------+
                      |
               REST + Socket.io
                      |
                      v
              +---------------+
              | Node + Express|
              | Main Backend  |
              +---+-------+---+
                  |       |
                  |       |
                  v       v
             +--------+  +-----------+
             | MongoDB|  | Python ML |
             |        |  | Service   |
             +--------+  +-----+-----+
                               |
                               v
                         Trained Model
```

This architecture should remain unchanged unless an explicit new ADR is
created and accepted.

------------------------------------------------------------------------

# 41. Final Principle

> **Do not change an established technical decision just because another
> technology appears newer, easier, or more popular. Change the
> architecture only when there is a clear project requirement,
> documented technical reason, and an approved new decision.**

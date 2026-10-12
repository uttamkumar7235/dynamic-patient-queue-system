# Project Memory

## Current Project

**Project Title:** AI Based Dynamic Patient Queue And Waiting Time
Prediction System

**Purpose:** Build a web-based patient queue system that assigns tokens,
tracks queue status in real time, and predicts estimated patient waiting
time using a machine learning model.

**Technology Baseline:** - Frontend: React - Backend: Node.js +
Express - Database: MongoDB + Mongoose - Real-time communication:
Socket.io - ML service: Python - ML API: FastAPI or Flask - ML
libraries: scikit-learn, XGBoost, LightGBM - Model serialization: Joblib

**Dataset:** Synthetic dataset only.

------------------------------------------------------------------------

## Current Status

The project is in the early development stage.

### Completed

-   Project topic finalized.
-   Project requirements identified.
-   Main features identified.
-   MERN stack selected.
-   Socket.io selected for real-time queue updates.
-   Python selected for the ML component.
-   MongoDB selected for application data.
-   Basic system workflow planned.
-   Database requirements and initial schema planned.
-   ML-based waiting-time prediction approach identified.
-   Synthetic dataset approach finalized.
-   Project documentation structure created.
-   Product Requirements Document created.
-   System Architecture document created.
-   System Design document created.
-   Development Rules document created.
-   Task Plan document created.
-   Technical Decisions / ADR document created.

### Current Progress

Approximately **10% complete**.

The project is moving from planning/documentation into implementation.

------------------------------------------------------------------------

## Current Task

**Primary Phase:** Backend and database implementation.

**Current Focus:** 1. Set up the backend project. 2. Configure MongoDB
connection. 3. Create Mongoose models. 4. Implement authentication and
authorization structure. 5. Implement patient registration. 6. Implement
doctor data and availability. 7. Implement queue creation and token
generation. 8. Prepare queue status transition logic. 9. Prepare the API
structure for later Socket.io integration.

------------------------------------------------------------------------

## Current Database State

### Doctors

Planned fields:

``` js
{
  _id: ObjectId,
  name: String,
  department: String,
  avgConsultTime: Number,
  isAvailable: Boolean,
  shiftStart: String,
  shiftEnd: String
}
```

### Patients

Planned fields:

``` js
{
  _id: ObjectId,
  name: String,
  age: Number,
  gender: String,
  contact: String,
  registeredAt: Date
}
```

### Queue

Planned fields:

``` js
{
  _id: ObjectId,
  patientId: ObjectId,
  doctorId: ObjectId,
  tokenNumber: Number,
  status: String,
  queuePosition: Number,
  predictedWaitTime: Number,
  joinedAt: Date,
  consultationStartedAt: Date,
  consultationCompletedAt: Date
}
```

### Users

Authentication-related users are expected to contain fields such as:

``` js
{
  _id: ObjectId,
  name: String,
  email: String,
  passwordHash: String,
  role: String
}
```

------------------------------------------------------------------------

## Queue Status

The main queue flow is:

``` text
WAITING
   ↓
CALLED
   ↓
IN_CONSULTATION
   ↓
COMPLETED
```

Alternative exits:

``` text
WAITING → CANCELLED
WAITING → NO_SHOW
```

The queue remains server-controlled. The frontend must not directly
modify queue data in MongoDB.

------------------------------------------------------------------------

## ML Status

### Goal

Predict the estimated waiting time for a patient.

### Planned Input Features

Potential features include:

-   Number of patients ahead
-   Current queue length
-   Average consultation time
-   Doctor availability
-   Current consultation state
-   Registration/arrival-related information
-   Other features supported by the final synthetic dataset

The final feature set will be decided after dataset analysis.

### Prediction Example

Request:

``` json
{
  "patientsAhead": 5,
  "queueLength": 8,
  "avgConsultTime": 12,
  "doctorAvailable": 1
}
```

Response:

``` json
{
  "predictedWaitTime": 58
}
```

The prediction represents an **estimated waiting time**, not a
guaranteed consultation time.

### ML Architecture

``` text
Node.js / Express Backend
          ↓
     Python ML API
          ↓
     Trained Model
          ↓
 Predicted Waiting Time
          ↓
 MongoDB / Queue Update
          ↓
 Socket.io Real-Time Update
```

The model will be trained separately and loaded for prediction. It will
not be retrained for every prediction request.

------------------------------------------------------------------------

## API Structure

Planned REST endpoints include:

### Authentication

``` text
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
```

### Patients

``` text
POST /api/patients
GET  /api/patients/:id
```

### Doctors

``` text
GET   /api/doctors
GET   /api/doctors/:id
PATCH /api/doctors/:id/availability
```

### Queue

``` text
POST  /api/queue
GET   /api/queue/:doctorId
PATCH /api/queue/:id/status
GET   /api/queue/:id/prediction
```

### ML Service

Example:

``` text
POST /predict
```

The exact API implementation may evolve during development, but changes
must follow the documented architecture and decisions.

------------------------------------------------------------------------

## Real-Time Communication

Socket.io will be used for live queue updates.

Planned events include:

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

The backend controls when these events are emitted.

------------------------------------------------------------------------

## Frontend Status

Frontend implementation is not yet complete.

Planned pages/components include:

-   Login/Register
-   Patient registration
-   Doctor selection
-   Patient queue status
-   Doctor dashboard
-   Queue display
-   Waiting-time display
-   Responsive navigation
-   Loading and error states

The React frontend will communicate with the backend through APIs and
Socket.io.

------------------------------------------------------------------------

## Authentication

Authentication is planned but implementation is still pending.

Expected requirements:

-   Secure password hashing
-   Login/logout
-   Role-based authorization
-   Protected routes
-   Environment variables for secrets
-   Server-side authorization checks

Possible roles include:

``` text
PATIENT
DOCTOR
ADMIN
```

Exact role permissions will be implemented according to the project
requirements.

------------------------------------------------------------------------

## Important Constraints

-   Use a **synthetic dataset** for ML development.
-   Do not claim real hospital data.
-   Do not claim clinical validation.
-   Do not present predictions as guaranteed waiting times.
-   Do not add real hospital integrations in the initial MVP.
-   Do not allow the frontend to directly access MongoDB.
-   Do not silently replace the selected technology stack.
-   Do not introduce unnecessary technologies without documenting the
    reason.
-   Keep the initial implementation focused on the MVP.
-   The project should remain responsive for desktop and mobile screens.
-   The word **"management"** should not be used in the project/report
    terminology.

------------------------------------------------------------------------

## Known Limitations

-   The ML model depends on the quality and representativeness of the
    synthetic dataset.
-   Synthetic data may not accurately represent real healthcare queue
    behavior.
-   Waiting-time predictions are estimates.
-   The initial system is not clinically validated.
-   The project currently focuses on a controlled MVP rather than real
    hospital deployment.
-   Advanced features such as SMS/email notifications, multi-location
    support, continuous retraining, and external hospital-system
    integration are future enhancements.

------------------------------------------------------------------------

## Known Issues

-   Frontend implementation is still pending.
-   Backend APIs are not fully implemented.
-   MongoDB schema needs to be converted from the planned design into
    working Mongoose models.
-   Queue transition logic needs implementation and testing.
-   ML dataset still needs detailed analysis and preprocessing.
-   Final ML model has not yet been selected.
-   Socket.io integration is pending.
-   End-to-end testing is pending.
-   Deployment configuration is pending.

------------------------------------------------------------------------

## Next Steps

### Immediate

1.  Initialize backend structure.
2.  Configure environment variables.
3.  Connect MongoDB.
4.  Create User, Doctor, Patient, and Queue models.
5.  Add validation and error-handling middleware.
6.  Implement authentication.
7.  Implement patient registration.
8.  Implement doctor APIs.
9.  Implement queue/token APIs.

### After Backend Foundation

1.  Implement queue status transitions.
2.  Add Socket.io.
3.  Build patient and doctor dashboards.
4.  Prepare the synthetic ML dataset.
5.  Perform data preprocessing and feature analysis.
6.  Train candidate regression models.
7.  Evaluate models.
8.  Select the final model based on documented evaluation results.
9.  Create the Python ML API.
10. Integrate predictions with the Node.js backend.
11. Connect prediction updates to Socket.io.
12. Test the complete workflow.

------------------------------------------------------------------------

## Current Architecture Snapshot

``` text
                    React Frontend
                          |
                 REST API + Socket.io
                          |
                    Node.js/Express
                     /           \
                    /             \
               MongoDB        Python ML API
                                  |
                           Trained ML Model
```

### Data Flow

``` text
Patient Registration
        ↓
Token Generation
        ↓
Queue Stored in MongoDB
        ↓
Waiting Time Prediction
        ↓
Queue Status Changes
        ↓
Socket.io Broadcast
        ↓
Patient / Doctor Dashboard Updated
```

------------------------------------------------------------------------

## Source of Truth

Use the project documentation in this order:

1.  **DECISIONS.md** --- permanent technical decisions.
2.  **MEMORY.md** --- current project state.
3.  **TASKS.md** --- implementation task plan.
4.  **ARCHITECTURE.md** --- system architecture.
5.  **DESIGN.md** --- detailed system design.
6.  **RULES.md** --- development and project rules.
7.  **PRD.md** --- product requirements.

If the current state changes, update **MEMORY.md**.

If a permanent technical decision changes, update **DECISIONS.md** and
then update **MEMORY.md** if the current state is affected.

------------------------------------------------------------------------

## Update Rule

`MEMORY.md` should describe **what is true now**, not every decision
ever made.

Keep it updated when:

-   A major task is completed.
-   A new task becomes the current focus.
-   A known issue is fixed or discovered.
-   The project moves to another development phase.
-   The database/API architecture changes according to an approved
    decision.
-   The ML model or dataset status changes.
-   A major integration is completed.

Do not use `MEMORY.md` to silently change permanent architecture
decisions. Permanent changes belong in `DECISIONS.md`.

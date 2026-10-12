# System Architecture Document

## AI-Based Dynamic Patient Queue and Waiting Time Prediction System

**Document Version:** 1.0\
**Project Type:** Final Year Project\
**Architecture Style:** Modular Client-Server Architecture\
**Primary Stack:** MERN + Socket.io + Python ML Service\
**Database:** MongoDB\
**Dataset:** Synthetic Dataset

------------------------------------------------------------------------

## 1. Architecture Overview

The system uses a modular architecture that separates the application
into four major layers:

1.  **Frontend Layer** --- React-based user interfaces.
2.  **Backend Layer** --- Node.js and Express.js APIs, authentication,
    queue logic, and Socket.io.
3.  **Data Layer** --- MongoDB for persistent application data.
4.  **Machine Learning Layer** --- Python-based prediction service for
    waiting-time estimation.

The architecture is designed so that the frontend does not directly
access MongoDB or the ML model. All application operations are
coordinated through the backend.

``` text
                         USERS
                +----------------------+
                |                      |
          +-----v-----+          +-----v------+
          |  Patient  |          | Doctor /   |
          |           |          | Staff      |
          +-----+-----+          +-----+------+
                |                      |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |    React Frontend    |
                | Patient / Doctor UI  |
                +----------+-----------+
                           |
                REST API + Socket.io
                           |
                           v
                +----------------------+
                | Node.js + Express.js |
                |    Backend Server    |
                +----+------------+----+
                     |            |
          +----------+            +-----------+
          |                                   |
          v                                   v
+-------------------+              +----------------------+
|     MongoDB       |              | Python ML Prediction |
| Application Data  |              |       Service        |
+-------------------+              +----------+-----------+
                                              |
                                              v
                                   +----------------------+
                                   | Trained ML Model     |
                                   | Waiting-Time Model   |
                                   +----------------------+
```

------------------------------------------------------------------------

# 2. Architectural Goals

The architecture should provide:

-   Clear separation of frontend, backend, database, and ML
    responsibilities.
-   Real-time queue synchronization.
-   Dynamic waiting-time prediction.
-   Secure access to application resources.
-   Maintainable and modular code.
-   Easy integration between Node.js and Python.
-   Ability to extend the system in future.
-   Support for responsive patient and doctor interfaces.

------------------------------------------------------------------------

# 3. High-Level Components

## 3.1 React Frontend

The frontend is responsible for:

-   Patient registration UI.
-   Token display.
-   Queue status.
-   Waiting-time display.
-   Doctor dashboard.
-   Staff interface.
-   Authentication UI.
-   Real-time updates.
-   API communication.

The frontend communicates with the backend using:

-   HTTP/REST APIs
-   Socket.io

The frontend must not communicate directly with MongoDB.

------------------------------------------------------------------------

## 3.2 Node.js + Express Backend

The backend is the central application layer.

Responsibilities include:

-   Authentication and authorization.
-   Patient registration.
-   Token generation.
-   Queue management.
-   Doctor management.
-   Doctor availability.
-   API request handling.
-   Input validation.
-   MongoDB interaction.
-   ML service communication.
-   Socket.io event handling.
-   Error handling.

The backend acts as the main coordinator between the frontend, database,
and ML service.

------------------------------------------------------------------------

## 3.3 MongoDB Database

MongoDB stores persistent application data.

Primary collections:

``` text
Doctors
Patients
Queue
Users
```

Additional collections may be introduced if required during
implementation.

MongoDB is accessed through Mongoose from the Node.js backend.

------------------------------------------------------------------------

## 3.4 Python Machine Learning Service

The ML service is responsible for:

-   Loading the trained model.
-   Receiving queue-related features.
-   Generating waiting-time predictions.
-   Returning prediction results to the backend.

The ML service should remain independent from the React frontend.

A possible implementation is a lightweight Python API using Flask or
FastAPI.

------------------------------------------------------------------------

## 3.5 Socket.io Layer

Socket.io provides real-time communication between the backend and
connected frontend clients.

It is used when queue information changes.

Example events:

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

------------------------------------------------------------------------

# 4. Detailed Architecture

## 4.1 Presentation Layer

``` text
React Application
│
├── Authentication Pages
│   ├── Login
│   └── Registration
│
├── Patient Module
│   ├── Registration
│   ├── Token View
│   ├── Queue Status
│   └── Waiting Time
│
├── Doctor Module
│   ├── Dashboard
│   ├── Active Queue
│   ├── Current Patient
│   └── Consultation Actions
│
└── Staff Module
    ├── Queue Monitoring
    ├── Patient Registration
    └── Doctor Availability
```

------------------------------------------------------------------------

## 4.2 Application Layer

The Node.js backend can be organized into the following modules:

``` text
Backend
│
├── Routes
│   ├── authRoutes
│   ├── patientRoutes
│   ├── doctorRoutes
│   └── queueRoutes
│
├── Controllers
│   ├── authController
│   ├── patientController
│   ├── doctorController
│   └── queueController
│
├── Models
│   ├── User
│   ├── Patient
│   ├── Doctor
│   └── Queue
│
├── Services
│   ├── queueService
│   ├── predictionService
│   └── notificationService
│
├── Middleware
│   ├── authentication
│   ├── authorization
│   ├── validation
│   └── errorHandler
│
└── Socket
    └── queueSocket
```

This structure separates business logic from route handling and database
models.

------------------------------------------------------------------------

# 5. Data Architecture

## 5.1 Doctors Collection

Example:

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

### Purpose

Stores doctor information and parameters required for queue processing
and prediction.

------------------------------------------------------------------------

## 5.2 Patients Collection

Example:

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

### Purpose

Stores patient registration information.

------------------------------------------------------------------------

## 5.3 Queue Collection

Example:

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

### Purpose

Stores the current and historical queue state.

------------------------------------------------------------------------

## 5.4 Users Collection

Example:

``` js
{
  _id: ObjectId,
  name: String,
  email: String,
  passwordHash: String,
  role: String
}
```

Possible roles:

``` text
PATIENT
DOCTOR
STAFF
```

------------------------------------------------------------------------

# 6. Backend Request Flow

A normal patient registration request follows this path:

``` text
Patient
   |
   v
React Registration Form
   |
   | POST /api/patients
   v
Express Route
   |
   v
Validation Middleware
   |
   v
Patient Controller
   |
   +----> Patient Model
   |          |
   |          v
   |       MongoDB
   |
   v
Queue Service
   |
   v
Token Generation
   |
   v
Prediction Service
   |
   v
Python ML API
   |
   v
Predicted Waiting Time
   |
   v
Queue Database Update
   |
   v
Socket.io Event
   |
   v
Connected React Clients
```

------------------------------------------------------------------------

# 7. Patient Registration Flow

``` text
1. Patient opens registration page
              |
              v
2. Patient enters required information
              |
              v
3. React validates basic input
              |
              v
4. Request sent to Node.js backend
              |
              v
5. Backend validates request
              |
              v
6. Patient data stored in MongoDB
              |
              v
7. Queue entry created
              |
              v
8. Token number generated
              |
              v
9. Prediction features prepared
              |
              v
10. ML service called
              |
              v
11. Predicted wait time returned
              |
              v
12. Queue record updated
              |
              v
13. Socket.io broadcasts queue update
              |
              v
14. Patient sees token + waiting time
```

------------------------------------------------------------------------

# 8. Queue Processing Architecture

The queue is the core operational component.

## Queue States

``` text
WAITING
   |
   v
CALLED
   |
   v
IN_CONSULTATION
   |
   v
COMPLETED
```

Alternative paths:

``` text
WAITING ─────> CANCELLED
WAITING ─────> NO_SHOW
```

------------------------------------------------------------------------

## Queue Update Flow

Whenever a queue-changing event occurs:

``` text
Queue Event
     |
     v
Update Queue State
     |
     v
Recalculate Queue Features
     |
     v
Call ML Prediction Service
     |
     v
Update Predicted Waiting Time
     |
     v
Emit Socket.io Event
     |
     v
Update Connected Clients
```

------------------------------------------------------------------------

# 9. Waiting-Time Prediction Architecture

The prediction pipeline consists of:

``` text
MongoDB Queue Data
        |
        v
Backend Queue Service
        |
        v
Feature Preparation
        |
        v
Python Prediction API
        |
        v
Pre-trained ML Model
        |
        v
Predicted Waiting Time
        |
        v
Node.js Backend
        |
        +----> MongoDB
        |
        +----> Socket.io
                 |
                 v
            React Clients
```

------------------------------------------------------------------------

# 10. Machine Learning Service

## 10.1 ML Service Responsibilities

The ML service should:

1.  Load the trained model.
2.  Receive prediction input.
3.  Validate required features.
4.  Apply the same preprocessing used during training.
5.  Generate prediction.
6.  Return the predicted waiting time.
7.  Return an appropriate error if prediction fails.

------------------------------------------------------------------------

## 10.2 Example Prediction Request

``` json
{
  "patientsAhead": 5,
  "queueLength": 8,
  "avgConsultTime": 12,
  "doctorAvailable": 1
}
```

## Example Response

``` json
{
  "predictedWaitTime": 58
}
```

The final feature set will be determined after analysis of the synthetic
dataset.

------------------------------------------------------------------------

# 11. Model Training Architecture

Model training is separate from the live application.

``` text
Synthetic Dataset
       |
       v
Data Cleaning
       |
       v
Feature Engineering
       |
       v
Train / Validation / Test Split
       |
       v
Model Training
       |
       +----> Random Forest
       |
       +----> XGBoost
       |
       +----> LightGBM
       |
       v
Model Evaluation
       |
       v
Selected Model
       |
       v
Model Serialization
       |
       v
model.pkl / appropriate model file
       |
       v
ML Prediction Service
```

------------------------------------------------------------------------

# 12. Real-Time Communication Architecture

Socket.io maintains a persistent connection between clients and the
backend.

``` text
                  Node.js Server
                       |
             +---------+---------+
             |         |         |
             v         v         v
          Patient    Doctor    Staff
          Client     Client    Client
```

When a queue event occurs:

``` text
Doctor Completes Consultation
          |
          v
Backend Updates Queue
          |
          v
Socket.io emits "queue:updated"
          |
          +----------+-----------+
                     |
             +-------+-------+
             |       |       |
             v       v       v
          Patient  Doctor   Staff
           UI       UI       UI
```

------------------------------------------------------------------------

# 13. Authentication Architecture

Authentication flow:

``` text
User
  |
  v
Login Form
  |
  v
POST /api/auth/login
  |
  v
Backend
  |
  v
Find User in MongoDB
  |
  v
Verify Password
  |
  v
Generate Session/JWT
  |
  v
Return Authentication Result
  |
  v
Frontend
```

Protected requests:

``` text
Frontend
   |
   v
Authentication Token
   |
   v
Express Middleware
   |
   v
Verify User
   |
   v
Check Role
   |
   v
Controller
```

------------------------------------------------------------------------

# 14. Role-Based Access

  -----------------------------------------------------------------------
  Role                                Main Access
  ----------------------------------- -----------------------------------
  Patient                             Registration, own queue
                                      information, predicted waiting time

  Doctor                              Own queue, consultation status,
                                      queue updates

  Staff                               Patient registration, queue
                                      monitoring, doctor availability
  -----------------------------------------------------------------------

The exact permissions can be refined during implementation.

------------------------------------------------------------------------

# 15. API Architecture

## Authentication

``` text
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
```

## Patients

``` text
POST /api/patients
GET  /api/patients/:id
```

## Doctors

``` text
GET   /api/doctors
GET   /api/doctors/:id
PATCH /api/doctors/:id/availability
```

## Queue

``` text
POST  /api/queue
GET   /api/queue/:doctorId
PATCH /api/queue/:id/status
GET   /api/queue/:id/prediction
```

These endpoints are architectural examples; the final API contract may
change during implementation.

------------------------------------------------------------------------

# 16. Error Handling Architecture

Errors should be handled at multiple levels.

``` text
Client Validation
       |
       v
Server Validation
       |
       v
Controller Error Handling
       |
       v
Service Error Handling
       |
       v
Global Express Error Handler
       |
       v
Standardized Error Response
```

Example response:

``` json
{
  "success": false,
  "message": "Unable to update queue status"
}
```

Sensitive internal error details should not be exposed to users.

------------------------------------------------------------------------

# 17. Security Architecture

Security controls include:

``` text
Input Validation
       |
       v
Authentication
       |
       v
Authorization
       |
       v
Protected Routes
       |
       v
Database Access
```

Additional controls:

-   Password hashing.
-   Secure authentication tokens/sessions.
-   Environment variables for secrets.
-   CORS configuration.
-   Server-side validation.
-   Appropriate database permissions.
-   Avoid hard-coded credentials.
-   Avoid unnecessary sensitive information in logs.

------------------------------------------------------------------------

# 18. Deployment Architecture

A possible deployment architecture is:

``` text
                    Internet
                       |
                       v
              +----------------+
              | React Frontend |
              +-------+--------+
                      |
                      | HTTPS
                      v
              +----------------+
              | Node.js Server |
              | Express +      |
              | Socket.io      |
              +---+--------+---+
                  |        |
                  |        |
                  v        v
             +--------+  +----------------+
             | MongoDB|  | Python ML API  |
             +--------+  +-------+--------+
                                 |
                                 v
                          Trained ML Model
```

The exact hosting providers are implementation decisions and are not
fixed by this architecture.

------------------------------------------------------------------------

# 19. Recommended Project Directory Structure

## Frontend

``` text
frontend/
│
├── src/
│   ├── components/
│   ├── pages/
│   ├── layouts/
│   ├── hooks/
│   ├── services/
│   ├── context/
│   ├── utils/
│   ├── socket/
│   ├── App.jsx
│   └── main.jsx
│
├── public/
└── package.json
```

## Backend

``` text
backend/
│
├── config/
├── controllers/
├── middleware/
├── models/
├── routes/
├── services/
├── sockets/
├── utils/
├── app.js
├── server.js
└── package.json
```

## ML Service

``` text
ml-service/
│
├── data/
├── models/
├── notebooks/
├── src/
│   ├── preprocessing/
│   ├── training/
│   ├── prediction/
│   └── api/
│
├── requirements.txt
└── app.py
```

A production project may keep training code and the live prediction
service in separate directories or repositories.

------------------------------------------------------------------------

# 20. Sequence Diagram --- Patient Registration

``` text
Patient        React       Backend       MongoDB       ML Service
  |              |            |             |              |
  | Register     |            |             |              |
  |------------->|            |             |              |
  |              | POST       |             |              |
  |              |----------->|             |              |
  |              |            | Save Patient|              |
  |              |            |------------>|              |
  |              |            |<------------|              |
  |              |            | Create Queue|              |
  |              |            |------------>|              |
  |              |            |<------------|              |
  |              |            | Predict     |              |
  |              |            |--------------------------->|
  |              |            |<---------------------------|
  |              |            | Update Queue |              |
  |              |            |------------>|              |
  |              |            | Socket Event |              |
  |              |<-----------|             |              |
  |<-------------|            |             |              |
  | Token + Wait |            |             |              |
```

------------------------------------------------------------------------

# 21. Sequence Diagram --- Consultation Completion

``` text
Doctor          React        Backend        MongoDB       ML Service
  |               |             |              |              |
  | Complete      |             |              |              |
  |-------------->|             |              |              |
  |               | PATCH       |              |              |
  |               |------------>|              |              |
  |               |             | Update Queue |              |
  |               |             |------------->|              |
  |               |             |<-------------|              |
  |               |             | Recalculate  |              |
  |               |             | features     |              |
  |               |             |----------------------------->|
  |               |             |<-----------------------------|
  |               |             | Save prediction              |
  |               |             |------------->|              |
  |               |             | Socket.io     |              |
  |               |<------------|              |              |
  |               |             |              |              |
  | Patients see updated queue  |              |              |
```

------------------------------------------------------------------------

# 22. Architecture Decision Records

## ADR-01: MERN Stack

**Decision:** Use MongoDB, Express.js, React, and Node.js.

**Reason:**

-   Consistent JavaScript development across the main web application.
-   Large ecosystem.
-   Suitable for REST API development.
-   MongoDB provides flexible document storage.
-   React supports component-based UI development.

------------------------------------------------------------------------

## ADR-02: Socket.io for Real-Time Updates

**Decision:** Use Socket.io.

**Reason:**

The queue changes frequently, so manually refreshing the browser would
provide a poor user experience. Socket.io allows the server to push
queue changes to connected clients.

------------------------------------------------------------------------

## ADR-03: Separate Python ML Service

**Decision:** Keep the ML prediction component separate from the Node.js
backend.

**Reason:**

Python provides a mature machine learning ecosystem. Separating the
service also keeps ML dependencies independent from the main web
application.

------------------------------------------------------------------------

## ADR-04: MongoDB

**Decision:** Use MongoDB as the primary database.

**Reason:**

The project contains document-oriented entities such as patients,
doctors, and queue records. MongoDB also integrates naturally with
Node.js through Mongoose.

------------------------------------------------------------------------

## ADR-05: Synthetic Dataset

**Decision:** Use synthetic data for model development.

**Reason:**

The project is an academic prototype and does not rely on real hospital
patient data. This also avoids representing synthetic results as
clinical validation.

------------------------------------------------------------------------

# 23. Data Flow Summary

``` text
                         +-------------+
                         |   Patient   |
                         +------+------+
                                |
                                v
                         +-------------+
                         |   React UI  |
                         +------+------+
                                |
                         REST / Socket
                                |
                                v
                     +---------------------+
                     | Node.js + Express   |
                     +----+-----------+----+
                          |           |
                          v           v
                   +----------+   +----------+
                   | MongoDB  |   | ML API   |
                   +----------+   +----+-----+
                                      |
                                      v
                                +-----------+
                                | ML Model  |
                                +-----------+
                                      |
                                      v
                              Prediction Result
                                      |
                                      v
                               Node.js Backend
                                      |
                                  Socket.io
                                      |
                                      v
                              React Dashboards
```

------------------------------------------------------------------------

# 24. Failure Scenarios

## ML Service Unavailable

If the ML service is unavailable:

1.  Backend should detect the prediction failure.
2.  Queue registration should not expose an invalid prediction.
3.  The system should return an appropriate status.
4.  The UI should indicate that the prediction is temporarily
    unavailable.
5.  The failure should be logged.

Depending on the final implementation, a basic non-ML fallback estimate
may be used for demonstration, but it should be clearly identified as a
fallback and not as an ML prediction.

------------------------------------------------------------------------

## Database Unavailable

If MongoDB is unavailable:

-   API requests requiring database access should fail gracefully.
-   Users should receive a meaningful error message.
-   The server should log the database error.
-   The application should avoid corrupting queue state.

------------------------------------------------------------------------

## Socket Connection Lost

If a client loses its Socket.io connection:

-   The UI should indicate the connection state if practical.
-   The client should attempt reconnection.
-   The latest queue state should be fetched through the REST API after
    reconnection.

------------------------------------------------------------------------

# 25. Performance Considerations

The system should:

-   Avoid unnecessary database queries.
-   Index frequently searched fields.
-   Keep Socket.io events focused on relevant queue updates.
-   Avoid retraining the ML model during normal prediction requests.
-   Load the trained model once when the ML service starts.
-   Keep prediction requests lightweight.
-   Use pagination for large historical records if required.

------------------------------------------------------------------------

# 26. Scalability Considerations

The architecture can be extended to support:

``` text
Multiple Departments
        |
        v
Multiple Doctors
        |
        v
Multiple Queues
        |
        v
Multiple Connected Patients
```

Future scaling may involve:

-   Separate services.
-   Load balancing.
-   Redis-based Socket.io scaling.
-   Database indexing and optimization.
-   Caching.
-   Containerized deployment.

These are future considerations and are not required for the initial
academic prototype.

------------------------------------------------------------------------

# 27. Observability

The application should provide basic visibility into:

-   API errors.
-   Authentication failures.
-   Database failures.
-   ML prediction failures.
-   Socket connection problems.
-   Queue operation failures.

For an academic prototype, structured application logs are sufficient.
More advanced monitoring can be added later.

------------------------------------------------------------------------

# 28. Testing Architecture

``` text
                 Testing
                    |
       +------------+------------+
       |            |            |
       v            v            v
   Unit Tests   Integration   System Tests
                    |
                    v
             ML Model Tests
```

### Unit Testing

Test individual functions and services.

### Integration Testing

Test interactions between:

-   Backend and MongoDB.
-   Backend and ML API.
-   Backend and Socket.io.
-   Frontend and backend.

### System Testing

Test the complete patient-to-consultation workflow.

------------------------------------------------------------------------

# 29. Key Architectural Principles

The implementation should follow these principles:

### Separation of Concerns

Each layer should have a clearly defined responsibility.

### Single Responsibility

A module should focus on one major responsibility.

### Loose Coupling

The ML service should remain independently replaceable.

### Reusability

Common UI components and backend services should be reusable.

### Security by Design

Authentication, authorization, validation, and secret management should
be considered from the beginning.

### Data Consistency

Queue state and predicted waiting time should be updated together
whenever possible.

### Graceful Failure

A failure in one component should not unnecessarily crash the entire
application.

------------------------------------------------------------------------

# 30. Final Architecture Summary

The final system consists of:

``` text
                AI-Based Dynamic Patient Queue
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
   React Frontend   Node/Express      Python ML
        |             Backend           Service
        |                |                |
        |                +-------+--------+
        |                        |
        |                        v
        |                     MongoDB
        |
        +-------- Socket.io <---+
```

### Core Responsibilities

  Component                       Responsibility
  ------------------------------- --------------------------------------------
  React                           User interface and client-side interaction
  Node.js                         Main application server
  Express.js                      REST API framework
  Socket.io                       Real-time queue communication
  MongoDB                         Persistent application data
  Mongoose                        MongoDB data modeling
  Python ML Service               Waiting-time prediction
  Scikit-learn/XGBoost/LightGBM   ML model development
  Git/GitHub                      Version control

The architecture supports the project's central workflow: **patient
registration → token generation → queue tracking → ML-based waiting-time
prediction → real-time queue updates → consultation completion**.

Because the model is trained using synthetic data, the architecture is
intended for an academic prototype and should not be represented as a
clinically validated healthcare system.

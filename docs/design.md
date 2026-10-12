# System Design Document

## AI-Based Dynamic Patient Queue and Waiting Time Prediction System

**Document Version:** 1.0\
**Project Type:** Final Year Project\
**Design Approach:** Modular, Layered, Client-Server Design\
**Primary Stack:** MERN + Socket.io + Python ML\
**Database:** MongoDB\
**Dataset:** Synthetic Dataset

------------------------------------------------------------------------

# 1. Purpose

This document describes the detailed design of the **AI-Based Dynamic
Patient Queue and Waiting Time Prediction System**.

The design defines:

-   Application modules
-   User interfaces
-   Backend structure
-   Database design
-   API design
-   Queue-processing logic
-   Machine learning integration
-   Real-time communication
-   Authentication
-   Error handling
-   Security
-   Testing considerations

The system is designed as an academic prototype. The machine learning
model will use a synthetic dataset, and its results should not be
represented as clinical validation.

------------------------------------------------------------------------

# 2. Design Goals

The system design aims to provide:

1.  A simple patient registration process.
2.  Automatic token generation.
3.  Accurate queue-state tracking.
4.  Dynamic waiting-time estimation.
5.  Real-time queue updates.
6.  Separate patient and doctor interfaces.
7.  Modular backend services.
8.  Clear separation between web application and ML components.
9.  Secure access to protected resources.
10. Easy future extension.

------------------------------------------------------------------------

# 3. Design Principles

## 3.1 Separation of Concerns

Each component should have one clearly defined responsibility.

``` text
Frontend
   ↓
User Interaction

Backend
   ↓
Business Logic

Database
   ↓
Persistent Data

ML Service
   ↓
Waiting-Time Prediction
```

## 3.2 Modularity

The system is divided into independent modules so that individual
components can be developed, tested, and modified without unnecessarily
affecting other components.

## 3.3 Loose Coupling

The React application should not directly access MongoDB or the ML
model.

The Node.js backend acts as the main application coordinator.

## 3.4 Reusability

Common UI components, backend services, validation functions, and
utilities should be reusable.

## 3.5 Security by Design

Authentication, authorization, input validation, and secret management
should be considered from the beginning.

------------------------------------------------------------------------

# 4. System Modules

The system is divided into the following major modules:

``` text
AI-Based Patient Queue System
│
├── Authentication Module
├── Patient Module
├── Doctor Module
├── Staff Module
├── Queue Module
├── Token Module
├── Waiting-Time Prediction Module
├── Real-Time Communication Module
├── Notification Module
└── Data Management Module
```

------------------------------------------------------------------------

# 5. Authentication Module

## 5.1 Purpose

The authentication module verifies user identity and controls access to
protected features.

## 5.2 User Roles

``` text
PATIENT
DOCTOR
STAFF
```

## 5.3 Login Flow

``` text
User
 |
 v
Login Page
 |
 v
Enter Credentials
 |
 v
POST /api/auth/login
 |
 v
Validate User
 |
 v
Verify Password
 |
 v
Generate Authentication Token/Session
 |
 v
Return Response
 |
 v
Redirect to Role-Based Dashboard
```

## 5.4 Design Requirements

-   Passwords must never be stored as plain text.
-   Protected APIs must require authentication.
-   Role-based authorization should be applied to restricted operations.
-   Authentication errors should return safe messages.

------------------------------------------------------------------------

# 6. Patient Module

## 6.1 Purpose

The patient module allows users to register and monitor their queue
status.

## 6.2 Main Features

-   Patient registration
-   Doctor/department selection
-   Token generation
-   Queue position
-   Predicted waiting time
-   Current serving token
-   Real-time queue updates
-   Consultation status

## 6.3 Patient Flow

``` text
Open Application
       |
       v
Patient Registration
       |
       v
Select Doctor
       |
       v
Submit Registration
       |
       v
Generate Token
       |
       v
Join Queue
       |
       v
Calculate Waiting Time
       |
       v
Display Queue Dashboard
       |
       v
Receive Real-Time Updates
       |
       v
Consultation
```

------------------------------------------------------------------------

# 7. Doctor Module

## 7.1 Purpose

The doctor module allows doctors to monitor and process their active
patient queue.

## 7.2 Main Features

-   Doctor dashboard
-   View active queue
-   View current patient
-   Call next patient
-   Start consultation
-   Complete consultation
-   Update patient status
-   View doctor availability

## 7.3 Doctor Flow

``` text
Doctor Login
     |
     v
Doctor Dashboard
     |
     v
View Queue
     |
     v
Call Next Patient
     |
     v
Start Consultation
     |
     v
Complete Consultation
     |
     v
Queue Automatically Updates
```

------------------------------------------------------------------------

# 8. Staff Module

## 8.1 Purpose

Staff can perform operational tasks related to patient registration and
queue monitoring.

## 8.2 Main Features

-   Register patients
-   View queues
-   Monitor token status
-   Manage doctor availability
-   Correct permitted queue information

Staff permissions should be restricted according to the final
authorization design.

------------------------------------------------------------------------

# 9. Queue Module

The queue module is the central business module.

## 9.1 Queue States

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

Alternative states:

``` text
WAITING → CANCELLED
WAITING → NO_SHOW
```

## 9.2 Queue State Rules

A patient should normally follow:

``` text
WAITING → CALLED
CALLED → IN_CONSULTATION
IN_CONSULTATION → COMPLETED
```

Invalid state transitions should be rejected by the backend.

## 9.3 Queue Ordering

For the initial version, the queue will generally follow registration
order for a selected doctor.

Example:

``` text
Token 101 → WAITING
Token 102 → WAITING
Token 103 → WAITING
```

After Token 101 is completed:

``` text
Token 101 → COMPLETED
Token 102 → NEXT
Token 103 → WAITING
```

The project can support more advanced prioritization in future versions
if required.

------------------------------------------------------------------------

# 10. Token Module

## 10.1 Purpose

The token module generates and maintains queue token numbers.

## 10.2 Token Requirements

Each active queue entry should have:

-   Token number
-   Patient ID
-   Doctor ID
-   Queue status
-   Registration time

## 10.3 Token Generation Concept

``` text
Doctor Queue
      |
      v
Find Latest Token
      |
      v
Increment Token
      |
      v
Assign New Token
```

Token numbering should avoid duplicate active tokens for the same
doctor/queue context.

------------------------------------------------------------------------

# 11. Waiting-Time Prediction Module

## 11.1 Purpose

This module predicts the expected waiting time for a patient.

The prediction is an estimate and not a guaranteed time.

## 11.2 Input Features

Potential features include:

``` text
Patients Ahead
Queue Length
Average Consultation Time
Doctor Availability
Current Consultation Status
Registration/Arrival Information
Other Dataset-Supported Features
```

The final feature set will be determined from the synthetic dataset and
model experiments.

## 11.3 Prediction Flow

``` text
Queue Data
    |
    v
Feature Extraction
    |
    v
Feature Validation
    |
    v
Python ML Service
    |
    v
Trained Model
    |
    v
Predicted Waiting Time
    |
    v
Backend
    |
    v
MongoDB + Frontend
```

------------------------------------------------------------------------

# 12. Machine Learning Design

## 12.1 Training Pipeline

``` text
Synthetic Dataset
       |
       v
Data Cleaning
       |
       v
Exploratory Data Analysis
       |
       v
Feature Engineering
       |
       v
Train/Test Split
       |
       v
Model Training
       |
       +----------------------+
       |                      |
       v                      v
Random Forest          XGBoost / LightGBM
       |                      |
       +----------+-----------+
                  |
                  v
          Model Evaluation
                  |
                  v
           Selected Model
                  |
                  v
          Model Serialization
```

## 12.2 Candidate Models

Possible models:

-   Random Forest Regressor
-   XGBoost Regressor
-   LightGBM Regressor
-   Linear Regression as a baseline

The final model should be selected using documented evaluation results
rather than assumed performance.

## 12.3 Evaluation Metrics

The model may be evaluated using:

-   MAE
-   MSE
-   RMSE
-   R² Score

------------------------------------------------------------------------

# 13. ML Prediction API Design

A lightweight Python API can expose the trained model.

## 13.1 Endpoint

``` text
POST /predict
```

## 13.2 Request

``` json
{
  "patientsAhead": 5,
  "queueLength": 8,
  "avgConsultTime": 12,
  "doctorAvailable": 1
}
```

## 13.3 Response

``` json
{
  "predictedWaitTime": 58
}
```

The exact fields will depend on the finalized trained model.

------------------------------------------------------------------------

# 14. Dynamic Prediction Design

Waiting-time prediction should be updated when queue conditions change.

## 14.1 Events Triggering Recalculation

-   New patient joins queue.
-   Patient completes consultation.
-   Patient is cancelled.
-   Patient is marked no-show.
-   Doctor availability changes.
-   Relevant consultation information changes.

## 14.2 Dynamic Update Flow

``` text
Queue Event
     |
     v
Update Queue
     |
     v
Get Current Queue State
     |
     v
Generate Prediction Features
     |
     v
Call ML Service
     |
     v
Receive Prediction
     |
     v
Save Prediction
     |
     v
Emit Socket.io Event
     |
     v
Update Client Interfaces
```

------------------------------------------------------------------------

# 15. Real-Time Communication Design

Socket.io will synchronize queue information between the backend and
connected clients.

## 15.1 Event Examples

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

## 15.2 Event Example

When a doctor completes a consultation:

``` text
Doctor
  |
  v
React Dashboard
  |
  v
PATCH /api/queue/:id/status
  |
  v
Backend
  |
  +--> Update MongoDB
  |
  +--> Recalculate Prediction
  |
  +--> Emit queue:updated
  |
  v
Connected Clients
```

------------------------------------------------------------------------

# 16. Database Design

## 16.1 Doctors Collection

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

## 16.2 Patients Collection

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

## 16.3 Queue Collection

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

## 16.4 Users Collection

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

# 17. Entity Relationships

The conceptual relationships are:

``` text
User
 |
 | may represent
 v
Patient / Doctor / Staff


Patient
   |
   | 1 : Many
   v
Queue Entries


Doctor
   |
   | 1 : Many
   v
Queue Entries
```

A queue entry references one patient and one doctor.

------------------------------------------------------------------------

# 18. Backend Design

## 18.1 Recommended Structure

``` text
backend/
│
├── config/
│   └── db.js
│
├── controllers/
│   ├── authController.js
│   ├── patientController.js
│   ├── doctorController.js
│   └── queueController.js
│
├── models/
│   ├── User.js
│   ├── Patient.js
│   ├── Doctor.js
│   └── Queue.js
│
├── routes/
│   ├── authRoutes.js
│   ├── patientRoutes.js
│   ├── doctorRoutes.js
│   └── queueRoutes.js
│
├── services/
│   ├── queueService.js
│   ├── predictionService.js
│   └── notificationService.js
│
├── middleware/
│   ├── authMiddleware.js
│   ├── roleMiddleware.js
│   ├── validationMiddleware.js
│   └── errorMiddleware.js
│
├── sockets/
│   └── queueSocket.js
│
├── utils/
│   └── helpers.js
│
├── app.js
└── server.js
```

------------------------------------------------------------------------

# 19. Frontend Design

## 19.1 Recommended Structure

``` text
frontend/
│
├── src/
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── QueueCard.jsx
│   │   ├── TokenCard.jsx
│   │   └── Loading.jsx
│   │
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── PatientDashboard.jsx
│   │   ├── DoctorDashboard.jsx
│   │   └── StaffDashboard.jsx
│   │
│   ├── services/
│   │   └── api.js
│   │
│   ├── socket/
│   │   └── socket.js
│   │
│   ├── context/
│   │   └── AuthContext.jsx
│   │
│   ├── hooks/
│   │
│   ├── utils/
│   │
│   ├── App.jsx
│   └── main.jsx
│
└── package.json
```

------------------------------------------------------------------------

# 20. Patient UI Design

## 20.1 Registration Page

The page should contain:

``` text
+--------------------------------------+
|         Patient Registration         |
+--------------------------------------+
| Name                                 |
| [____________________________]       |
|                                      |
| Age                                  |
| [________]                           |
|                                      |
| Gender                               |
| [ Select ]                           |
|                                      |
| Contact                              |
| [____________________________]       |
|                                      |
| Doctor                               |
| [ Select Doctor ]                    |
|                                      |
|          [ Register ]                |
+--------------------------------------+
```

## 20.2 Queue Dashboard

``` text
+--------------------------------------+
|           Your Queue Status          |
+--------------------------------------+
| Token Number       #105              |
|                                      |
| Queue Position     4                 |
|                                      |
| Current Token      #101              |
|                                      |
| Estimated Wait     38 minutes        |
|                                      |
| Status             Waiting           |
+--------------------------------------+
```

The UI should clearly distinguish between:

-   Current queue position
-   Current serving token
-   Predicted waiting time
-   Patient's status

------------------------------------------------------------------------

# 21. Doctor Dashboard Design

``` text
+------------------------------------------------+
|                Doctor Dashboard                |
+------------------------------------------------+
| Doctor: Dr. Sharma       Status: Available     |
+------------------------------------------------+
| Current Patient: Token #101                    |
|                                                |
| [ Start Consultation ] [ Complete ]            |
+------------------------------------------------+
|                 Active Queue                   |
+------+----------+-------------+---------------+
|Token | Patient  | Status      | Wait Time     |
+------+----------+-------------+---------------+
|101   | Patient A| Consulting  | --            |
|102   | Patient B| Waiting     | 12 min        |
|103   | Patient C| Waiting     | 25 min        |
+------+----------+-------------+---------------+
```

------------------------------------------------------------------------

# 22. API Design

## Authentication

``` text
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
```

## Patient

``` text
POST /api/patients
GET  /api/patients/:id
```

## Doctor

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

------------------------------------------------------------------------

# 23. API Request/Response Design

## Registration Request

``` json
{
  "name": "Rahul Kumar",
  "age": 25,
  "gender": "Male",
  "contact": "XXXXXXXXXX",
  "doctorId": "doctor_id"
}
```

## Registration Response

``` json
{
  "success": true,
  "message": "Patient registered successfully",
  "data": {
    "patientId": "patient_id",
    "tokenNumber": 105,
    "queuePosition": 4,
    "predictedWaitTime": 38
  }
}
```

The example contact value is intentionally masked; real application data
should be handled securely.

------------------------------------------------------------------------

# 24. Standard API Response Format

Successful response:

``` json
{
  "success": true,
  "message": "Operation successful",
  "data": {}
}
```

Error response:

``` json
{
  "success": false,
  "message": "Invalid request"
}
```

This provides consistency across APIs.

------------------------------------------------------------------------

# 25. Validation Design

## Patient Validation

Required:

-   Name
-   Age
-   Gender where applicable
-   Contact where applicable
-   Doctor

Validation examples:

``` text
Name → required
Age → valid numeric range
Contact → valid format
Doctor ID → valid existing doctor
```

## Queue Validation

The backend should verify:

-   Queue entry exists.
-   User has permission.
-   Status transition is valid.
-   Doctor is associated with the queue entry.
-   Required prediction features are valid.

------------------------------------------------------------------------

# 26. Error Handling Design

Errors should be handled at four levels:

``` text
Frontend Validation
        |
        v
API Validation
        |
        v
Service-Level Handling
        |
        v
Global Error Handler
```

Example:

``` json
{
  "success": false,
  "message": "Patient could not be registered"
}
```

Internal technical details should be logged on the server but not
unnecessarily exposed to users.

------------------------------------------------------------------------

# 27. Security Design

The system should implement:

## Authentication

Use secure password hashing and an appropriate session/JWT strategy.

## Authorization

Check user role before protected operations.

## Input Validation

Validate all client-provided data on the server.

## Secret Management

Store:

``` text
DATABASE_URL
JWT_SECRET
ML_SERVICE_URL
OTHER_API_KEYS
```

in environment variables rather than source code.

## Database Security

Use appropriate database credentials and permissions.

------------------------------------------------------------------------

# 28. Real-Time State Synchronization

A client can initially retrieve queue information through REST:

``` text
GET /api/queue/:doctorId
```

Then Socket.io maintains live updates.

``` text
Initial State
     |
     v
REST API
     |
     v
React State
     |
     v
Socket.io Listener
     |
     v
Queue Event
     |
     v
Update React State
```

This combination prevents the application from depending entirely on a
persistent socket connection.

------------------------------------------------------------------------

# 29. Queue Algorithm Design

## 29.1 Add Patient

``` text
Input:
patientId
doctorId

1. Find active queue for doctor.
2. Determine next token number.
3. Create queue entry.
4. Determine current patients ahead.
5. Prepare prediction features.
6. Request ML prediction.
7. Save predicted waiting time.
8. Emit queue update.
```

## 29.2 Complete Patient

``` text
Input:
queueId

1. Validate queue entry.
2. Verify authorized doctor/staff.
3. Change status to COMPLETED.
4. Record completion time.
5. Recalculate affected queue information.
6. Request updated predictions if required.
7. Save results.
8. Emit real-time update.
```

------------------------------------------------------------------------

# 30. Waiting-Time Design

The system should treat waiting time as a dynamic estimate.

Conceptually:

``` text
Predicted Wait Time
        =
ML Model(
    Queue Features
)
```

Potential inputs:

``` text
Patients Ahead
Queue Length
Average Consultation Time
Doctor Availability
Current Consultation State
Other Validated Features
```

The system should not display the prediction as a guaranteed appointment
time.

------------------------------------------------------------------------

# 31. Model Explainability Design

If SHAP is included, the system may provide an explanation of which
features influenced the prediction.

Example conceptual output:

``` text
Predicted Wait Time: 38 minutes

Main contributing factors:
- 5 patients ahead
- High current queue length
- Average consultation time: 12 minutes
```

This feature is optional for the initial MVP.

------------------------------------------------------------------------

# 32. Notification Design

The initial version may use in-app notifications.

Possible notifications:

``` text
"Your token is #105."

"Token #103 is currently being served."

"Your estimated waiting time has changed."

"Please be ready for your consultation."
```

SMS or email notifications can be added as future enhancements.

------------------------------------------------------------------------

# 33. Responsive Design

The frontend should follow a responsive design approach.

Target screen sizes:

``` text
Mobile
Tablet
Laptop
Desktop
```

The UI should prioritize the most important information on smaller
screens:

``` text
Token Number
      ↓
Queue Position
      ↓
Predicted Wait
      ↓
Current Serving Token
      ↓
Status
```

------------------------------------------------------------------------

# 34. Accessibility Considerations

The interface should aim to provide:

-   Readable font sizes.
-   Clear labels.
-   Keyboard-friendly controls.
-   Meaningful button text.
-   Sufficient visual distinction between states.
-   Clear error messages.
-   Responsive layout.

------------------------------------------------------------------------

# 35. Deployment Design

Possible deployment structure:

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
          | Express        |
          | Socket.io      |
          +---+--------+---+
              |        |
              v        v
        +---------+  +-----------+
        | MongoDB |  | ML API    |
        +---------+  +-----+-----+
                           |
                           v
                     Trained Model
```

The actual hosting providers can be selected later.

------------------------------------------------------------------------

# 36. Configuration Design

Example backend environment variables:

``` text
PORT=
MONGODB_URI=
JWT_SECRET=
ML_SERVICE_URL=
CLIENT_URL=
```

Example ML environment variables:

``` text
MODEL_PATH=
PORT=
```

No secret values should be committed to GitHub.

------------------------------------------------------------------------

# 37. Logging Design

The system should log:

``` text
INFO
  Server started
  Database connected
  ML service connected

WARN
  Invalid request
  Prediction unavailable

ERROR
  Database error
  ML service error
  Authentication failure
```

Logs should avoid unnecessarily exposing personal or sensitive
information.

------------------------------------------------------------------------

# 38. Failure Handling Design

## ML Service Failure

``` text
Prediction Request
       |
       v
ML Service
       |
       X
Failure
       |
       v
Backend catches error
       |
       v
Return controlled response
       |
       v
Frontend displays temporary unavailability
```

## Socket Failure

``` text
Socket Disconnected
       |
       v
Reconnect Attempt
       |
       v
Reconnect Successful
       |
       v
Fetch Latest Queue State
       |
       v
Synchronize UI
```

## Database Failure

The backend should:

-   Return an appropriate error.
-   Log the failure.
-   Avoid partial or inconsistent queue updates where possible.

------------------------------------------------------------------------

# 39. Testing Design

## 39.1 Unit Testing

Test:

-   Token generation
-   Queue state transitions
-   Validation functions
-   Prediction service
-   Authentication utilities

## 39.2 Integration Testing

Test:

``` text
React → Backend
Backend → MongoDB
Backend → ML Service
Backend → Socket.io
```

## 39.3 End-to-End Testing

Test:

``` text
Patient Registration
        ↓
Token Generation
        ↓
Queue Entry
        ↓
Prediction
        ↓
Doctor Consultation
        ↓
Queue Update
        ↓
Patient Dashboard Update
```

------------------------------------------------------------------------

# 40. Security and Privacy Boundaries

The project should avoid collecting unnecessary personal information.

Because the project uses synthetic data for ML development:

-   Synthetic records should be clearly identified during experiments.
-   Real patient data should not be included in the development dataset.
-   Model results should not be described as clinically validated.
-   The prototype should not provide medical diagnosis or treatment
    recommendations.

------------------------------------------------------------------------

# 41. Design Constraints

The design is subject to:

1.  Academic project timeline.
2.  Availability of synthetic data.
3.  Limited infrastructure.
4.  Model performance depending on dataset quality.
5.  Potential difference between synthetic queue behavior and real-world
    healthcare environments.
6.  Limited scope of the initial MVP.

------------------------------------------------------------------------

# 42. Future Design Extensions

The architecture can later support:

``` text
Multi-Hospital Support
        |
        v
Multi-Department Queues
        |
        v
Appointment Scheduling
        |
        v
Advanced Notifications
        |
        v
Analytics Dashboard
        |
        v
Continuous Model Retraining
        |
        v
Mobile Application
```

Future versions may also introduce:

-   Advanced queue prioritization.
-   More sophisticated prediction models.
-   Historical analytics.
-   Model monitoring.
-   Explainability dashboards.
-   External hospital-system integration.

------------------------------------------------------------------------

# 43. End-to-End Design Summary

The complete system design can be summarized as:

``` text
                    USER
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
              +---+-------+---+
                  |       |
                  |       |
                  v       v
             +--------+  +-----------+
             |MongoDB |  | Python ML |
             +--------+  +-----+-----+
                               |
                               v
                         Trained Model
                               |
                               v
                     Waiting Prediction
                               |
                               v
                         Node Backend
                               |
                               v
                         Socket.io
                               |
                               v
                       Updated Clients
```

The core design principle is that **Node.js acts as the central
application coordinator**, MongoDB maintains persistent state, the
Python service handles machine learning prediction, and Socket.io
distributes important queue changes to connected users in real time.

------------------------------------------------------------------------

# 44. Final Design Checklist

Before implementation is considered complete, verify:

-   [ ] React application created.
-   [ ] Backend structure created.
-   [ ] MongoDB connection implemented.
-   [ ] User authentication implemented.
-   [ ] Role-based authorization implemented.
-   [ ] Patient registration implemented.
-   [ ] Token generation implemented.
-   [ ] Queue state management implemented.
-   [ ] Doctor dashboard implemented.
-   [ ] Patient dashboard implemented.
-   [ ] Socket.io integrated.
-   [ ] Synthetic dataset prepared.
-   [ ] ML model trained and evaluated.
-   [ ] Python prediction service implemented.
-   [ ] Backend-to-ML communication implemented.
-   [ ] Dynamic prediction update implemented.
-   [ ] Error handling implemented.
-   [ ] Responsive UI implemented.
-   [ ] Unit/integration/system testing performed.
-   [ ] Deployment configuration prepared.
-   [ ] Documentation updated.

------------------------------------------------------------------------

# 45. Final Statement

The proposed design provides a structured foundation for implementing
the **AI-Based Dynamic Patient Queue and Waiting Time Prediction
System**. It separates user interaction, application logic, persistent
storage, real-time communication, and machine learning into manageable
components.

The design supports the project's main workflow:

**Patient Registration → Token Generation → Queue Entry → Waiting-Time
Prediction → Real-Time Queue Updates → Consultation → Queue Completion**

The system is intended as an academic prototype using synthetic data.
Any future use with real healthcare environments would require
additional security, privacy, integration, testing, and appropriate
clinical validation.

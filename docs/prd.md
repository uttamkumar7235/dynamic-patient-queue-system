# Product Requirements Document (PRD)

## AI-Based Dynamic Patient Queue and Waiting Time Prediction System

**Document Version:** 1.0\
**Project Type:** Final Year Project\
**Technology Stack:** MERN Stack + Socket.io + Python/ML\
**Dataset:** Synthetic Dataset\
**Project Status:** Initial Development

------------------------------------------------------------------------

## 1. Project Overview

The **AI-Based Dynamic Patient Queue and Waiting Time Prediction
System** is a web-based application designed to improve the patient
queue experience by providing digital patient registration, token
assignment, real-time queue updates, and AI/ML-based waiting-time
prediction.

The system will allow patients to register for a consultation and
receive a queue token. Doctors or authorized staff will be able to
manage the active queue and update consultation status. The system will
continuously use current queue information and other relevant parameters
to estimate the patient's expected waiting time.

The project will use a **synthetic dataset** for developing and
evaluating the machine learning model. It will not claim clinical
validation or use real hospital patient data.

------------------------------------------------------------------------

## 2. Problem Statement

Traditional patient queues can make it difficult for patients to know
how long they will have to wait. Static token systems generally provide
a queue position but do not dynamically estimate waiting time when the
queue changes.

The proposed system addresses this problem by combining:

-   Digital patient registration
-   Automatic token generation
-   Queue tracking
-   Real-time status updates
-   Dynamic waiting-time prediction
-   Doctor availability information
-   Machine learning-based estimation

------------------------------------------------------------------------

## 3. Objectives

### Primary Objectives

1.  Develop a web-based digital patient registration system.
2.  Generate and manage patient queue tokens.
3.  Provide real-time queue updates using Socket.io.
4.  Predict the expected waiting time for patients using machine
    learning.
5.  Update waiting-time estimates when queue conditions change.
6.  Provide separate interfaces for patients and authorized
    staff/doctors.
7.  Store application and queue data using MongoDB.
8.  Build a modular architecture that can be extended in the future.

### Secondary Objectives

-   Reduce uncertainty about expected waiting time.
-   Improve transparency of queue status.
-   Provide a simple and responsive user interface.
-   Display relevant queue information without requiring patients to
    repeatedly ask staff.
-   Provide a foundation for future AI-based healthcare queue features.

------------------------------------------------------------------------

## 4. Target Users

### 4.1 Patients

Patients will be able to:

-   Register for consultation.
-   Select or view the relevant doctor/department.
-   Receive a token number.
-   View their queue position.
-   View predicted waiting time.
-   Receive real-time queue updates.
-   View consultation status.

### 4.2 Doctors

Doctors will be able to:

-   View their active queue.
-   See registered patients.
-   Start or complete consultations.
-   Update patient status.
-   View relevant queue information.

### 4.3 Authorized Staff/Admin

Authorized staff may be able to:

-   Register patients.
-   Manage queues.
-   Manage doctor availability.
-   Monitor active consultations.
-   Correct or update queue information when required.

------------------------------------------------------------------------

## 5. Product Scope

### In Scope

-   Patient registration
-   Token generation
-   Doctor/department selection
-   Queue creation and tracking
-   Doctor availability
-   Real-time queue updates
-   Waiting-time prediction
-   Patient status management
-   MongoDB database
-   REST API backend
-   Responsive frontend
-   Machine learning model integration
-   Basic authentication/authorization
-   Queue dashboard

### Out of Scope

The first version will not include:

-   Real patient medical records
-   Diagnosis or treatment recommendations
-   Clinical decision-making
-   Emergency medical prioritization
-   Integration with real hospital information systems
-   Real-world clinical validation
-   Medical diagnosis using AI
-   Payment processing
-   Insurance processing

------------------------------------------------------------------------

## 6. Functional Requirements

### FR-01: Patient Registration

The system shall allow a patient to enter required registration
information.

Possible fields include:

-   Patient name
-   Age
-   Gender
-   Contact information
-   Doctor/department
-   Registration date/time
-   Other parameters required by the prediction model

The system shall validate required fields before registration.

------------------------------------------------------------------------

### FR-02: Token Generation

After successful registration, the system shall generate a unique queue
token.

The token should contain or be associated with:

-   Token number
-   Patient ID
-   Doctor ID
-   Queue ID
-   Registration timestamp
-   Current status

------------------------------------------------------------------------

### FR-03: Queue Management

The system shall maintain the current queue for each doctor.

Possible patient statuses:

-   Waiting
-   In Consultation
-   Completed
-   Cancelled
-   No-show

The queue order shall be updated when a patient's status changes.

------------------------------------------------------------------------

### FR-04: Waiting-Time Prediction

The system shall estimate the expected waiting time for a patient using
a machine learning model.

Potential input features include:

-   Number of patients ahead
-   Doctor availability
-   Average consultation time
-   Current queue length
-   Patient arrival/registration time
-   Department/doctor information
-   Number of active consultations
-   Historical/synthetic queue-related parameters

The exact features will be finalized during model development based on
dataset analysis and model performance.

------------------------------------------------------------------------

### FR-05: Dynamic Prediction

The predicted waiting time shall be recalculated when important queue
conditions change.

Examples:

-   A patient completes consultation.
-   A new patient joins the queue.
-   Doctor availability changes.
-   Consultation duration changes.
-   A patient is cancelled or marked as no-show.

------------------------------------------------------------------------

### FR-06: Real-Time Updates

The system shall use **Socket.io** to provide real-time queue updates.

When the queue changes, connected clients should receive updated
information without manually refreshing the page.

------------------------------------------------------------------------

### FR-07: Doctor Dashboard

The doctor dashboard shall display:

-   Doctor information
-   Current queue
-   Patient token numbers
-   Patient status
-   Current/next patient
-   Consultation actions
-   Relevant waiting-time information

------------------------------------------------------------------------

### FR-08: Patient Dashboard

The patient dashboard shall display:

-   Patient token
-   Queue position
-   Doctor/department
-   Current queue status
-   Predicted waiting time
-   Current serving token
-   Consultation status

------------------------------------------------------------------------

### FR-09: Doctor Availability

The system shall maintain doctor availability information.

Possible states:

-   Available
-   Unavailable
-   On break
-   Consultation in progress

Availability information may be used as an input to waiting-time
calculation.

------------------------------------------------------------------------

### FR-10: Authentication and Authorization

The system should provide secure login functionality for authorized
users.

Different roles may have different permissions, such as:

-   Patient
-   Doctor
-   Staff/Admin

Users shall only access functions permitted for their role.

------------------------------------------------------------------------

### FR-11: Data Storage

Application data shall be stored in MongoDB.

The backend shall use Mongoose for schema definition and database
interaction.

------------------------------------------------------------------------

### FR-12: Error Handling

The system shall provide meaningful error messages for:

-   Invalid registration data
-   Missing required fields
-   Database errors
-   Authentication failures
-   Prediction service failures
-   Invalid queue operations

------------------------------------------------------------------------

## 7. Non-Functional Requirements

### NFR-01: Performance

The system should provide responsive API operations and avoid
unnecessary delays during normal usage.

### NFR-02: Real-Time Responsiveness

Queue changes should be reflected on connected clients with minimal
delay.

### NFR-03: Scalability

The architecture should allow additional doctors, departments, and
queues to be added without major changes to the application structure.

### NFR-04: Usability

The interface should be simple enough for users with limited technical
experience.

### NFR-05: Responsiveness

The frontend should work on:

-   Desktop
-   Laptop
-   Tablet
-   Mobile devices

### NFR-06: Security

The application should:

-   Validate user input.
-   Protect authenticated routes.
-   Avoid exposing sensitive information unnecessarily.
-   Store passwords securely if authentication uses passwords.
-   Use environment variables for secrets and API keys.

### NFR-07: Maintainability

Frontend, backend, and ML components should be separated into logical
modules.

### NFR-08: Reliability

The application should handle invalid operations and temporary
prediction/API failures gracefully.

------------------------------------------------------------------------

## 8. Proposed Technology Stack

### Frontend

-   React.js
-   JavaScript
-   HTML5
-   CSS3
-   Tailwind CSS or equivalent styling approach

### Backend

-   Node.js
-   Express.js
-   REST APIs
-   Socket.io

### Database

-   MongoDB
-   Mongoose

### Machine Learning

-   Python
-   Pandas
-   NumPy
-   Scikit-learn
-   XGBoost and/or LightGBM for model experimentation
-   Joblib for model serialization
-   SHAP may be used for model explainability

### Development Tools

-   Git
-   GitHub
-   VS Code
-   Postman
-   MongoDB Compass

------------------------------------------------------------------------

## 9. System Architecture

The proposed system will follow a modular architecture:

``` text
                    +----------------------+
                    |      User Interface  |
                    |    React Frontend    |
                    +----------+-----------+
                               |
                    REST API / Socket.io
                               |
                    +----------v-----------+
                    |   Node.js + Express  |
                    |      Backend API     |
                    +----+------------+----+
                         |            |
                    +----v----+  +----v------+
                    | MongoDB |  | ML Service |
                    | Database|  |  Python    |
                    +---------+  +-----+------+
                                      |
                               +------v------+
                               | ML Prediction|
                               | Model       |
                               +-------------+
```

------------------------------------------------------------------------

## 10. Database Requirements

### 10.1 Doctors Collection

Example structure:

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

### 10.2 Patients Collection

Example structure:

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

### 10.3 Queue Collection

Example structure:

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

The final schema may be adjusted during implementation according to
application requirements.

------------------------------------------------------------------------

## 11. Machine Learning Requirements

### 11.1 Prediction Goal

The ML component will predict the expected waiting time for a patient in
minutes.

### 11.2 Dataset

A **synthetic dataset** will be used for model development and testing.

The dataset may contain variables such as:

-   Queue length
-   Patients ahead
-   Average consultation time
-   Doctor availability
-   Arrival time
-   Consultation-related parameters
-   Historical/synthetic waiting time

### 11.3 Candidate Models

The project may experiment with:

-   Linear Regression
-   Random Forest Regressor
-   XGBoost Regressor
-   LightGBM Regressor

The final model will be selected based on documented evaluation metrics
and suitability for the project.

### 11.4 Evaluation Metrics

Possible regression metrics include:

-   Mean Absolute Error (MAE)
-   Mean Squared Error (MSE)
-   Root Mean Squared Error (RMSE)
-   R² Score

### 11.5 Model Integration

The trained model may be exposed through a Python-based prediction
service/API.

The Node.js backend will send relevant queue parameters to the ML
service and receive the predicted waiting time.

------------------------------------------------------------------------

## 12. API Requirements

Example REST API groups:

### Patient APIs

``` text
POST   /api/patients
GET    /api/patients/:id
```

### Doctor APIs

``` text
GET    /api/doctors
GET    /api/doctors/:id
PATCH  /api/doctors/:id/availability
```

### Queue APIs

``` text
POST   /api/queue
GET    /api/queue/:doctorId
PATCH  /api/queue/:id/status
GET    /api/queue/:id/prediction
```

### Authentication APIs

``` text
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
```

The exact API structure may change during implementation.

------------------------------------------------------------------------

## 13. Real-Time Events

Socket.io events may include:

``` text
queue:updated
patient:registered
patient:called
consultation:started
consultation:completed
patient:cancelled
doctor:availabilityChanged
prediction:updated
```

These event names are proposed and may be refined during implementation.

------------------------------------------------------------------------

## 14. User Flow

### Patient Flow

``` text
Open Application
      |
      v
Patient Registration
      |
      v
Select Doctor/Department
      |
      v
Generate Token
      |
      v
Join Queue
      |
      v
View Queue Position
      |
      v
View Predicted Waiting Time
      |
      v
Receive Real-Time Updates
      |
      v
Consultation
      |
      v
Queue Status = Completed
```

### Doctor Flow

``` text
Login
  |
  v
Open Doctor Dashboard
  |
  v
View Active Queue
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

## 15. Waiting-Time Calculation Concept

The system should not rely only on a fixed formula.

Instead, the ML model will learn relationships between queue-related
input features and waiting time from the synthetic dataset.

A simplified conceptual relationship is:

``` text
Waiting Time
      =
f(
  Patients Ahead,
  Average Consultation Time,
  Doctor Availability,
  Queue Length,
  Other Relevant Features
)
```

The actual prediction will be generated by the trained model.

------------------------------------------------------------------------

## 16. Real-Time Dynamic Update Logic

When a queue event occurs:

``` text
Queue Event
    |
    +--> New Patient Added
    |
    +--> Patient Completed
    |
    +--> Patient Cancelled
    |
    +--> Doctor Availability Changed
    |
    v
Update Queue
    |
    v
Prepare Current Features
    |
    v
ML Prediction
    |
    v
Store Updated Prediction
    |
    v
Emit Socket.io Event
    |
    v
Update Patient/Doctor UI
```

------------------------------------------------------------------------

## 17. UI Requirements

### Patient Interface

The patient interface should contain:

-   Registration form
-   Token confirmation
-   Queue status card
-   Predicted waiting time
-   Current serving token
-   Queue position
-   Doctor information
-   Status notifications

### Doctor Interface

The doctor interface should contain:

-   Dashboard
-   Active queue table/list
-   Current patient
-   Next patient
-   Patient status controls
-   Availability controls
-   Queue statistics

------------------------------------------------------------------------

## 18. Validation Requirements

The system should validate:

-   Required fields
-   Valid age range
-   Valid contact information
-   Valid doctor selection
-   Valid queue status transitions
-   Duplicate/invalid queue operations
-   Authentication credentials
-   ML input values

------------------------------------------------------------------------

## 19. Security Requirements

The application should implement:

-   Password hashing for password-based authentication.
-   JWT/session-based authorization where applicable.
-   Protected API routes.
-   Server-side validation.
-   Sanitization of user input.
-   Environment variables for secrets.
-   Appropriate CORS configuration.
-   No hard-coded credentials or API keys.

------------------------------------------------------------------------

## 20. Logging and Monitoring

The backend should log important application events such as:

-   Server errors
-   Database errors
-   Authentication failures
-   Queue update failures
-   ML prediction failures

Logs should not unnecessarily contain sensitive patient information.

------------------------------------------------------------------------

## 21. Assumptions

1.  The project uses synthetic data.
2.  Internet connectivity is available when the deployed application
    requires external services.
3.  Doctor consultation times can vary.
4.  The ML model provides an estimate rather than a guaranteed waiting
    time.
5.  The initial implementation is intended as an academic prototype.
6.  The project does not replace professional medical or hospital
    decision-making systems.

------------------------------------------------------------------------

## 22. Constraints

-   Availability of suitable synthetic training data.
-   Limited project development time.
-   ML prediction accuracy depends on dataset quality.
-   Real-world queue behavior can differ from synthetic data.
-   The first version may support a limited number of roles and
    workflows.
-   Clinical validation is outside the current project scope.

------------------------------------------------------------------------

## 23. Success Criteria

The project will be considered functionally successful when:

-   A patient can register successfully.
-   A unique token is generated.
-   The patient is added to the correct queue.
-   The doctor/staff dashboard displays the active queue.
-   Queue status can be updated.
-   Waiting time can be predicted by the ML component.
-   Predictions can be updated after queue changes.
-   Connected clients receive real-time queue updates.
-   Data is correctly stored and retrieved from MongoDB.
-   The application works responsively on common screen sizes.
-   The complete workflow can be demonstrated using synthetic data.

------------------------------------------------------------------------

## 24. Testing Requirements

### Unit Testing

Test individual:

-   API controllers
-   Utility functions
-   Queue calculations
-   Validation functions
-   ML prediction interface

### Integration Testing

Test:

-   Frontend ↔ Backend
-   Backend ↔ MongoDB
-   Backend ↔ ML service
-   Backend ↔ Socket.io

### System Testing

Test the complete workflow:

``` text
Registration
→ Token Generation
→ Queue Entry
→ Waiting-Time Prediction
→ Queue Update
→ Real-Time Notification
→ Consultation Completion
```

### Model Testing

Evaluate the ML model using appropriate regression metrics and a
separate test dataset.

------------------------------------------------------------------------

## 25. Deployment Requirements

Potential deployment architecture:

``` text
Frontend
   |
   +--> React Application

Backend
   |
   +--> Node.js + Express + Socket.io

Database
   |
   +--> MongoDB

ML Service
   |
   +--> Python Prediction API
```

Possible deployment platforms may be selected during implementation
based on project requirements and availability.

------------------------------------------------------------------------

## 26. Future Enhancements

Possible future enhancements include:

-   Multi-department support
-   Appointment scheduling
-   SMS/email notifications
-   More advanced prediction models
-   Model explainability dashboard
-   Historical queue analytics
-   Priority queue support where appropriate
-   Multi-location support
-   Integration with hospital information systems
-   Continuous model retraining
-   Mobile application
-   Advanced analytics dashboard

These features are outside the initial MVP scope.

------------------------------------------------------------------------

## 27. MVP Definition

The Minimum Viable Product (MVP) will include:

1.  Patient registration
2.  Doctor selection
3.  Token generation
4.  Queue storage
5.  Patient queue dashboard
6.  Doctor queue dashboard
7.  Queue status updates
8.  ML-based waiting-time prediction
9.  Socket.io real-time updates
10. MongoDB persistence
11. Basic authentication/authorization
12. Responsive web interface

------------------------------------------------------------------------

## 28. Development Phases

### Phase 1 --- Planning and Research

-   Finalize requirements
-   Study existing patient queue systems
-   Review relevant literature
-   Define research gap
-   Finalize architecture

### Phase 2 --- Database and Backend

-   Create MongoDB schemas
-   Implement Express server
-   Develop REST APIs
-   Implement authentication
-   Implement queue logic

### Phase 3 --- Frontend

-   Create React application
-   Build patient interface
-   Build doctor dashboard
-   Integrate REST APIs
-   Implement responsive UI

### Phase 4 --- Machine Learning

-   Prepare synthetic dataset
-   Perform data preprocessing
-   Train candidate models
-   Evaluate models
-   Save selected model
-   Create prediction API

### Phase 5 --- Real-Time Integration

-   Integrate Socket.io
-   Implement queue events
-   Update waiting-time predictions dynamically
-   Synchronize patient and doctor dashboards

### Phase 6 --- Testing and Deployment

-   Perform unit testing
-   Perform integration testing
-   Perform system testing
-   Test ML predictions
-   Fix bugs
-   Deploy prototype
-   Prepare final documentation and presentation

------------------------------------------------------------------------

## 29. Research and Academic Considerations

The system is developed as an academic prototype to investigate how
machine learning and real-time web technologies can be combined for
dynamic patient queue and waiting-time prediction.

The project should clearly distinguish between:

-   **Prototype results**
-   **Synthetic-data model performance**
-   **Real-world healthcare performance**

Model results obtained from synthetic data should not be presented as
clinical validation or proof of performance in real hospitals.

------------------------------------------------------------------------

## 30. Glossary

  -----------------------------------------------------------------------
  Term                                Meaning
  ----------------------------------- -----------------------------------
  PRD                                 Product Requirements Document

  MVP                                 Minimum Viable Product

  MERN                                MongoDB, Express.js, React, Node.js

  API                                 Application Programming Interface

  REST API                            Web API using REST architectural
                                      principles

  Socket.io                           Library for real-time bidirectional
                                      communication

  ML                                  Machine Learning

  MAE                                 Mean Absolute Error

  RMSE                                Root Mean Squared Error

  R²                                  Coefficient of Determination

  Synthetic Dataset                   Artificially generated data used
                                      for development/testing

  Token                               Unique number assigned to a patient
                                      in the queue

  Queue Position                      Patient's current position in the
                                      waiting line
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 31. Final Product Requirement Summary

The system shall provide a complete digital workflow for patient queue
registration and tracking while using machine learning to estimate
waiting time dynamically.

The core workflow is:

``` text
Patient Registration
        ↓
Token Generation
        ↓
Queue Entry
        ↓
Feature Collection
        ↓
ML Waiting-Time Prediction
        ↓
Patient Dashboard
        ↓
Real-Time Queue Changes
        ↓
Prediction Update
        ↓
Consultation
        ↓
Queue Completion
```

The primary technical objective is to integrate a **MERN-based web
application**, **Socket.io real-time communication**, **MongoDB data
storage**, and a **Python-based machine learning prediction component**
into one functional academic prototype.

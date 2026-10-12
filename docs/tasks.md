# Project Task Plan

## AI-Based Dynamic Patient Queue and Waiting Time Prediction System

**Document Version:** 1.0\
**Project Type:** Final Year Project\
**Primary Stack:** MERN + Socket.io + Python ML\
**Database:** MongoDB\
**Dataset:** Synthetic Dataset

------------------------------------------------------------------------

# 1. Purpose

This document defines the implementation tasks for the project.

The tasks are organized by:

-   Project setup
-   Database
-   Backend
-   Authentication
-   Queue system
-   Frontend
-   Machine learning
-   Socket.io
-   Integration
-   Testing
-   Deployment
-   Documentation

The project should be developed incrementally. The core queue workflow
should be completed before optional features are added.

------------------------------------------------------------------------

# 2. Task Status Legend

Use the following status values:

``` text
TODO
IN_PROGRESS
BLOCKED
REVIEW
DONE
```

Priority values:

``` text
P0 = Critical
P1 = High
P2 = Medium
P3 = Low
```

------------------------------------------------------------------------

# 3. Phase 0 --- Project Planning

## TASK-001 --- Finalize Project Requirements

**Priority:** P0\
**Status:** DONE

### Description

Finalize the functional and non-functional requirements.

### Checklist

-   [x] Patient registration requirements
-   [x] Token requirements
-   [x] Queue requirements
-   [x] Waiting-time prediction requirements
-   [x] Doctor dashboard requirements
-   [x] Patient dashboard requirements
-   [x] Real-time update requirements
-   [x] Authentication requirements
-   [x] Security requirements

### Deliverable

`prd.md`

------------------------------------------------------------------------

## TASK-002 --- Finalize System Architecture

**Priority:** P0\
**Status:** DONE

### Checklist

-   [x] Frontend architecture
-   [x] Backend architecture
-   [x] Database architecture
-   [x] ML service architecture
-   [x] Socket.io architecture
-   [x] Deployment architecture

### Deliverable

`architecture.md`

------------------------------------------------------------------------

## TASK-003 --- Finalize System Design

**Priority:** P0\
**Status:** DONE

### Checklist

-   [x] Module design
-   [x] API design
-   [x] Queue design
-   [x] UI design
-   [x] ML integration design
-   [x] Error handling design

### Deliverable

`design.md`

------------------------------------------------------------------------

## TASK-004 --- Define Development Rules

**Priority:** P0\
**Status:** DONE

### Deliverable

`rules.md`

------------------------------------------------------------------------

# 4. Phase 1 --- Repository and Development Setup

## TASK-005 --- Create GitHub Repository

**Priority:** P0\
**Status:** TODO

### Checklist

-   [ ] Create repository
-   [ ] Add README
-   [ ] Add `.gitignore`
-   [ ] Add project documentation
-   [ ] Define main branch
-   [ ] Create development/feature branches

------------------------------------------------------------------------

## TASK-006 --- Create Project Directory Structure

**Priority:** P0\
**Status:** TODO

### Target Structure

``` text
project/
│
├── frontend/
├── backend/
├── ml-service/
├── docs/
├── .gitignore
├── README.md
├── prd.md
├── architecture.md
├── design.md
├── rules.md
└── tasks.md
```

------------------------------------------------------------------------

## TASK-007 --- Configure Environment Variables

**Priority:** P0\
**Status:** TODO

### Backend

``` text
PORT
MONGODB_URI
JWT_SECRET
ML_SERVICE_URL
CLIENT_URL
```

### ML Service

``` text
MODEL_PATH
PORT
```

### Checklist

-   [ ] Create `.env`
-   [ ] Add `.env` to `.gitignore`
-   [ ] Create `.env.example`
-   [ ] Verify environment variables load correctly

------------------------------------------------------------------------

# 5. Phase 2 --- Database Development

## TASK-008 --- Configure MongoDB

**Priority:** P0\
**Status:** TODO

### Checklist

-   [ ] Create MongoDB database
-   [ ] Configure connection
-   [ ] Test connection
-   [ ] Handle connection errors

------------------------------------------------------------------------

## TASK-009 --- Create User Schema

**Priority:** P1\
**Status:** TODO

### Fields

``` text
name
email
passwordHash
role
createdAt
```

### Roles

``` text
PATIENT
DOCTOR
STAFF
```

------------------------------------------------------------------------

## TASK-010 --- Create Patient Schema

**Priority:** P0\
**Status:** TODO

### Fields

``` text
name
age
gender
contact
registeredAt
```

### Checklist

-   [ ] Define schema
-   [ ] Add validation
-   [ ] Add timestamps if required
-   [ ] Test create/read operations

------------------------------------------------------------------------

## TASK-011 --- Create Doctor Schema

**Priority:** P0\
**Status:** TODO

### Fields

``` text
name
department
avgConsultTime
isAvailable
shiftStart
shiftEnd
```

### Checklist

-   [ ] Define schema
-   [ ] Add validation
-   [ ] Add sample doctors
-   [ ] Test queries

------------------------------------------------------------------------

## TASK-012 --- Create Queue Schema

**Priority:** P0\
**Status:** TODO

### Fields

``` text
patientId
doctorId
tokenNumber
status
queuePosition
predictedWaitTime
joinedAt
consultationStartedAt
consultationCompletedAt
```

### Status Values

``` text
WAITING
CALLED
IN_CONSULTATION
COMPLETED
CANCELLED
NO_SHOW
```

------------------------------------------------------------------------

## TASK-013 --- Add Database Indexes

**Priority:** P2\
**Status:** TODO

Potential indexes:

``` text
doctorId
patientId
status
tokenNumber
joinedAt
```

Indexes should be added only where they support actual query patterns.

------------------------------------------------------------------------

# 6. Phase 3 --- Backend Foundation

## TASK-014 --- Initialize Node.js Backend

**Priority:** P0\
**Status:** TODO

### Checklist

-   [ ] Initialize npm project
-   [ ] Install Express
-   [ ] Install Mongoose
-   [ ] Install dotenv
-   [ ] Install CORS middleware
-   [ ] Configure server
-   [ ] Add health-check endpoint

------------------------------------------------------------------------

## TASK-015 --- Configure Express Application

**Priority:** P0\
**Status:** TODO

### Checklist

-   [ ] JSON middleware
-   [ ] CORS
-   [ ] Routes
-   [ ] Error middleware
-   [ ] Environment configuration

------------------------------------------------------------------------

## TASK-016 --- Configure Database Connection

**Priority:** P0\
**Status:** TODO

### Checklist

-   [ ] Create `config/db.js`
-   [ ] Connect to MongoDB
-   [ ] Handle connection failure
-   [ ] Test connection

------------------------------------------------------------------------

## TASK-017 --- Create Backend Folder Structure

**Priority:** P0\
**Status:** TODO

``` text
backend/
├── config/
├── controllers/
├── middleware/
├── models/
├── routes/
├── services/
├── sockets/
├── utils/
├── app.js
└── server.js
```

------------------------------------------------------------------------

# 7. Phase 4 --- Authentication and Authorization

## TASK-018 --- Implement User Registration

**Priority:** P1\
**Status:** TODO

### Checklist

-   [ ] Registration API
-   [ ] Input validation
-   [ ] Duplicate email handling
-   [ ] Password hashing
-   [ ] Save user

------------------------------------------------------------------------

## TASK-019 --- Implement Login

**Priority:** P1\
**Status:** TODO

### Checklist

-   [ ] Login endpoint
-   [ ] Verify credentials
-   [ ] Generate authentication token/session
-   [ ] Return user role
-   [ ] Handle invalid credentials

------------------------------------------------------------------------

## TASK-020 --- Implement Authentication Middleware

**Priority:** P1\
**Status:** TODO

### Checklist

-   [ ] Verify authentication
-   [ ] Extract user information
-   [ ] Reject unauthorized requests

------------------------------------------------------------------------

## TASK-021 --- Implement Role-Based Authorization

**Priority:** P1\
**Status:** TODO

### Rules

``` text
PATIENT → Patient operations
DOCTOR  → Doctor/queue operations
STAFF   → Operational queue operations
```

### Checklist

-   [ ] Role middleware
-   [ ] Protect doctor routes
-   [ ] Protect staff routes
-   [ ] Protect patient-specific routes

------------------------------------------------------------------------

# 8. Phase 5 --- Patient Module

## TASK-022 --- Create Patient Registration API

**Priority:** P0\
**Status:** TODO

``` text
POST /api/patients
```

### Checklist

-   [ ] Validate request
-   [ ] Create patient
-   [ ] Return patient ID
-   [ ] Handle duplicate/invalid data

------------------------------------------------------------------------

## TASK-023 --- Create Patient Retrieval API

**Priority:** P1\
**Status:** TODO

``` text
GET /api/patients/:id
```

### Checklist

-   [ ] Authentication
-   [ ] Authorization
-   [ ] Return patient data
-   [ ] Handle missing patient

------------------------------------------------------------------------

## TASK-024 --- Create Patient Registration UI

**Priority:** P0\
**Status:** TODO

### Fields

``` text
Name
Age
Gender
Contact
Doctor
```

### Checklist

-   [ ] Form UI
-   [ ] Client validation
-   [ ] API integration
-   [ ] Loading state
-   [ ] Error state
-   [ ] Success state

------------------------------------------------------------------------

# 9. Phase 6 --- Doctor Module

## TASK-025 --- Create Doctor APIs

**Priority:** P0\
**Status:** TODO

Endpoints:

``` text
GET /api/doctors
GET /api/doctors/:id
PATCH /api/doctors/:id/availability
```

------------------------------------------------------------------------

## TASK-026 --- Create Doctor Dashboard

**Priority:** P0\
**Status:** TODO

### Dashboard should display

``` text
Doctor
Availability
Current Patient
Next Patient
Active Queue
Patient Status
```

------------------------------------------------------------------------

## TASK-027 --- Implement Doctor Availability

**Priority:** P1\
**Status:** TODO

### Checklist

-   [ ] Availability endpoint
-   [ ] Update database
-   [ ] Validate doctor access
-   [ ] Emit real-time update
-   [ ] Trigger prediction update if required

------------------------------------------------------------------------

# 10. Phase 7 --- Token System

## TASK-028 --- Design Token Generation Logic

**Priority:** P0\
**Status:** TODO

### Requirements

-   [ ] Determine latest active token
-   [ ] Generate next token
-   [ ] Prevent active duplicates
-   [ ] Associate token with doctor/queue
-   [ ] Store token in MongoDB

------------------------------------------------------------------------

## TASK-029 --- Implement Token Generation

**Priority:** P0\
**Status:** TODO

### Output

``` json
{
  "tokenNumber": 105,
  "queuePosition": 4
}
```

------------------------------------------------------------------------

## TASK-030 --- Create Token Display UI

**Priority:** P0\
**Status:** TODO

Display:

``` text
Token Number
Queue Position
Current Token
Estimated Wait
Status
```

------------------------------------------------------------------------

# 11. Phase 8 --- Queue Management

## TASK-031 --- Create Queue API

**Priority:** P0\
**Status:** TODO

``` text
POST /api/queue
GET /api/queue/:doctorId
PATCH /api/queue/:id/status
```

------------------------------------------------------------------------

## TASK-032 --- Implement Queue Ordering

**Priority:** P0\
**Status:** TODO

Initial ordering:

``` text
Registration/Queue Entry Time
```

------------------------------------------------------------------------

## TASK-033 --- Implement Queue Status Transitions

**Priority:** P0\
**Status:** TODO

Allowed:

``` text
WAITING → CALLED
CALLED → IN_CONSULTATION
IN_CONSULTATION → COMPLETED
WAITING → CANCELLED
WAITING → NO_SHOW
```

------------------------------------------------------------------------

## TASK-034 --- Implement Queue Position Calculation

**Priority:** P0\
**Status:** TODO

Calculate:

``` text
Patients ahead
Current position
Next patient
```

------------------------------------------------------------------------

## TASK-035 --- Implement Queue Dashboard

**Priority:** P0\
**Status:** TODO

### Checklist

-   [ ] Active queue
-   [ ] Token numbers
-   [ ] Patient status
-   [ ] Current patient
-   [ ] Next patient
-   [ ] Queue position
-   [ ] Estimated waiting time

------------------------------------------------------------------------

# 12. Phase 9 --- Machine Learning Dataset

## TASK-036 --- Define ML Features

**Priority:** P0\
**Status:** TODO

Potential features:

``` text
patientsAhead
queueLength
avgConsultTime
doctorAvailable
consultationState
other validated features
```

The final feature list must be based on the actual synthetic dataset.

------------------------------------------------------------------------

## TASK-037 --- Create/Prepare Synthetic Dataset

**Priority:** P0\
**Status:** TODO

### Checklist

-   [ ] Define synthetic data generation approach
-   [ ] Generate records
-   [ ] Check missing values
-   [ ] Check invalid values
-   [ ] Check feature distributions
-   [ ] Save dataset
-   [ ] Document assumptions

------------------------------------------------------------------------

## TASK-038 --- Perform Exploratory Data Analysis

**Priority:** P1\
**Status:** TODO

Analyze:

-   [ ] Feature distributions
-   [ ] Correlations
-   [ ] Outliers
-   [ ] Target distribution
-   [ ] Feature relationships

------------------------------------------------------------------------

# 13. Phase 10 --- Machine Learning Model

## TASK-039 --- Preprocess Dataset

**Priority:** P0\
**Status:** TODO

### Checklist

-   [ ] Handle missing values
-   [ ] Encode categorical variables where required
-   [ ] Scale features where required
-   [ ] Split dataset
-   [ ] Save preprocessing logic

------------------------------------------------------------------------

## TASK-040 --- Train Baseline Model

**Priority:** P0\
**Status:** TODO

Possible baseline:

``` text
Linear Regression
```

Record:

``` text
MAE
MSE
RMSE
R²
```

------------------------------------------------------------------------

## TASK-041 --- Train Random Forest Model

**Priority:** P1\
**Status:** TODO

### Checklist

-   [ ] Train model
-   [ ] Evaluate model
-   [ ] Record metrics
-   [ ] Compare with baseline

------------------------------------------------------------------------

## TASK-042 --- Experiment with XGBoost/LightGBM

**Priority:** P1\
**Status:** TODO

### Checklist

-   [ ] Train candidate models
-   [ ] Tune selected parameters where appropriate
-   [ ] Evaluate
-   [ ] Compare results
-   [ ] Document experiment

------------------------------------------------------------------------

## TASK-043 --- Select Final Model

**Priority:** P0\
**Status:** TODO

Selection must be based on:

``` text
Evaluation metrics
Model stability
Complexity
Inference requirements
Project constraints
```

Do not select a model only because it produces a visually attractive
result.

------------------------------------------------------------------------

## TASK-044 --- Serialize Final Model

**Priority:** P0\
**Status:** TODO

Possible format:

``` text
model.pkl
```

Also preserve any required preprocessing object.

------------------------------------------------------------------------

# 14. Phase 11 --- ML Prediction Service

## TASK-045 --- Create Python ML Service

**Priority:** P0\
**Status:** TODO

Possible framework:

``` text
FastAPI
```

or

``` text
Flask
```

------------------------------------------------------------------------

## TASK-046 --- Create Prediction Endpoint

**Priority:** P0\
**Status:** TODO

``` text
POST /predict
```

------------------------------------------------------------------------

## TASK-047 --- Validate Prediction Input

**Priority:** P0\
**Status:** TODO

Validate:

``` text
Required fields
Numeric values
Expected ranges
Feature format
```

------------------------------------------------------------------------

## TASK-048 --- Load Model on Service Startup

**Priority:** P0\
**Status:** TODO

The model should be loaded once rather than retrained for each request.

------------------------------------------------------------------------

## TASK-049 --- Test Prediction API

**Priority:** P0\
**Status:** TODO

Test:

-   [ ] Valid request
-   [ ] Missing feature
-   [ ] Invalid feature
-   [ ] Model unavailable
-   [ ] Multiple requests

------------------------------------------------------------------------

# 15. Phase 12 --- Backend and ML Integration

## TASK-050 --- Create Prediction Service in Node.js

**Priority:** P0\
**Status:** TODO

Example:

``` text
services/predictionService.js
```

Responsibilities:

-   Prepare features
-   Call Python API
-   Validate response
-   Handle timeout/failure
-   Return prediction

------------------------------------------------------------------------

## TASK-051 --- Integrate Prediction During Patient Registration

**Priority:** P0\
**Status:** TODO

Flow:

``` text
Register Patient
      ↓
Create Queue Entry
      ↓
Calculate Features
      ↓
Call ML Service
      ↓
Save Prediction
      ↓
Return Result
```

------------------------------------------------------------------------

## TASK-052 --- Integrate Dynamic Prediction Updates

**Priority:** P0\
**Status:** TODO

Trigger prediction updates after relevant queue changes.

------------------------------------------------------------------------

# 16. Phase 13 --- Socket.io Integration

## TASK-053 --- Configure Socket.io Server

**Priority:** P0\
**Status:** TODO

### Checklist

-   [ ] Initialize Socket.io
-   [ ] Configure CORS
-   [ ] Handle connections
-   [ ] Handle disconnects
-   [ ] Define event names

------------------------------------------------------------------------

## TASK-054 --- Implement Queue Events

**Priority:** P0\
**Status:** TODO

Events:

``` text
patient:registered
queue:updated
patient:called
consultation:started
consultation:completed
patient:cancelled
```

------------------------------------------------------------------------

## TASK-055 --- Implement Prediction Event

**Priority:** P1\
**Status:** TODO

``` text
prediction:updated
```

------------------------------------------------------------------------

## TASK-056 --- Implement Frontend Socket Listener

**Priority:** P0\
**Status:** TODO

### Checklist

-   [ ] Connect socket
-   [ ] Listen for queue updates
-   [ ] Update React state
-   [ ] Handle reconnect
-   [ ] Handle disconnect

------------------------------------------------------------------------

# 17. Phase 14 --- Patient Dashboard

## TASK-057 --- Build Patient Dashboard

**Priority:** P0\
**Status:** TODO

Display:

``` text
Token Number
Queue Position
Current Serving Token
Estimated Waiting Time
Doctor
Status
```

------------------------------------------------------------------------

## TASK-058 --- Add Real-Time Queue Updates

**Priority:** P0\
**Status:** TODO

The patient should see relevant queue changes without manually
refreshing the page.

------------------------------------------------------------------------

## TASK-059 --- Add Connection Status

**Priority:** P2\
**Status:** TODO

Optional UI:

``` text
Live Updates Connected
Reconnecting...
```

------------------------------------------------------------------------

# 18. Phase 15 --- Doctor Dashboard

## TASK-060 --- Build Active Queue View

**Priority:** P0\
**Status:** TODO

Display:

``` text
Token
Patient
Status
Queue Position
Estimated Wait
```

------------------------------------------------------------------------

## TASK-061 --- Implement Call Next Patient

**Priority:** P0\
**Status:** TODO

Flow:

``` text
Next WAITING patient
        ↓
CALLED
        ↓
Socket update
```

------------------------------------------------------------------------

## TASK-062 --- Implement Start Consultation

**Priority:** P0\
**Status:** TODO

Flow:

``` text
CALLED
   ↓
IN_CONSULTATION
```

------------------------------------------------------------------------

## TASK-063 --- Implement Complete Consultation

**Priority:** P0\
**Status:** TODO

Flow:

``` text
IN_CONSULTATION
       ↓
COMPLETED
       ↓
Update Queue
       ↓
Update Predictions
       ↓
Emit Socket Event
```

------------------------------------------------------------------------

# 19. Phase 16 --- Staff Features

## TASK-064 --- Build Staff Dashboard

**Priority:** P1\
**Status:** TODO

Display:

``` text
Doctors
Availability
Active Queues
Patient Counts
Queue Status
```

------------------------------------------------------------------------

## TASK-065 --- Staff Patient Registration

**Priority:** P1\
**Status:** TODO

Allow authorized staff to register patients through the same validated
backend flow.

------------------------------------------------------------------------

# 20. Phase 17 --- UI/UX and Responsive Design

## TASK-066 --- Create Common UI Components

**Priority:** P1\
**Status:** TODO

Examples:

``` text
Navbar
Button
Input
Modal
Card
StatusBadge
Loading
ErrorMessage
```

------------------------------------------------------------------------

## TASK-067 --- Apply Responsive Design

**Priority:** P1\
**Status:** TODO

Test:

``` text
Mobile
Tablet
Laptop
Desktop
```

------------------------------------------------------------------------

## TASK-068 --- Improve Loading/Error/Empty States

**Priority:** P1\
**Status:** TODO

Every major API-driven page should handle:

``` text
Loading
Success
Error
Empty
Disconnected
```

where relevant.

------------------------------------------------------------------------

# 21. Phase 18 --- Security Hardening

## TASK-069 --- Review Authentication Security

**Priority:** P0\
**Status:** TODO

### Checklist

-   [ ] Password hashing
-   [ ] Secure token/session handling
-   [ ] Protected routes
-   [ ] Role validation

------------------------------------------------------------------------

## TASK-070 --- Review API Validation

**Priority:** P0\
**Status:** TODO

Check:

-   [ ] Request body validation
-   [ ] URL parameter validation
-   [ ] Query validation
-   [ ] ML input validation

------------------------------------------------------------------------

## TASK-071 --- Review Secret Management

**Priority:** P0\
**Status:** TODO

Verify:

-   [ ] `.env` ignored
-   [ ] No credentials in source
-   [ ] No secrets in Git history
-   [ ] `.env.example` contains placeholders only

------------------------------------------------------------------------

# 22. Phase 19 --- Testing

## TASK-072 --- Backend Unit Tests

**Priority:** P1\
**Status:** TODO

Test:

-   [ ] Token generation
-   [ ] Queue state transitions
-   [ ] Validation
-   [ ] Prediction service
-   [ ] Authentication utilities

------------------------------------------------------------------------

## TASK-073 --- API Integration Tests

**Priority:** P1\
**Status:** TODO

Test:

``` text
Frontend/Client
      ↓
Backend API
      ↓
MongoDB
```

------------------------------------------------------------------------

## TASK-074 --- ML Service Tests

**Priority:** P1\
**Status:** TODO

Test:

-   [ ] Valid prediction
-   [ ] Invalid input
-   [ ] Missing input
-   [ ] Model loading
-   [ ] Error response

------------------------------------------------------------------------

## TASK-075 --- Socket.io Tests

**Priority:** P1\
**Status:** TODO

Test:

-   [ ] Client connection
-   [ ] Queue event
-   [ ] Prediction event
-   [ ] Disconnect
-   [ ] Reconnection

------------------------------------------------------------------------

## TASK-076 --- End-to-End Workflow Test

**Priority:** P0\
**Status:** TODO

Complete workflow:

``` text
Patient Registration
       ↓
Token Generation
       ↓
Queue Entry
       ↓
Prediction
       ↓
Patient Dashboard
       ↓
Doctor Calls Patient
       ↓
Consultation
       ↓
Completion
       ↓
Queue Update
       ↓
Prediction Update
       ↓
Patient Dashboard Update
```

------------------------------------------------------------------------

# 23. Phase 20 --- Performance Testing

## TASK-077 --- Test API Response Performance

**Priority:** P2\
**Status:** TODO

Measure important endpoints.

------------------------------------------------------------------------

## TASK-078 --- Test Prediction Response Time

**Priority:** P2\
**Status:** TODO

Check ML service response time under normal demo load.

------------------------------------------------------------------------

## TASK-079 --- Test Real-Time Update Latency

**Priority:** P2\
**Status:** TODO

Check whether queue updates reach connected clients as expected.

------------------------------------------------------------------------

# 24. Phase 21 --- Deployment

## TASK-080 --- Prepare Frontend Deployment

**Priority:** P1\
**Status:** TODO

### Checklist

-   [ ] Production build
-   [ ] Environment variables
-   [ ] API URL configuration
-   [ ] Test deployed frontend

------------------------------------------------------------------------

## TASK-081 --- Prepare Backend Deployment

**Priority:** P1\
**Status:** TODO

### Checklist

-   [ ] Production environment
-   [ ] Environment variables
-   [ ] CORS configuration
-   [ ] Database connection
-   [ ] Socket.io configuration
-   [ ] Health check

------------------------------------------------------------------------

## TASK-082 --- Deploy ML Service

**Priority:** P1\
**Status:** TODO

### Checklist

-   [ ] Package dependencies
-   [ ] Include model
-   [ ] Configure model path
-   [ ] Configure API
-   [ ] Test prediction endpoint

------------------------------------------------------------------------

## TASK-083 --- Connect Deployed Services

**Priority:** P1\
**Status:** TODO

``` text
Frontend
   ↓
Backend
   ↓
MongoDB

Backend
   ↓
ML Service
```

------------------------------------------------------------------------

# 25. Phase 22 --- Documentation

## TASK-084 --- Update README

**Priority:** P1\
**Status:** TODO

README should include:

-   Project overview
-   Features
-   Architecture
-   Technology stack
-   Setup instructions
-   Environment variables
-   Running instructions
-   API overview
-   ML overview
-   Screenshots where appropriate

------------------------------------------------------------------------

## TASK-085 --- Update PRD

**Priority:** P1\
**Status:** TODO

Update requirements when approved project scope changes.

------------------------------------------------------------------------

## TASK-086 --- Update Architecture Document

**Priority:** P1\
**Status:** TODO

Update:

``` text
architecture.md
```

when major architecture decisions change.

------------------------------------------------------------------------

## TASK-087 --- Update Design Document

**Priority:** P1\
**Status:** TODO

Update:

``` text
design.md
```

when database, API, UI, or module design changes.

------------------------------------------------------------------------

## TASK-088 --- Update Rules

**Priority:** P2\
**Status:** TODO

Update:

``` text
rules.md
```

if development standards change.

------------------------------------------------------------------------

# 26. Phase 23 --- Final Academic Validation

## TASK-089 --- Verify Synthetic Dataset Statement

**Priority:** P0\
**Status:** TODO

Verify that all documentation correctly states that the ML model uses
synthetic data.

------------------------------------------------------------------------

## TASK-090 --- Verify No Clinical Claims

**Priority:** P0\
**Status:** TODO

Search:

``` text
README
Report
PPT
Code comments
Documentation
```

for unsupported claims about clinical validation.

------------------------------------------------------------------------

## TASK-091 --- Verify Research References

**Priority:** P1\
**Status:** TODO

Check:

-   [ ] Paper titles
-   [ ] Authors
-   [ ] Publication details
-   [ ] Research gap claims
-   [ ] Citations

------------------------------------------------------------------------

## TASK-092 --- Prepare Final Demo Scenario

**Priority:** P0\
**Status:** TODO

Create a predictable demo:

``` text
1. Login/Register
2. Register patient
3. Generate token
4. Show predicted wait
5. Open doctor dashboard
6. Call patient
7. Start consultation
8. Complete consultation
9. Show queue update
10. Show updated prediction
```

------------------------------------------------------------------------

# 27. Phase 24 --- Final Release Checklist

## Application

-   [ ] Patient registration works.
-   [ ] Doctor selection works.
-   [ ] Token generation works.
-   [ ] Queue management works.
-   [ ] Queue status transitions work.
-   [ ] Patient dashboard works.
-   [ ] Doctor dashboard works.
-   [ ] Staff dashboard works if included.
-   [ ] Waiting-time prediction works.
-   [ ] Dynamic prediction updates work.
-   [ ] Socket.io works.
-   [ ] Authentication works.
-   [ ] Authorization works.
-   [ ] MongoDB persistence works.

## ML

-   [ ] Synthetic dataset prepared.
-   [ ] Data preprocessing completed.
-   [ ] Candidate models evaluated.
-   [ ] Final model selected.
-   [ ] Model serialized.
-   [ ] Prediction API works.
-   [ ] Backend integration works.
-   [ ] Evaluation metrics documented.

## Security

-   [ ] No secrets committed.
-   [ ] Passwords hashed.
-   [ ] Protected APIs secured.
-   [ ] Server-side validation implemented.
-   [ ] Error messages are safe.
-   [ ] CORS reviewed.

## Quality

-   [ ] Unit tests pass.
-   [ ] Integration tests pass.
-   [ ] End-to-end workflow passes.
-   [ ] Responsive UI verified.
-   [ ] Socket reconnection tested.
-   [ ] ML failure tested.
-   [ ] Database failure handling tested.

## Documentation

-   [ ] README complete.
-   [ ] PRD updated.
-   [ ] Architecture updated.
-   [ ] Design updated.
-   [ ] Rules updated.
-   [ ] Tasks updated.
-   [ ] API documentation updated.
-   [ ] ML experiment documentation complete.

------------------------------------------------------------------------

# 28. Suggested Development Order

The recommended implementation order is:

``` text
1. Repository Setup
       ↓
2. MongoDB + Schemas
       ↓
3. Express Backend
       ↓
4. Authentication
       ↓
5. Patient Registration
       ↓
6. Token Generation
       ↓
7. Queue Management
       ↓
8. Patient Dashboard
       ↓
9. Doctor Dashboard
       ↓
10. Synthetic Dataset
       ↓
11. ML Model
       ↓
12. Python Prediction API
       ↓
13. Backend ↔ ML Integration
       ↓
14. Socket.io Integration
       ↓
15. Dynamic Prediction Updates
       ↓
16. Responsive UI
       ↓
17. Testing
       ↓
18. Deployment
       ↓
19. Documentation
       ↓
20. Final Demo
```

------------------------------------------------------------------------

# 29. Task Tracking Template

Use this format for future tasks:

``` markdown
## TASK-XXX — Task Name

**Priority:** P0/P1/P2/P3  
**Status:** TODO/IN_PROGRESS/BLOCKED/REVIEW/DONE  
**Owner:** Team Member  
**Depends On:** TASK-XXX

### Description

What needs to be implemented.

### Checklist

- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

### Acceptance Criteria

- [ ] Expected result 1
- [ ] Expected result 2

### Notes

Additional implementation information.
```

------------------------------------------------------------------------

# 30. Definition of Done

A task should be marked `DONE` only when:

``` text
Requirement understood
        ↓
Implementation completed
        ↓
Validation completed
        ↓
Error cases considered
        ↓
Testing completed
        ↓
Code reviewed
        ↓
Documentation updated if required
        ↓
Committed to Git
```

------------------------------------------------------------------------

# 31. Current Project Task Snapshot

Based on the project documentation created so far:

  Area                      Status
  ------------------------- --------
  Requirements              DONE
  Architecture              DONE
  System Design             DONE
  Development Rules         DONE
  Repository Setup          TODO
  Database Implementation   TODO
  Backend Implementation    TODO
  Authentication            TODO
  Patient Module            TODO
  Doctor Module             TODO
  Queue Module              TODO
  ML Dataset                TODO
  ML Model                  TODO
  Python ML API             TODO
  Backend-ML Integration    TODO
  Socket.io Integration     TODO
  Frontend Dashboards       TODO
  Testing                   TODO
  Deployment                TODO
  Final Documentation       TODO

------------------------------------------------------------------------

# 32. Final Project Goal

The final implementation should demonstrate this complete workflow:

``` text
                 PATIENT
                    |
                    v
           Patient Registration
                    |
                    v
              Token Generation
                    |
                    v
               Join Queue
                    |
                    v
          Waiting-Time Prediction
                    |
                    v
           Patient Dashboard
                    |
              Real-Time Updates
                    |
                    v
              Doctor Dashboard
                    |
                    v
             Call Patient
                    |
                    v
          Start Consultation
                    |
                    v
         Complete Consultation
                    |
                    v
             Queue Updated
                    |
                    v
        Predictions Recalculated
                    |
                    v
            Clients Updated
```

The implementation should prioritize a stable, demonstrable core
workflow over unnecessary additional features.

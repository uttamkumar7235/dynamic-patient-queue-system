# Project Rules

## AI-Based Dynamic Patient Queue and Waiting Time Prediction System

**Document Version:** 1.0\
**Project Type:** Final Year Project\
**Primary Stack:** MERN + Socket.io + Python ML\
**Database:** MongoDB\
**Dataset:** Synthetic Dataset

------------------------------------------------------------------------

# 1. Purpose

This document defines the development, coding, architecture, data,
security, UI, Git, testing, and documentation rules that should be
followed while building the project.

The purpose is to keep the codebase:

-   Consistent
-   Maintainable
-   Secure
-   Easy to understand
-   Easy to test
-   Easy to extend
-   Suitable for an academic final-year project

These rules apply to all future implementation unless a specific
requirement explicitly changes them.

------------------------------------------------------------------------

# 2. Core Project Rules

## Rule 1 --- Keep the Architecture Modular

The project must maintain a clear separation between:

``` text
Frontend
Backend
Database
Real-Time Communication
Machine Learning
```

Do not place unrelated responsibilities in the same file or module.

------------------------------------------------------------------------

## Rule 2 --- Use the MERN Stack for the Main Web Application

The main application must use:

-   MongoDB
-   Express.js
-   React.js
-   Node.js

Socket.io should be used for real-time queue communication.

Python should be used specifically for the machine learning/prediction
component.

------------------------------------------------------------------------

## Rule 3 --- Node.js Backend Is the Main Application Coordinator

The React frontend must not directly communicate with:

-   MongoDB
-   Python model files
-   Internal ML implementation

The normal flow should be:

``` text
React
  ↓
Node.js / Express
  ↓
MongoDB / ML Service
```

------------------------------------------------------------------------

## Rule 4 --- Keep the ML Service Separate

Machine learning code should remain separate from the Node.js
application.

Recommended structure:

``` text
Frontend
    ↓
Node.js Backend
    ↓
Python ML API
    ↓
Trained Model
```

Do not place Python model-training logic inside the React or Node.js
codebase.

------------------------------------------------------------------------

# 3. Project Scope Rules

## Rule 5 --- Do Not Expand the MVP Unnecessarily

The initial MVP should focus on:

1.  Patient registration
2.  Doctor selection
3.  Token generation
4.  Queue management
5.  Patient dashboard
6.  Doctor dashboard
7.  Waiting-time prediction
8.  Socket.io real-time updates
9.  MongoDB persistence
10. Basic authentication/authorization
11. Responsive UI

Additional features should be added only after the core workflow is
stable.

------------------------------------------------------------------------

## Rule 6 --- No Medical Diagnosis

The system must not be presented as a medical diagnosis or treatment
system.

The ML component is only intended for:

``` text
Waiting-Time Prediction
```

It must not provide:

-   Diagnosis
-   Treatment recommendations
-   Medical prescriptions
-   Clinical decisions

------------------------------------------------------------------------

## Rule 7 --- No Claims of Clinical Validation

The project uses a **synthetic dataset**.

Therefore, documentation, presentations, reports, and README files must
not claim:

-   Real hospital validation
-   Clinical validation
-   Real patient-data validation
-   Proven hospital-level accuracy
-   Production healthcare deployment

Model results must be described as results obtained from the synthetic
dataset.

------------------------------------------------------------------------

# 4. Data Rules

## Rule 8 --- Use Synthetic Data

The ML development dataset must be synthetic.

Do not introduce real patient medical records into the project
repository.

------------------------------------------------------------------------

## Rule 9 --- Do Not Commit Sensitive Data

Never commit:

``` text
Passwords
API Keys
JWT Secrets
Database Credentials
Private Tokens
Real Patient Data
```

to GitHub.

------------------------------------------------------------------------

## Rule 10 --- Use Environment Variables

Sensitive configuration should be stored in `.env`.

Example:

``` env
PORT=5000
MONGODB_URI=your_database_url
JWT_SECRET=your_secret
ML_SERVICE_URL=http://localhost:8000
CLIENT_URL=http://localhost:5173
```

The `.env` file must be included in `.gitignore`.

------------------------------------------------------------------------

# 5. Database Rules

## Rule 11 --- Use MongoDB Through Mongoose

The Node.js backend should use Mongoose for:

-   Schema definitions
-   Validation
-   Database queries
-   Relationships/references

------------------------------------------------------------------------

## Rule 12 --- Keep Schemas Explicit

Important fields should have clear types and validation.

Example:

``` js
const queueSchema = new mongoose.Schema({
  patientId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "Patient",
    required: true
  },

  doctorId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "Doctor",
    required: true
  },

  tokenNumber: {
    type: Number,
    required: true
  },

  status: {
    type: String,
    enum: ["WAITING", "CALLED", "IN_CONSULTATION", "COMPLETED", "CANCELLED", "NO_SHOW"],
    default: "WAITING"
  }
});
```

------------------------------------------------------------------------

## Rule 13 --- Use References Consistently

Use MongoDB references for entities such as:

``` text
Patient → Queue
Doctor → Queue
User → Role
```

Do not duplicate large amounts of the same data unnecessarily.

------------------------------------------------------------------------

## Rule 14 --- Protect Queue State

Queue status must be updated through backend business logic.

The frontend must not be allowed to arbitrarily modify queue state
without server validation.

------------------------------------------------------------------------

# 6. Queue Rules

## Rule 15 --- Validate Queue State Transitions

Allowed primary flow:

``` text
WAITING
   ↓
CALLED
   ↓
IN_CONSULTATION
   ↓
COMPLETED
```

Alternative:

``` text
WAITING → CANCELLED
WAITING → NO_SHOW
```

Invalid transitions should be rejected.

------------------------------------------------------------------------

## Rule 16 --- Queue Order Must Be Deterministic

For the initial implementation, patients should generally be ordered
according to registration/queue entry time for the selected doctor.

Example:

``` text
Token 101
Token 102
Token 103
```

Do not randomly reorder the queue.

------------------------------------------------------------------------

## Rule 17 --- Token Numbers Must Not Conflict

The system must avoid duplicate active token numbers within the same
doctor/queue context.

Token generation must be handled on the server.

------------------------------------------------------------------------

## Rule 18 --- Queue Changes Must Trigger Required Updates

Important queue events include:

-   Patient registration
-   Patient cancellation
-   Consultation start
-   Consultation completion
-   No-show
-   Doctor availability change

These events should trigger appropriate queue and prediction updates.

------------------------------------------------------------------------

# 7. Waiting-Time Prediction Rules

## Rule 19 --- Waiting Time Is an Estimate

The UI and documentation should use language such as:

``` text
Estimated Waiting Time
Predicted Waiting Time
Expected Waiting Time
```

Avoid presenting the prediction as a guaranteed time.

------------------------------------------------------------------------

## Rule 20 --- Prediction Must Use Validated Features

Only features supported by the final dataset/model should be sent to the
ML service.

Potential features include:

``` text
Patients Ahead
Queue Length
Average Consultation Time
Doctor Availability
Current Consultation State
Other Dataset-Supported Features
```

Do not invent model inputs simply for UI purposes.

------------------------------------------------------------------------

## Rule 21 --- Use the Same Preprocessing During Inference

The preprocessing applied during model training must be consistent with
the preprocessing used when making predictions.

Example:

``` text
Training Data
    ↓
Preprocessing
    ↓
Model Training

Live Input
    ↓
Same Preprocessing
    ↓
Model Prediction
```

------------------------------------------------------------------------

## Rule 22 --- Do Not Retrain the Model During Every Prediction

The production/demo prediction flow should:

``` text
Load Trained Model
        ↓
Receive Features
        ↓
Predict
        ↓
Return Result
```

Training should be a separate process.

------------------------------------------------------------------------

## Rule 23 --- Document Model Performance Honestly

If the model achieves a particular MAE/RMSE/R² score, report it with:

-   Dataset context
-   Test methodology
-   Model name
-   Evaluation metric

Do not generalize synthetic-data performance to real hospitals.

------------------------------------------------------------------------

# 8. Backend Coding Rules

## Rule 24 --- Follow Layered Backend Structure

Use:

``` text
Routes
Controllers
Services
Models
Middleware
Utilities
Sockets
```

Recommended flow:

``` text
Route
  ↓
Controller
  ↓
Service
  ↓
Model / External Service
```

------------------------------------------------------------------------

## Rule 25 --- Keep Controllers Small

Controllers should coordinate requests and responses.

Business logic should preferably be placed in services.

Avoid putting large amounts of queue or ML logic directly inside route
handlers.

------------------------------------------------------------------------

## Rule 26 --- Use Async/Await

Prefer:

``` js
const patient = await Patient.findById(id);
```

instead of deeply nested callbacks.

Always handle asynchronous errors appropriately.

------------------------------------------------------------------------

## Rule 27 --- Use Centralized Error Handling

Use a global Express error handler rather than writing inconsistent
error responses throughout the application.

------------------------------------------------------------------------

## Rule 28 --- Validate Server-Side

Frontend validation is useful for user experience, but it is not a
security boundary.

Every important input must also be validated on the backend.

------------------------------------------------------------------------

## Rule 29 --- Use Meaningful HTTP Status Codes

Examples:

``` text
200 → Successful request
201 → Resource created
400 → Invalid request
401 → Authentication required/failed
403 → Access denied
404 → Resource not found
409 → Conflict
500 → Internal server error
```

------------------------------------------------------------------------

# 9. API Rules

## Rule 30 --- Use RESTful API Naming

Prefer:

``` text
/api/patients
/api/doctors
/api/queue
/api/auth
```

Avoid unnecessarily inconsistent endpoint names.

------------------------------------------------------------------------

## Rule 31 --- Use Consistent Responses

Success:

``` json
{
  "success": true,
  "message": "Operation successful",
  "data": {}
}
```

Error:

``` json
{
  "success": false,
  "message": "Something went wrong"
}
```

------------------------------------------------------------------------

## Rule 32 --- Do Not Expose Internal Errors

Do not return:

``` text
Database connection strings
Stack traces
Secret values
Internal filesystem paths
Private credentials
```

to the client.

------------------------------------------------------------------------

# 10. Frontend Rules

## Rule 33 --- Use React Components

Break the UI into reusable components.

Examples:

``` text
Navbar
QueueCard
TokenCard
DoctorCard
Loading
ErrorMessage
StatusBadge
```

------------------------------------------------------------------------

## Rule 34 --- Avoid Large Monolithic Components

If a component becomes difficult to understand, divide it into smaller
components.

For example:

``` text
DoctorDashboard
├── DoctorHeader
├── CurrentPatient
├── QueueList
└── QueueActions
```

------------------------------------------------------------------------

## Rule 35 --- Keep API Logic Separate

API calls should preferably be placed in:

``` text
services/
```

rather than scattered throughout UI components.

Example:

``` js
patientService.registerPatient()
queueService.getQueue()
doctorService.updateAvailability()
```

------------------------------------------------------------------------

## Rule 36 --- Use Clear UI States

The frontend should handle:

``` text
Loading
Success
Error
Empty
Disconnected
```

states where applicable.

------------------------------------------------------------------------

## Rule 37 --- Make the UI Responsive

The application must support:

``` text
Mobile
Tablet
Laptop
Desktop
```

Important patient information should remain easy to read on small
screens.

------------------------------------------------------------------------

# 11. Socket.io Rules

## Rule 38 --- Use Socket.io Only for Real-Time Events

Socket.io should handle events such as:

``` text
queue:updated
patient:registered
patient:called
consultation:started
consultation:completed
prediction:updated
doctor:availabilityChanged
```

Do not replace every REST API with Socket.io unnecessarily.

------------------------------------------------------------------------

## Rule 39 --- REST + Socket.io Should Work Together

Recommended pattern:

``` text
REST API
    ↓
Initial Data

Socket.io
    ↓
Live Changes
```

If the socket disconnects, the client should be able to retrieve the
latest state through REST.

------------------------------------------------------------------------

## Rule 40 --- Handle Socket Reconnection

The frontend should handle temporary socket disconnections gracefully.

After reconnection:

``` text
Reconnect
   ↓
Fetch Latest Queue State
   ↓
Synchronize UI
```

------------------------------------------------------------------------

# 12. Authentication and Authorization Rules

## Rule 41 --- Never Store Plain-Text Passwords

Passwords must be securely hashed.

------------------------------------------------------------------------

## Rule 42 --- Protect Sensitive Routes

Examples:

``` text
Doctor queue controls
Staff operations
User account operations
```

must require authentication and appropriate authorization.

------------------------------------------------------------------------

## Rule 43 --- Enforce Roles on the Backend

Do not rely only on frontend route hiding.

The backend must verify:

``` text
Is the user authenticated?
        ↓
What is the user's role?
        ↓
Is this operation allowed?
```

------------------------------------------------------------------------

# 13. Security Rules

## Rule 44 --- Validate All External Input

Validate:

-   Request body
-   URL parameters
-   Query parameters
-   Authentication data
-   ML input

------------------------------------------------------------------------

## Rule 45 --- Avoid Hard-Coded Secrets

Bad:

``` js
const jwtSecret = "my-secret-123";
```

Good:

``` js
const jwtSecret = process.env.JWT_SECRET;
```

------------------------------------------------------------------------

## Rule 46 --- Configure CORS Properly

Do not use unrestricted CORS in a production deployment unless there is
a documented reason.

------------------------------------------------------------------------

## Rule 47 --- Keep Dependencies Updated

Use stable versions of required packages and remove unused dependencies.

------------------------------------------------------------------------

# 14. ML Service Rules

## Rule 48 --- Keep the ML API Simple

The ML API should have a clear contract.

Example:

``` text
POST /predict
```

Input:

``` json
{
  "patientsAhead": 5,
  "queueLength": 8,
  "avgConsultTime": 12,
  "doctorAvailable": 1
}
```

Output:

``` json
{
  "predictedWaitTime": 58
}
```

------------------------------------------------------------------------

## Rule 49 --- Validate ML Input

The ML service must reject:

-   Missing required features
-   Invalid numeric values
-   Unexpected formats
-   Impossible values where validation rules are defined

------------------------------------------------------------------------

## Rule 50 --- Return Controlled ML Errors

If the model cannot produce a prediction:

``` json
{
  "success": false,
  "message": "Prediction unavailable"
}
```

Do not expose internal Python stack traces to the frontend.

------------------------------------------------------------------------

# 15. File and Folder Naming Rules

Use clear and consistent naming.

## JavaScript/React

Prefer:

``` text
PatientDashboard.jsx
DoctorDashboard.jsx
QueueCard.jsx
queueService.js
authController.js
```

## Python

Prefer:

``` text
model.py
predict.py
preprocess.py
train.py
```

## Markdown

Use lowercase names for project documentation:

``` text
prd.md
architecture.md
design.md
rules.md
README.md
```

------------------------------------------------------------------------

# 16. Code Style Rules

## Rule 51 --- Use Meaningful Names

Avoid:

``` js
let x;
let a;
let temp;
```

Prefer:

``` js
let queuePosition;
let predictedWaitTime;
let doctorId;
```

------------------------------------------------------------------------

## Rule 52 --- Keep Functions Focused

A function should ideally perform one clear task.

Bad:

``` text
registerPatientAndTrainModelAndSendEmailAndUpdateDoctorAnd...
```

Better:

``` text
registerPatient()
generateToken()
predictWaitingTime()
notifyQueueUpdate()
```

------------------------------------------------------------------------

## Rule 53 --- Avoid Unnecessary Duplication

If the same logic appears multiple times, consider extracting it into a
utility or service.

------------------------------------------------------------------------

## Rule 54 --- Comment Why, Not Obvious What

Avoid:

``` js
// Increment i
i++;
```

Prefer comments that explain non-obvious business decisions.

------------------------------------------------------------------------

# 17. Git and GitHub Rules

## Rule 55 --- Use Git Frequently

Make small, meaningful commits.

Examples:

``` text
feat: add patient registration API
feat: implement token generation
feat: add queue dashboard
fix: correct queue status transition
fix: handle ML service timeout
docs: update architecture
```

------------------------------------------------------------------------

## Rule 56 --- Do Not Commit Generated or Secret Files

`.gitignore` should include items such as:

``` text
node_modules/
.env
dist/
build/
__pycache__/
*.pyc
.venv/
```

Model files should only be committed if intentionally required by the
project and appropriately sized/licensed.

------------------------------------------------------------------------

## Rule 57 --- Keep Main Branch Stable

Use a development/feature branch for significant changes.

Example:

``` text
main
  |
  +-- feature/patient-registration
  |
  +-- feature/queue-management
  |
  +-- feature/ml-prediction
```

Merge tested changes into `main`.

------------------------------------------------------------------------

# 18. Testing Rules

## Rule 58 --- Test New Features

Every major feature should have at least basic testing.

Examples:

``` text
Patient registration
Token generation
Queue transitions
Prediction API
Authentication
Socket events
```

------------------------------------------------------------------------

## Rule 59 --- Test Failure Cases

Do not test only successful scenarios.

Test:

``` text
Invalid input
Missing data
Unauthorized request
Non-existent patient
Invalid queue transition
ML service unavailable
Database unavailable
Socket disconnect
```

------------------------------------------------------------------------

## Rule 60 --- Test the Complete Workflow

The main end-to-end workflow should work:

``` text
Register Patient
      ↓
Generate Token
      ↓
Join Queue
      ↓
Predict Wait Time
      ↓
Display Patient Dashboard
      ↓
Doctor Calls Patient
      ↓
Consultation Starts
      ↓
Consultation Completes
      ↓
Queue Updates
      ↓
Predictions Update
```

------------------------------------------------------------------------

# 19. Documentation Rules

## Rule 61 --- Keep Documentation Updated

When architecture or important functionality changes, update relevant
documentation.

Important documents include:

``` text
README.md
prd.md
architecture.md
design.md
rules.md
```

------------------------------------------------------------------------

## Rule 62 --- Document Important API Changes

If an endpoint changes, update API documentation.

------------------------------------------------------------------------

## Rule 63 --- Document ML Experiments

For each important ML experiment, record:

``` text
Dataset version
Features
Model
Hyperparameters
Evaluation metrics
Results
Observations
```

Do not report only the best-looking result without context.

------------------------------------------------------------------------

# 20. UI/UX Rules

## Rule 64 --- Keep the Patient Interface Simple

The patient should quickly understand:

``` text
Your Token
Queue Position
Current Token
Estimated Waiting Time
Status
```

------------------------------------------------------------------------

## Rule 65 --- Use Clear Status Labels

Recommended:

``` text
Waiting
Called
In Consultation
Completed
Cancelled
No-show
```

Avoid confusing technical terms in the patient-facing UI.

------------------------------------------------------------------------

## Rule 66 --- Show Prediction as an Estimate

Example:

``` text
Estimated waiting time: 38 minutes
```

Avoid:

``` text
You will be seen exactly at 10:38 AM
```

unless the system actually supports appointment-time guarantees.

------------------------------------------------------------------------

# 21. Performance Rules

## Rule 67 --- Avoid Unnecessary Database Queries

Use efficient queries and appropriate indexes.

------------------------------------------------------------------------

## Rule 68 --- Do Not Retrain During Normal Requests

The prediction service should load an existing trained model.

------------------------------------------------------------------------

## Rule 69 --- Avoid Excessive Socket Events

Emit events only when relevant state changes occur.

------------------------------------------------------------------------

## Rule 70 --- Keep API Responses Focused

Return only the information needed by the client.

------------------------------------------------------------------------

# 22. Error and Failure Rules

## Rule 71 --- Never Let One Failure Crash the Whole Application

For example:

``` text
ML Service Down
```

should not automatically crash:

``` text
Node.js Server
```

The system should handle the failure gracefully.

------------------------------------------------------------------------

## Rule 72 --- Provide User-Friendly Errors

Instead of:

``` text
ECONNREFUSED 127.0.0.1:8000
```

the user-facing message can be:

``` text
Waiting-time prediction is temporarily unavailable.
```

Technical details belong in server logs.

------------------------------------------------------------------------

# 23. Academic Project Rules

## Rule 73 --- Be Accurate in Reports and Presentations

Use:

``` text
Synthetic Dataset
ML-based waiting-time prediction
Academic prototype
Experimental evaluation
```

Do not claim:

``` text
Clinically validated
Hospital-proven
Real patient accuracy
Production-ready healthcare system
```

unless such evidence actually exists.

------------------------------------------------------------------------

## Rule 74 --- Clearly State Limitations

The project documentation should acknowledge:

-   Synthetic dataset
-   Limited real-world representation
-   No clinical validation
-   Prediction uncertainty
-   Academic prototype scope

------------------------------------------------------------------------

## Rule 75 --- Keep Research Claims Traceable

Any important claim about existing research should be supported by the
corresponding paper or reliable source.

Do not invent:

-   Research results
-   Accuracy values
-   Dataset sizes
-   Hospital deployments
-   Literature findings

------------------------------------------------------------------------

# 24. Development Workflow Rules

Use the following general workflow:

``` text
Requirement
    ↓
Design
    ↓
Implementation
    ↓
Testing
    ↓
Review
    ↓
Documentation
    ↓
Commit
```

For a new feature:

``` text
1. Understand requirement
2. Check architecture
3. Design database/API changes
4. Implement backend
5. Implement frontend
6. Integrate ML/Socket.io if required
7. Test
8. Fix errors
9. Update documentation
10. Commit changes
```

------------------------------------------------------------------------

# 25. Definition of Done

A feature is considered complete only when:

-   [ ] Requirement is understood.
-   [ ] Design is defined.
-   [ ] Backend is implemented.
-   [ ] Frontend is implemented.
-   [ ] Database changes are complete.
-   [ ] Validation is implemented.
-   [ ] Error handling is implemented.
-   [ ] Authentication/authorization is handled where required.
-   [ ] Real-time behavior is tested where required.
-   [ ] ML integration is tested where required.
-   [ ] Responsive UI is verified.
-   [ ] Basic testing is complete.
-   [ ] Documentation is updated.
-   [ ] Code is committed to Git.

------------------------------------------------------------------------

# 26. Do Not Do These Things

The following practices should be avoided:

``` text
❌ Hard-code passwords or API keys
❌ Store plain-text passwords
❌ Access MongoDB directly from React
❌ Put ML training inside API requests
❌ Put all backend logic inside one file
❌ Allow arbitrary queue-state changes from the frontend
❌ Claim synthetic-data results are clinical validation
❌ Commit .env files
❌ Ignore server-side validation
❌ Expose stack traces to users
❌ Use random queue ordering
❌ Add unnecessary features before the MVP works
❌ Copy code without understanding its purpose
❌ Leave broken/debug code in production paths
```

------------------------------------------------------------------------

# 27. Preferred Practices

``` text
✅ Modular architecture
✅ Clear folder structure
✅ Server-side validation
✅ Secure authentication
✅ Role-based authorization
✅ Consistent API responses
✅ Centralized error handling
✅ Socket.io for live queue changes
✅ Python service for ML prediction
✅ Synthetic dataset for experiments
✅ Honest reporting of ML performance
✅ Meaningful Git commits
✅ Responsive UI
✅ Automated/basic testing
✅ Updated documentation
```

------------------------------------------------------------------------

# 28. Priority Order for Development

When deciding what to implement first, follow:

``` text
Priority 1
Core Queue Workflow
        ↓
Priority 2
Database + Backend APIs
        ↓
Priority 3
Patient/Doctor UI
        ↓
Priority 4
Authentication
        ↓
Priority 5
ML Prediction
        ↓
Priority 6
Socket.io Real-Time Updates
        ↓
Priority 7
Testing + Error Handling
        ↓
Priority 8
UI Refinement + Documentation
```

The exact order can be adjusted when technical dependencies require it.

------------------------------------------------------------------------

# 29. Final Project Rule

The project should always remain centered around its primary objective:

> **Providing a digital patient queue with dynamic
> machine-learning-based waiting-time prediction and real-time queue
> updates.**

Every new feature should be evaluated against:

``` text
Does it support the core project?
        |
       Yes
        ↓
Implement if useful.

       No
        ↓
Keep it out of the MVP unless there is a clear reason.
```

------------------------------------------------------------------------

# 30. Final Checklist

Before final submission:

## Application

-   [ ] Patient registration works.
-   [ ] Token generation works.
-   [ ] Queue management works.
-   [ ] Doctor dashboard works.
-   [ ] Patient dashboard works.
-   [ ] Waiting-time prediction works.
-   [ ] Socket.io updates work.
-   [ ] Authentication works.
-   [ ] Authorization works.
-   [ ] MongoDB persistence works.
-   [ ] Error handling works.
-   [ ] Responsive UI works.

## ML

-   [ ] Synthetic dataset documented.
-   [ ] Preprocessing documented.
-   [ ] Model training documented.
-   [ ] Evaluation metrics documented.
-   [ ] Selected model documented.
-   [ ] Prediction API works.
-   [ ] Limitations documented.

## Security

-   [ ] No secrets in GitHub.
-   [ ] Passwords are hashed.
-   [ ] Protected APIs are secured.
-   [ ] Server-side validation exists.
-   [ ] Sensitive logs are avoided.

## Code Quality

-   [ ] Modular folder structure.
-   [ ] Meaningful names.
-   [ ] No unnecessary duplication.
-   [ ] No unused debug code.
-   [ ] Consistent API responses.
-   [ ] Proper error handling.

## Documentation

-   [ ] README updated.
-   [ ] PRD updated.
-   [ ] Architecture document updated.
-   [ ] Design document updated.
-   [ ] Rules document updated.
-   [ ] API documentation updated.
-   [ ] ML experiment results documented.

------------------------------------------------------------------------

# 31. Final Summary

These rules establish a consistent development standard for the
**AI-Based Dynamic Patient Queue and Waiting Time Prediction System**.

The most important principles are:

``` text
MERN for the main web application
        +
Socket.io for real-time communication
        +
MongoDB for persistent data
        +
Python for ML prediction
        +
Synthetic data for ML experiments
        +
Secure and modular development
        +
Honest academic reporting
```

The system should be developed incrementally, with the core queue
workflow implemented and tested before adding optional features.

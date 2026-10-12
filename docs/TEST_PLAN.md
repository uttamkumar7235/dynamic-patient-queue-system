# Test Plan

## 1. Purpose

This document defines what **"working"** means for the AI Based Dynamic
Patient Queue And Waiting Time Prediction System.

The goal is to verify that the system works correctly across
authentication, patient registration, doctor availability, queue
handling, waiting-time prediction, real-time updates, authorization,
validation, error handling, and responsive UI.

Testing should confirm that implemented features behave according to the
project requirements and documented architecture.

------------------------------------------------------------------------

## 2. Testing Scope

The following areas are included:

-   Authentication
-   Authorization and role-based access
-   Patient registration
-   Doctor data and availability
-   Token generation
-   Queue creation and ordering
-   Queue status transitions
-   Waiting-time prediction
-   Python ML API
-   MongoDB data persistence
-   REST APIs
-   Socket.io real-time updates
-   Frontend functionality
-   Validation and error handling
-   Responsive design
-   Basic security checks
-   End-to-end workflow

------------------------------------------------------------------------

## 3. Authentication

### Signup

-   User can create an account with valid information.
-   Required fields are validated.
-   Duplicate email registration is rejected.
-   Invalid email format shows an appropriate error.
-   Weak or invalid password input is rejected according to the defined
    validation rules.
-   Passwords are not stored as plain text.
-   Successful registration returns the expected response.

### Login

-   User can login using valid credentials.
-   Invalid email shows an error.
-   Invalid password shows an error.
-   Empty credentials are rejected.
-   Successful login creates the expected authenticated session/token.
-   User is redirected to the appropriate authenticated area.

### Logout

-   User can logout successfully.
-   Authentication state is cleared after logout.
-   Logged-out users cannot access protected pages.
-   Logged-out users cannot call protected APIs successfully.

------------------------------------------------------------------------

## 4. Authorization

-   A user can access only the resources permitted for their role.
-   Protected API routes reject unauthenticated requests.
-   Patients cannot perform doctor-only actions.
-   Patients cannot perform admin-only actions.
-   Doctors cannot perform admin-only actions unless explicitly allowed.
-   A user cannot modify another user's protected information.
-   Authorization is checked on the backend, not only in the frontend.

------------------------------------------------------------------------

## 5. Patient Registration

-   Patient can submit valid registration information.
-   Required patient fields are validated.
-   Invalid age is rejected.
-   Invalid or missing required information shows an error.
-   Successfully registered patient is stored in MongoDB.
-   Registration timestamp is stored correctly.
-   Duplicate or invalid data is handled according to the defined rules.
-   Successful registration produces the expected response.

------------------------------------------------------------------------

## 6. Doctor Module

-   Doctor list can be retrieved successfully.
-   Doctor details can be retrieved successfully.
-   Doctor department is displayed correctly.
-   Doctor availability is displayed correctly.
-   Authorized users can update doctor availability.
-   Unauthorized users cannot change doctor availability.
-   Invalid doctor IDs return an appropriate error.
-   Unavailable doctors are handled correctly during queue registration.

------------------------------------------------------------------------

## 7. Token Generation

-   A valid patient can join a selected doctor's queue.
-   A token number is generated correctly.
-   Token numbers follow the defined queue rules.
-   A patient cannot create an invalid queue entry.
-   The selected doctor is associated with the queue entry.
-   The queue entry is stored in MongoDB.
-   Registration/join time is stored correctly.
-   Queue position is calculated correctly.

### Token Edge Cases

-   Multiple patients joining the same queue receive valid distinct
    token numbers.
-   Patients joining different doctors do not interfere with each
    other's queues.
-   Invalid doctor IDs are rejected.
-   Invalid patient IDs are rejected.
-   Queue creation for an unavailable doctor follows the defined
    business rule.

------------------------------------------------------------------------

## 8. Queue Ordering

-   Patients are displayed in the correct queue order.
-   Earlier valid registrations appear before later registrations
    according to the queue rules.
-   Queue position is updated when a patient is called.
-   Queue position changes correctly when a patient is completed.
-   Cancelled patients do not incorrectly block the queue.
-   No-show patients do not incorrectly block the queue.
-   The server remains the source of truth for queue ordering.
-   Frontend changes cannot directly alter queue data in MongoDB.

------------------------------------------------------------------------

## 9. Queue Status

The expected main flow is:

``` text
WAITING
   ↓
CALLED
   ↓
IN_CONSULTATION
   ↓
COMPLETED
```

Alternative flows:

``` text
WAITING → CANCELLED
WAITING → NO_SHOW
```

### Tests

-   Newly registered patient receives `WAITING` status.
-   Authorized doctor can call the next patient.
-   `WAITING` can transition to `CALLED`.
-   `CALLED` can transition to `IN_CONSULTATION`.
-   `IN_CONSULTATION` can transition to `COMPLETED`.
-   A waiting patient can be cancelled according to the defined rules.
-   A waiting patient can be marked as no-show according to the defined
    rules.
-   Invalid status transitions are rejected.
-   Unauthorized users cannot change queue status.
-   Status changes are persisted in MongoDB.
-   Status changes are reflected in the UI.

------------------------------------------------------------------------

## 10. Waiting-Time Prediction

### Prediction Input

-   Required prediction features are collected correctly.
-   Feature values are validated before being sent to the ML service.
-   Missing required features are handled correctly.
-   Invalid numeric values are rejected.

### Prediction API

-   Node.js backend can communicate with the Python ML service.
-   Python ML API accepts valid prediction requests.
-   Python ML API returns a valid prediction.
-   Prediction is numeric and represents an estimated waiting time.
-   Invalid requests return an appropriate error.
-   ML service failure is handled gracefully by the backend.
-   Prediction timeout or unavailable ML service does not crash the main
    application.

### Prediction Integration

-   Prediction is generated when required by the queue workflow.
-   Predicted waiting time is stored correctly when applicable.
-   Updated queue information can trigger a new prediction.
-   The displayed waiting time is clearly treated as an estimate.
-   The application does not claim that the predicted value is
    guaranteed.

------------------------------------------------------------------------

## 11. Machine Learning Model

-   Synthetic dataset can be loaded successfully.
-   Dataset preprocessing completes without unexpected errors.
-   Required features exist in the training data.
-   Missing or invalid training data is handled appropriately.
-   Candidate regression models can be trained.
-   Models can be evaluated using documented evaluation metrics.
-   The selected model can be saved successfully.
-   Saved model can be loaded successfully for prediction.
-   Prediction using the saved model produces the expected output
    format.
-   The model is loaded for prediction rather than retrained for every
    request.

### ML Limitations

-   Testing must not claim clinical validation.
-   Testing must not treat the synthetic dataset as real hospital data.
-   Model performance should be reported only for the available
    synthetic/test data.
-   Predictions should be treated as estimates.

------------------------------------------------------------------------

## 12. REST API Testing

### Authentication APIs

``` text
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
```

Verify:

-   Valid requests succeed.
-   Invalid requests return appropriate errors.
-   Authentication requirements are enforced.

### Patient APIs

``` text
POST /api/patients
GET /api/patients/:id
```

Verify:

-   Valid patient operations succeed.
-   Invalid IDs are handled.
-   Unauthorized access is rejected.

### Doctor APIs

``` text
GET /api/doctors
GET /api/doctors/:id
PATCH /api/doctors/:id/availability
```

Verify:

-   Doctor data is returned correctly.
-   Availability updates are authorized.
-   Invalid requests are rejected.

### Queue APIs

``` text
POST /api/queue
GET /api/queue/:doctorId
PATCH /api/queue/:id/status
GET /api/queue/:id/prediction
```

Verify:

-   Queue creation works.
-   Queue retrieval returns correct ordering.
-   Status updates work.
-   Invalid queue operations are rejected.
-   Prediction information is returned correctly.

------------------------------------------------------------------------

## 13. Socket.io Real-Time Updates

-   Client can establish a Socket.io connection.
-   Connected clients receive relevant queue updates.
-   New patient registration triggers the appropriate event.
-   Queue changes trigger `queue:updated`.
-   Patient calling triggers `patient:called`.
-   Consultation start triggers `consultation:started`.
-   Consultation completion triggers `consultation:completed`.
-   Cancellation triggers `patient:cancelled`.
-   Doctor availability changes trigger `doctor:availabilityChanged`.
-   Prediction changes trigger `prediction:updated` when applicable.
-   Disconnected clients can reconnect without corrupting queue state.
-   Socket events do not replace backend authorization.

------------------------------------------------------------------------

## 14. MongoDB Persistence

-   Application connects successfully to MongoDB.
-   Required collections/models are created correctly.
-   Patient records are persisted correctly.
-   Doctor records are persisted correctly.
-   User records are persisted correctly.
-   Queue records are persisted correctly.
-   Queue status updates are persisted.
-   Prediction values are persisted when required.
-   Invalid documents are rejected through schema validation.
-   Database connection errors are handled gracefully.

------------------------------------------------------------------------

## 15. Frontend Testing

### Patient Interface

-   Patient can register.
-   Patient can select a doctor.
-   Patient can join the queue.
-   Patient can view token number.
-   Patient can view queue position.
-   Patient can view estimated waiting time.
-   Patient can see queue status changes.
-   Loading states are displayed where needed.
-   API errors are displayed clearly.

### Doctor Interface

-   Doctor can login.
-   Doctor can view their queue.
-   Doctor can see patient queue order.
-   Doctor can call the next patient.
-   Doctor can start consultation.
-   Doctor can complete consultation.
-   Doctor can update availability if authorized.
-   Queue changes appear without requiring unnecessary manual refresh.

------------------------------------------------------------------------

## 16. Validation and Error Handling

-   Required fields cannot be submitted empty.
-   Invalid input shows a clear error.
-   Invalid IDs return appropriate errors.
-   Unauthorized requests return an appropriate status.
-   Non-existent resources return an appropriate response.
-   Server errors do not expose sensitive implementation details.
-   Network failures show a user-friendly message.
-   ML service failures show a controlled error state.
-   Database failures are handled without crashing the frontend.

------------------------------------------------------------------------

## 17. Security Checks

-   Passwords are hashed before storage.
-   Password hashes are never returned unnecessarily to the frontend.
-   Authentication middleware protects private APIs.
-   Authorization is enforced server-side.
-   Secrets are stored in environment variables.
-   Sensitive configuration is not committed to Git.
-   Invalid authentication tokens are rejected.
-   Users cannot access resources they do not own or have permission to
    access.
-   Basic input validation is applied to API requests.
-   Common injection risks are addressed through proper database/API
    handling.

------------------------------------------------------------------------

## 18. Responsive Testing

The application should be tested at:

### Mobile

**375px width**

Check:

-   Navigation
-   Registration form
-   Queue display
-   Token display
-   Waiting-time display
-   Buttons
-   Tables/cards
-   Text wrapping
-   Horizontal scrolling

### Tablet

**768px width**

Check:

-   Navigation
-   Dashboard layout
-   Queue information
-   Forms
-   Cards and tables
-   Spacing and alignment

### Desktop

**1440px width**

Check:

-   Full dashboard layout
-   Queue display
-   Navigation
-   Tables/cards
-   Content spacing
-   Overall visual consistency

The UI should not have unintended horizontal scrolling at supported
screen sizes.

------------------------------------------------------------------------

## 19. End-to-End Test

### Main Patient Flow

``` text
Register/Login
      ↓
Select Doctor
      ↓
Register Patient
      ↓
Receive Token
      ↓
Join Queue
      ↓
View Queue Position
      ↓
View Estimated Waiting Time
      ↓
Receive Real-Time Queue Updates
      ↓
Patient Called
      ↓
Consultation Started
      ↓
Consultation Completed
```

This complete flow should work without manual database modification.

------------------------------------------------------------------------

## 20. Queue Scenario Testing

### Scenario A --- Single Patient

-   One patient joins an available doctor's queue.
-   Patient receives a token.
-   Patient becomes the first waiting patient.
-   Waiting-time prediction is generated.
-   Doctor calls the patient.
-   Consultation starts.
-   Consultation completes.
-   Queue becomes empty.

### Scenario B --- Multiple Patients

-   Multiple patients join the same doctor queue.
-   Each patient receives a valid token.
-   Queue order is correct.
-   Each patient's position is correct.
-   Waiting-time estimates are generated.
-   Calling one patient updates the remaining queue.
-   Remaining patients receive updated queue information.

### Scenario C --- Cancellation

-   Patient joins the queue.
-   Patient cancels according to the allowed flow.
-   Queue is updated.
-   Remaining patients are not incorrectly delayed by the cancelled
    entry.

### Scenario D --- No-Show

-   Patient reaches the called state.
-   Patient is marked as no-show according to the allowed flow.
-   Queue proceeds to the next valid patient.

### Scenario E --- Doctor Unavailable

-   Doctor is marked unavailable.
-   New queue registration follows the defined rule.
-   Existing queue information remains consistent.
-   Doctor availability change is reflected in connected clients.

------------------------------------------------------------------------

## 21. Error and Edge-Case Testing

Test the system with:

-   Empty form submission
-   Invalid email
-   Invalid password
-   Duplicate account
-   Invalid patient ID
-   Invalid doctor ID
-   Invalid queue ID
-   Missing authentication token
-   Expired/invalid authentication token
-   Unauthorized role
-   Duplicate queue request
-   Multiple patients joining simultaneously
-   Doctor unavailable
-   Empty queue
-   Cancelled patient
-   No-show patient
-   ML service unavailable
-   Database unavailable
-   Network interruption
-   Socket disconnection
-   Invalid prediction input
-   Very large queue
-   Unexpected API response

------------------------------------------------------------------------

## 22. Performance Checks

For the MVP, verify that:

-   Normal API requests return within an acceptable time during local
    testing.
-   Queue updates do not cause unnecessary repeated database operations.
-   Socket.io updates are received promptly by connected clients.
-   Prediction requests complete within an acceptable time.
-   Large queue scenarios do not break queue ordering.
-   The frontend remains usable while API/ML requests are processing.

Exact performance thresholds can be added after baseline measurements
are available.

------------------------------------------------------------------------

## 23. Test Data

Testing should use controlled synthetic/test data.

Example:

``` text
Doctor:
Name: Dr. Sharma
Department: General Medicine
Average Consultation Time: 12 minutes
Available: Yes
```

Example patients:

``` text
Patient 1 → Token 1
Patient 2 → Token 2
Patient 3 → Token 3
```

Test data should not be presented as real patient or hospital data.

------------------------------------------------------------------------

## 24. Acceptance Criteria

The system can be considered functionally working for the MVP when:

-   Authentication works correctly.
-   Protected routes and APIs enforce authorization.
-   Patients can be registered.
-   Doctors can be retrieved and availability can be updated by
    authorized users.
-   Patients can join a doctor's queue.
-   Tokens and queue positions are generated correctly.
-   Queue status transitions work correctly.
-   Queue data is persisted in MongoDB.
-   Waiting-time prediction works through the Python ML service.
-   Prediction failures are handled safely.
-   Socket.io delivers relevant queue updates.
-   Patient and doctor interfaces display current queue information.
-   Responsive layouts work at 375px, 768px, and 1440px.
-   Major invalid-input and error scenarios are handled.
-   The main end-to-end patient flow works without manual database
    changes.

------------------------------------------------------------------------

## 25. Test Status

Use the following status values while testing:

  -----------------------------------------------------------------------
  Status                              Meaning
  ----------------------------------- -----------------------------------
  NOT STARTED                         Test has not been executed

  PASS                                Expected behavior confirmed

  FAIL                                Expected behavior not achieved

  BLOCKED                             Test cannot be executed because of
                                      another issue

  FIXED                               Previously failed test has been
                                      corrected and needs retesting

  RETEST                              Fix is available and test needs to
                                      be executed again
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 26. Test Case Tracking

A detailed test case can follow this format:

  -----------------------------------------------------------------------------
  ID             Module           Test           Expected Result Status
  -------------- ---------------- -------------- --------------- --------------
  AUTH-001       Authentication   Signup with    Account is      NOT STARTED
                                  valid data     created         

  AUTH-002       Authentication   Login with     User is         NOT STARTED
                                  valid          authenticated   
                                  credentials                    

  AUTH-003       Authentication   Login with     Error is        NOT STARTED
                                  invalid        displayed       
                                  password                       

  AUTH-004       Authorization    Access         Access is       NOT STARTED
                                  dashboard      denied          
                                  while logged                   
                                  out                            

  PAT-001        Patient          Register valid Patient is      NOT STARTED
                                  patient        stored          

  QUE-001        Queue            Join available Token is        NOT STARTED
                                  doctor's queue generated       

  QUE-002        Queue            Add multiple   Queue order is  NOT STARTED
                                  patients       correct         

  QUE-003        Queue            Change queue   Valid           NOT STARTED
                                  status         transition      
                                                 succeeds        

  ML-001         ML               Send valid     Prediction is   NOT STARTED
                                  prediction     returned        
                                  request                        

  ML-002         ML               Send invalid   Validation      NOT STARTED
                                  prediction     error is        
                                  request        returned        

  SOC-001        Socket.io        Register       Queue update is NOT STARTED
                                  patient        broadcast       

  UI-001         Responsive       Test at 375px  Layout remains  NOT STARTED
                                                 usable          

  UI-002         Responsive       Test at 768px  Layout remains  NOT STARTED
                                                 usable          

  UI-003         Responsive       Test at 1440px Layout remains  NOT STARTED
                                                 usable          
  -----------------------------------------------------------------------------

------------------------------------------------------------------------

## 27. Definition of "Working"

For this project, **working** means that a feature:

1.  Performs its intended function.
2.  Stores and retrieves data correctly.
3.  Enforces authentication and authorization where required.
4.  Handles invalid input safely.
5.  Handles expected errors without breaking the application.
6.  Updates dependent parts of the system correctly.
7.  Works through the intended user interface and API flow.
8.  Does not require manual database changes for normal operation.
9.  Passes its relevant test cases.
10. Does not violate the project's documented architecture or technical
    decisions.

A feature should not be considered complete only because the UI appears
to work. Its backend behavior, database persistence, authorization,
error handling, and relevant integrations must also work.

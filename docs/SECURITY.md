# Security Requirements

## 1. Purpose

Security is part of the system design from the beginning.

These requirements define the minimum security practices for the AI
Based Dynamic Patient Queue And Waiting Time Prediction System during
development, testing, and deployment.

Security should not be added five minutes before deployment. It should
be considered whenever authentication, authorization, APIs, database
operations, file handling, configuration, or user input is implemented.

------------------------------------------------------------------------

## 2. Authentication

-   Private routes require authentication.
-   Protected API endpoints must verify the user's authentication state.
-   Login must require valid credentials.
-   Invalid credentials must not create an authenticated session.
-   Passwords must never be stored as plain text.
-   Passwords must be securely hashed before storage.
-   Authentication tokens/session information must be handled securely.
-   Invalid, expired, or missing authentication credentials must be
    rejected.
-   Logout must invalidate or clear the authenticated state according to
    the chosen authentication mechanism.
-   Authentication logic must be implemented on the backend.
-   Frontend route protection alone is not sufficient.

------------------------------------------------------------------------

## 3. Authorization

Users can only access resources and perform actions they are authorized
to access.

-   Authorization must be enforced on the backend.
-   Users cannot access another user's private resources without
    permission.
-   Patients cannot perform doctor-only operations.
-   Unauthorized users cannot change queue status.
-   Unauthorized users cannot modify doctor availability.
-   Admin-only operations must require the appropriate role.
-   Role information supplied by the client must not be trusted without
    server-side verification.
-   Resource ownership must be checked before returning or modifying
    protected data.
-   Directly changing an ID in a request must not allow access to
    another user's data.

### Example

A patient requesting:

``` text
GET /api/patients/<another-patient-id>
```

must be rejected unless the user's role and permissions explicitly allow
that access.

------------------------------------------------------------------------

## 4. Secrets and Configuration

Never expose secrets to client-side code.

-   Store secrets in environment variables.
-   Do not hard-code passwords, API keys, database credentials, or
    authentication secrets in source code.
-   Do not commit `.env` files containing real secrets to Git.
-   Use `.env.example` with placeholder values for required
    configuration.
-   Keep production credentials separate from development credentials.
-   Do not send server-side secrets to the React frontend.
-   Do not expose MongoDB credentials in browser code.
-   Do not expose ML-service credentials or internal service secrets to
    the client.
-   Rotate compromised secrets immediately.
-   Review configuration before pushing code to a public repository.

### Example

Safe:

``` text
DATABASE_URL=<environment-variable>
JWT_SECRET=<environment-variable>
```

Unsafe:

``` js
const JWT_SECRET = "my-secret-password";
```

------------------------------------------------------------------------

## 5. Database Security

MongoDB must be accessed only through the backend.

-   React must never connect directly to MongoDB.
-   MongoDB credentials must remain server-side.
-   Use a dedicated database user with only the permissions required by
    the application.
-   Avoid using unrestricted database accounts for normal application
    access.
-   Use appropriate database access policies.
-   Apply Mongoose schema validation.
-   Validate IDs before querying resources.
-   Do not trust user-provided database identifiers.
-   Prevent unauthorized reads and updates through backend authorization
    checks.
-   Avoid returning sensitive database fields to the client.
-   Use appropriate indexes for frequently queried fields.
-   Configure production database access so that unnecessary public
    access is not allowed.
-   Use encrypted connections where supported by the deployment
    environment.
-   Maintain appropriate backups for production data.
-   Do not use real patient information during development or testing.

------------------------------------------------------------------------

## 6. Input Validation

Validate all user input.

Input validation must be performed on the backend even if the frontend
already validates the same input.

Validate:

-   Required fields
-   Data types
-   String length
-   Numeric ranges
-   Email format
-   IDs
-   Enumerated values
-   Date/time values
-   Queue status values
-   Role values
-   ML prediction inputs

### Examples

Patient age should:

-   Be numeric.
-   Be within the application's allowed range.
-   Not contain unexpected text.

Queue status should accept only supported values such as:

``` text
WAITING
CALLED
IN_CONSULTATION
COMPLETED
CANCELLED
NO_SHOW
```

Unexpected values must be rejected.

------------------------------------------------------------------------

## 7. API Security

Validate request bodies, query parameters, route parameters, and headers
where applicable.

For every API endpoint:

-   Validate the request body.
-   Validate route parameters.
-   Validate query parameters.
-   Authenticate protected requests.
-   Authorize the requested operation.
-   Reject unexpected or invalid input.
-   Return appropriate HTTP status codes.
-   Do not expose internal stack traces to clients.
-   Do not expose database credentials or secrets in API responses.
-   Do not trust client-supplied role or ownership information.
-   Apply reasonable request limits where appropriate.
-   Handle malformed JSON and invalid requests safely.

### API Example

For:

``` text
PATCH /api/queue/:id/status
```

the backend should verify:

1.  The user is authenticated.
2.  The queue ID is valid.
3.  The queue exists.
4.  The user has permission to change its status.
5.  The requested status is valid.
6.  The status transition is allowed.
7.  The update is persisted successfully.

------------------------------------------------------------------------

## 8. Queue Security

Because the queue is a core part of the system:

-   Queue ordering must be controlled by the backend.
-   Clients must not be allowed to arbitrarily set their queue position.
-   Clients must not be allowed to assign themselves an arbitrary token
    number.
-   Queue status transitions must be validated server-side.
-   Patients must not be able to modify another patient's queue entry.
-   Unauthorized users must not be able to remove or modify queue
    entries.
-   Concurrent queue requests should be handled safely.
-   Queue data returned to a user should contain only information they
    are authorized to see.

------------------------------------------------------------------------

## 9. Waiting-Time Prediction Security

The ML service must not be treated as a trusted source for arbitrary
client input.

-   Prediction requests should originate through the authorized backend
    workflow.
-   Validate all prediction features before sending them to the ML
    service.
-   Validate the ML service response before storing or displaying it.
-   Do not allow users to upload or replace the production model through
    an ordinary client request.
-   The trained model should be stored in a controlled server-side
    location.
-   Do not expose internal ML service credentials to the frontend.
-   ML-service errors must not expose internal implementation details.
-   Predicted waiting time must be displayed as an estimate.
-   The prediction system must not be presented as making clinical
    decisions.

------------------------------------------------------------------------

## 10. Socket.io Security

Socket.io connections must follow the application's authentication and
authorization rules.

-   Authenticate protected socket connections where required.
-   Do not trust user identity supplied only by client-side event data.
-   Validate socket event payloads.
-   Verify authorization before sensitive socket actions.
-   Do not allow arbitrary users to emit privileged queue events.
-   Server-side events should be generated from validated application
    actions.
-   Sensitive information should not be broadcast to unauthorized
    clients.
-   Handle disconnects and reconnects safely.
-   Do not expose internal server information through socket errors.

------------------------------------------------------------------------

## 11. File Uploads

If file uploads are added in the future, validate:

### File Type

-   Allow only explicitly supported file types.
-   Do not rely only on the filename extension.
-   Validate the file's actual type where practical.
-   Reject unsupported file formats.

### File Size

-   Set a maximum file size.
-   Reject files exceeding the configured limit.
-   Prevent unusually large uploads from consuming excessive server
    resources.

### Filename

-   Do not trust user-provided filenames.
-   Sanitize filenames.
-   Avoid using raw filenames as server filesystem paths.
-   Prevent path traversal such as:

``` text
../../file
```

-   Generate safe server-side filenames where appropriate.

### Additional Upload Controls

-   Store uploaded files outside sensitive application code directories
    where appropriate.
-   Restrict executable file types unless explicitly required.
-   Validate uploads before processing them.
-   Do not expose private uploaded files publicly without authorization.

------------------------------------------------------------------------

## 12. Password Security

-   Passwords must be hashed using a suitable password-hashing
    algorithm.
-   Never store plain-text passwords.
-   Never log passwords.
-   Never return passwords or password hashes in normal API responses.
-   Password requirements should be enforced consistently.
-   Authentication error messages should avoid unnecessarily revealing
    sensitive account information.

------------------------------------------------------------------------

## 13. Error Handling

Security errors should fail safely.

-   Do not expose stack traces in production responses.
-   Do not expose database connection strings.
-   Do not expose environment variables.
-   Do not expose internal file paths.
-   Do not expose authentication secrets.
-   Log useful server-side information without logging sensitive
    credentials.
-   Return clear but appropriately limited client-facing error messages.

Example client response:

``` json
{
  "message": "Invalid request"
}
```

Avoid exposing internal details such as:

``` text
MongoServerError: connection string ...
```

------------------------------------------------------------------------

## 14. HTTP and Transport Security

For production deployment:

-   Use HTTPS.
-   Do not transmit authentication credentials over plain HTTP.
-   Configure secure cookie settings if cookies are used.
-   Configure appropriate CORS rules.
-   Do not allow arbitrary origins unless required.
-   Use security-related HTTP headers where appropriate.
-   Configure secure transport for database and internal service
    connections where supported.

------------------------------------------------------------------------

## 15. CORS

CORS must be explicitly configured.

-   Allow only trusted frontend origins in production.
-   Do not use unrestricted origins when credentials or protected APIs
    are involved.
-   Review allowed HTTP methods.
-   Review allowed headers.
-   Avoid enabling unnecessary cross-origin access.

Development configuration may use a local frontend origin, but
production configuration should use the deployed application's trusted
origin.

------------------------------------------------------------------------

## 16. Rate Limiting and Abuse Protection

Apply reasonable limits to endpoints that may be abused.

Particularly consider:

-   Login
-   Registration
-   Password-related operations
-   Prediction requests
-   Public API endpoints
-   Resource-intensive operations

Rate limiting should reduce repeated abusive requests without preventing
normal project usage.

------------------------------------------------------------------------

## 17. Dependency Security

-   Keep dependencies reasonably up to date.
-   Review security warnings from package managers.
-   Remove unused dependencies.
-   Avoid installing packages that are not required.
-   Review third-party packages before using them.
-   Do not ignore serious known vulnerabilities without documenting the
    reason.

For Node.js:

``` text
npm audit
```

can be used as one part of dependency security checking.

Python dependencies should also be reviewed for known vulnerabilities.

------------------------------------------------------------------------

## 18. Git and Repository Security

Never commit:

-   `.env`
-   Database passwords
-   API keys
-   Authentication secrets
-   Private certificates
-   Production credentials
-   Private patient data
-   Private uploaded files

Use `.gitignore` for sensitive local files.

Example:

``` text
.env
.env.*
!.env.example
node_modules/
__pycache__/
*.pyc
```

Before pushing code:

-   Check staged files.
-   Search for accidentally exposed secrets.
-   Confirm that test data does not contain real patient information.
-   Confirm that production credentials are not included.

------------------------------------------------------------------------

## 19. Logging and Monitoring

Logs should help diagnose problems without exposing sensitive
information.

Do not log:

-   Passwords
-   Authentication tokens
-   Database passwords
-   API keys
-   Sensitive personal information unnecessarily

Useful logs may include:

-   Authentication failures
-   Authorization failures
-   API errors
-   Database errors
-   ML service failures
-   Unexpected queue state transitions
-   Application startup/shutdown events

Production logging should be reviewed periodically.

------------------------------------------------------------------------

## 20. Privacy and Patient Data

Although the project uses synthetic data, the application should still
follow privacy-conscious design.

-   Use synthetic data for development and testing.
-   Do not add real patient information to the repository.
-   Do not use real patient records in demonstrations.
-   Do not expose unnecessary patient information on public screens.
-   Restrict access to patient information according to role and
    ownership.
-   Avoid storing personal information that is not required by the
    project.
-   Do not use project screenshots containing real personal information.

------------------------------------------------------------------------

## 21. Frontend Security

The React frontend must not be treated as a trusted security boundary.

-   Never store server secrets in frontend environment variables.
-   Do not place database credentials in React code.
-   Do not rely on hidden UI elements to enforce permissions.
-   Backend APIs must perform the actual authorization checks.
-   Avoid rendering untrusted HTML directly.
-   Validate data received from APIs before using it in sensitive
    operations.
-   Handle authentication state carefully.
-   Do not expose unnecessary internal API information.

------------------------------------------------------------------------

## 22. Environment Separation

Maintain separate configuration for:

``` text
Development
Testing
Production
```

Production secrets must not be reused in development.

Development and testing should use synthetic data.

Environment-specific configuration should be stored outside source code
whenever it contains sensitive information.

------------------------------------------------------------------------

## 23. Security Testing Checklist

Before considering the MVP ready for deployment, verify:

### Authentication

-   [ ] Private routes require authentication.
-   [ ] Invalid credentials are rejected.
-   [ ] Passwords are securely hashed.
-   [ ] Logout works correctly.
-   [ ] Invalid authentication credentials are rejected.

### Authorization

-   [ ] Users cannot access unauthorized resources.
-   [ ] Role permissions are enforced server-side.
-   [ ] Queue actions are permission-controlled.
-   [ ] Doctor availability updates are permission-controlled.

### Secrets

-   [ ] No secrets are hard-coded.
-   [ ] `.env` is not committed.
-   [ ] Production secrets are stored securely.
-   [ ] Frontend contains no server-side secrets.

### Database

-   [ ] MongoDB is accessed only by the backend.
-   [ ] Database access uses appropriate permissions.
-   [ ] Input IDs are validated.
-   [ ] Sensitive fields are not unnecessarily returned.
-   [ ] Production database access is restricted.

### Input and APIs

-   [ ] Request bodies are validated.
-   [ ] Route parameters are validated.
-   [ ] Query parameters are validated.
-   [ ] Invalid input is rejected.
-   [ ] API errors do not expose internal details.

### Queue

-   [ ] Token generation is server-controlled.
-   [ ] Queue position is server-controlled.
-   [ ] Status transitions are validated.
-   [ ] Unauthorized queue modifications are rejected.

### ML

-   [ ] Prediction inputs are validated.
-   [ ] ML service responses are validated.
-   [ ] ML credentials are not exposed.
-   [ ] Model files cannot be replaced through unauthorized requests.

### Socket.io

-   [ ] Protected connections are authenticated where required.
-   [ ] Event payloads are validated.
-   [ ] Sensitive events are authorization-controlled.

### File Uploads

If file uploads are implemented:

-   [ ] File type is validated.
-   [ ] File size is limited.
-   [ ] Filename is sanitized.
-   [ ] Path traversal is prevented.
-   [ ] Uploaded files are access-controlled.

### Production

-   [ ] HTTPS is enabled.
-   [ ] CORS is restricted.
-   [ ] Dependencies are reviewed.
-   [ ] Logging does not expose secrets.
-   [ ] Production configuration is separated from development
    configuration.

------------------------------------------------------------------------

## 24. Security Definition of Done

A feature should not be considered security-complete merely because its
normal workflow works.

A feature is security-complete when:

1.  Authentication requirements are defined.
2.  Authorization requirements are defined.
3.  Input validation is implemented.
4.  Sensitive data is protected.
5.  Errors fail safely.
6.  API access is controlled.
7.  Database access is restricted.
8.  Secrets are not exposed.
9.  Relevant security edge cases have been tested.
10. The implementation follows the project's documented security
    requirements.

Security is therefore part of development, testing, and deployment
rather than a final step before release.

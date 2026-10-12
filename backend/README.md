# Backend (Node.js + Express)

Minimal backend scaffold for TASK-014.

Quick start

1. Install dependencies from the `backend` folder:

```powershell
cd backend
npm install
```

2. Run in development (uses `nodemon`):

```powershell
npm run dev
```

3. Or run production start:

```powershell
npm start
```

Health endpoint: `GET /api/health` returns a simple JSON status.

Database stub
 
- A lightweight MongoDB helper is available at `src/config/db.js`.
- By default the server does not attempt to connect; to enable the DB,
  import and call `connectDB()` from `src/index.js` after providing
  a `MONGODB_URI` in your `.env` file (see `.env.example`).

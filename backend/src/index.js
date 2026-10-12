const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const healthRouter = require('./routes/health');
const { connectDB } = require('./config/db');

const app = express();

app.use(cors());
app.use(express.json());

app.use('/api/health', healthRouter);

app.get('/', (req, res) => res.json({ message: 'Dynamic Patient Queue Backend' }));

const port = process.env.PORT || 5000;

async function start() {
  try {
    await connectDB();
  } catch (err) {
    console.error('Failed to connect to MongoDB, aborting start.');
    process.exit(1);
  }

  app.listen(port, () => {
    console.log(`Backend server listening on port ${port}`);
  });
}

start();

module.exports = app;

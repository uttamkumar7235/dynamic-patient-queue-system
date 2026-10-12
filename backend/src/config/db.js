const mongoose = require('mongoose');
const dotenv = require('dotenv');

dotenv.config();

/**
 * connectDB - establish a Mongoose connection using `MONGODB_URI`.
 * - If `MONGODB_URI` is not set, the function resolves without connecting.
 * - If `MONGODB_URI` is set, it attempts to connect and rejects on error.
 *
 * Caller should decide whether to continue or abort on connection failure.
 */
async function connectDB(uri) {
  const mongoUri = uri || process.env.MONGODB_URI;
  if (!mongoUri) {
    console.warn('MONGODB_URI not set — skipping MongoDB connection.');
    return;
  }

  // Mongoose connection options
  const opts = {
    // Recommended in modern mongoose versions; keep minimal to avoid warnings
    serverSelectionTimeoutMS: 5000
  };

  try {
    await mongoose.connect(mongoUri, opts);

    mongoose.connection.on('error', (err) => {
      console.error('MongoDB connection error (runtime):', err);
    });

    mongoose.connection.on('disconnected', () => {
      console.warn('MongoDB disconnected');
    });

    mongoose.connection.on('reconnected', () => {
      console.log('MongoDB reconnected');
    });

    console.log('MongoDB connected');
  } catch (err) {
    console.error('MongoDB initial connection error:', err.message || err);
    // Re-throw so caller can decide to exit or retry
    throw err;
  }
}

module.exports = { connectDB };

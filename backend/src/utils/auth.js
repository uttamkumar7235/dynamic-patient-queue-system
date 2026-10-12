const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'development-secret-change-me';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '1d';

function normalizeUser(user) {
  const plainUser = user && typeof user.toObject === 'function' ? user.toObject() : user;

  return {
    id: plainUser?._id ? plainUser._id.toString() : plainUser?.id,
    name: plainUser?.name,
    email: plainUser?.email,
    role: plainUser?.role
  };
}

function generateToken(user) {
  const payload = normalizeUser(user);

  return jwt.sign(
    {
      id: payload.id,
      email: payload.email,
      role: payload.role,
      name: payload.name
    },
    JWT_SECRET,
    { expiresIn: JWT_EXPIRES_IN }
  );
}

function verifyToken(token) {
  return jwt.verify(token, JWT_SECRET);
}

async function hashPassword(password) {
  return bcrypt.hash(password, 10);
}

async function comparePassword(candidatePassword, passwordHash) {
  return bcrypt.compare(candidatePassword, passwordHash);
}

module.exports = {
  JWT_SECRET,
  JWT_EXPIRES_IN,
  normalizeUser,
  generateToken,
  verifyToken,
  hashPassword,
  comparePassword
};

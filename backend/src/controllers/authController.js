const User = require('../models/User');
const { normalizeUser, generateToken, hashPassword, comparePassword } = require('../utils/auth');

function validateEmail(email) {
  return typeof email === 'string' && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
}

function sanitizeRegistrationInput(body = {}) {
  const name = typeof body.name === 'string' ? body.name.trim() : '';
  const email = typeof body.email === 'string' ? body.email.trim().toLowerCase() : '';
  const password = typeof body.password === 'string' ? body.password : '';
  const role = typeof body.role === 'string' ? body.role.trim().toUpperCase() : 'PATIENT';

  if (!name) {
    throw Object.assign(new Error('Name is required'), { status: 400 });
  }

  if (!validateEmail(email)) {
    throw Object.assign(new Error('Please provide a valid email address'), { status: 400 });
  }

  if (password.length < 8) {
    throw Object.assign(new Error('Password must be at least 8 characters long'), { status: 400 });
  }

  if (role !== 'PATIENT') {
    throw Object.assign(new Error('Public registration is restricted to PATIENT accounts.'), { status: 400 });
  }

  return { name, email, password, role };
}

async function registerUser({ UserModel = User, body = {} } = {}) {
  const { name, email, password, role } = sanitizeRegistrationInput(body);

  const existingUser = await UserModel.findOne({ email });
  if (existingUser) {
    throw Object.assign(new Error('An account with this email already exists'), { status: 409 });
  }

  const passwordHash = await hashPassword(password);
  const user = await UserModel.create({
    name,
    email,
    passwordHash,
    role
  });

  return {
    token: generateToken(user),
    user: normalizeUser(user)
  };
}

async function loginUser({ UserModel = User, body = {} } = {}) {
  const email = typeof body.email === 'string' ? body.email.trim().toLowerCase() : '';
  const password = typeof body.password === 'string' ? body.password : '';

  if (!validateEmail(email)) {
    throw Object.assign(new Error('Please provide a valid email address'), { status: 400 });
  }

  if (!password) {
    throw Object.assign(new Error('Password is required'), { status: 400 });
  }

  const user = await UserModel.findOne({ email });
  if (!user) {
    throw Object.assign(new Error('Invalid email or password'), { status: 401 });
  }

  const isPasswordValid = await comparePassword(password, user.passwordHash);
  if (!isPasswordValid) {
    throw Object.assign(new Error('Invalid email or password'), { status: 401 });
  }

  return {
    token: generateToken(user),
    user: normalizeUser(user)
  };
}

module.exports = {
  registerUser,
  loginUser,
  sanitizeRegistrationInput,
  validateEmail
};

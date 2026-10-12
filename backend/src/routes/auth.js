const express = require('express');
const User = require('../models/User');
const { registerUser, loginUser } = require('../controllers/authController');
const { authenticate, authorize } = require('../middleware/auth');

const router = express.Router();

router.post('/register', async (req, res) => {
  try {
    const result = await registerUser({ UserModel: User, body: req.body });

    return res.status(201).json({
      message: 'Registration successful',
      token: result.token,
      user: result.user
    });
  } catch (error) {
    const status = error.status || 500;
    return res.status(status).json({
      message: error.message || 'Registration failed'
    });
  }
});

router.post('/login', async (req, res) => {
  try {
    const result = await loginUser({ UserModel: User, body: req.body });

    return res.status(200).json({
      message: 'Login successful',
      token: result.token,
      user: result.user
    });
  } catch (error) {
    const status = error.status || 500;
    return res.status(status).json({
      message: error.message || 'Login failed'
    });
  }
});

router.get('/me', authenticate, (req, res) => {
  return res.status(200).json({ user: req.user });
});

router.get('/doctor-only', authenticate, authorize('DOCTOR'), (req, res) => {
  return res.status(200).json({ message: 'Doctor access granted', user: req.user });
});

router.get('/staff-only', authenticate, authorize('STAFF'), (req, res) => {
  return res.status(200).json({ message: 'Staff access granted', user: req.user });
});

module.exports = router;

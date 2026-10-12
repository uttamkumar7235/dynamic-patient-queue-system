const mongoose = require('mongoose');
const Doctor = require('../models/Doctor');

function isValidObjectId(value) {
  return mongoose.isValidObjectId(value);
}

function parseAvailabilityPayload(body = {}) {
  const isAvailable = body.isAvailable;

  if (typeof isAvailable !== 'boolean') {
    throw Object.assign(new Error('isAvailable must be a boolean'), { status: 400 });
  }

  return { isAvailable };
}

async function listDoctors(req, res) {
  if (!req.user) {
    return res.status(401).json({ message: 'Authentication required' });
  }

  try {
    const doctors = await Doctor.find({}).sort({ name: 1 });
    return res.status(200).json({ doctors });
  } catch (error) {
    return res.status(500).json({ message: 'Unable to fetch doctors' });
  }
}

async function getDoctorById(req, res) {
  if (!req.user) {
    return res.status(401).json({ message: 'Authentication required' });
  }

  const { id } = req.params;
  if (!isValidObjectId(id)) {
    return res.status(400).json({ message: 'Invalid doctor ID' });
  }

  try {
    const doctor = await Doctor.findById(id);

    if (!doctor) {
      return res.status(404).json({ message: 'Doctor not found' });
    }

    return res.status(200).json({ doctor });
  } catch (error) {
    return res.status(500).json({ message: 'Unable to fetch doctor' });
  }
}

async function updateDoctorAvailability(req, res) {
  if (!req.user) {
    return res.status(401).json({ message: 'Authentication required' });
  }

  const { id } = req.params;
  if (!isValidObjectId(id)) {
    return res.status(400).json({ message: 'Invalid doctor ID' });
  }

  if (!['DOCTOR', 'STAFF'].includes(req.user.role)) {
    return res.status(403).json({ message: 'You do not have permission to update doctor availability' });
  }

  if (req.user.role === 'DOCTOR' && req.user.id !== id) {
    return res.status(403).json({ message: 'You can only update your own availability' });
  }

  try {
    const { isAvailable } = parseAvailabilityPayload(req.body);
    const doctor = await Doctor.findById(id);

    if (!doctor) {
      return res.status(404).json({ message: 'Doctor not found' });
    }

    doctor.isAvailable = isAvailable;
    await doctor.save();

    return res.status(200).json({ message: 'Doctor availability updated', doctor });
  } catch (error) {
    const status = error.status || 500;
    return res.status(status).json({ message: error.message || 'Unable to update doctor availability' });
  }
}

module.exports = {
  listDoctors,
  getDoctorById,
  updateDoctorAvailability,
  parseAvailabilityPayload,
  isValidObjectId
};

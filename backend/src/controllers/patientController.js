const mongoose = require('mongoose');
const Patient = require('../models/Patient');

function isValidObjectId(value) {
  return mongoose.isValidObjectId(value);
}

function parsePatientPayload(body = {}) {
  const name = typeof body.name === 'string' ? body.name.trim() : '';
  const age = Number(body.age);
  const gender = typeof body.gender === 'string' ? body.gender.trim() : '';
  const contact = typeof body.contact === 'string' ? body.contact.trim() : '';

  if (!name) {
    throw Object.assign(new Error('Name is required'), { status: 400 });
  }

  if (!Number.isInteger(age) || age < 0 || age > 120) {
    throw Object.assign(new Error('Age must be a whole number between 0 and 120'), { status: 400 });
  }

  if (!gender) {
    throw Object.assign(new Error('Gender is required'), { status: 400 });
  }

  if (!contact) {
    throw Object.assign(new Error('Contact information is required'), { status: 400 });
  }

  return { name, age, gender, contact };
}

async function createPatient(req, res) {
  if (!req.user) {
    return res.status(401).json({ message: 'Authentication required' });
  }

  if (!['PATIENT', 'STAFF'].includes(req.user.role)) {
    return res.status(403).json({ message: 'You do not have permission to create patient records' });
  }

  try {
    const payload = parsePatientPayload(req.body);

    const patientData = {
      ...payload
    };

    if (req.user.role === 'PATIENT') {
      patientData.userId = new mongoose.Types.ObjectId(req.user.id);
      const existing = await Patient.findOne({ userId: patientData.userId });
      if (existing) {
        return res.status(409).json({ message: 'Patient record already exists for this account' });
      }
    }

    if (req.user.role === 'STAFF' && req.body.userId) {
      if (!isValidObjectId(req.body.userId)) {
        return res.status(400).json({ message: 'Invalid user ID' });
      }
      patientData.userId = new mongoose.Types.ObjectId(req.body.userId);
    }

    const patient = await Patient.create(patientData);
    return res.status(201).json({ patient });
  } catch (error) {
    const status = error.status || 500;
    return res.status(status).json({ message: error.message || 'Unable to create patient record' });
  }
}

async function getPatientById(req, res) {
  if (!req.user) {
    return res.status(401).json({ message: 'Authentication required' });
  }

  const { id } = req.params;
  if (!isValidObjectId(id)) {
    return res.status(400).json({ message: 'Invalid patient ID' });
  }

  try {
    const patient = await Patient.findById(id);

    if (!patient) {
      return res.status(404).json({ message: 'Patient not found' });
    }

    if (req.user.role === 'PATIENT' && patient.userId?.toString() !== req.user.id) {
      return res.status(403).json({ message: 'You do not have access to this patient record' });
    }

    if (!['PATIENT', 'DOCTOR', 'STAFF'].includes(req.user.role)) {
      return res.status(403).json({ message: 'You do not have permission to view patient data' });
    }

    return res.status(200).json({ patient });
  } catch (error) {
    const status = error.status || 500;
    return res.status(status).json({ message: error.message || 'Unable to fetch patient record' });
  }
}

module.exports = {
  createPatient,
  getPatientById,
  parsePatientPayload,
  isValidObjectId
};

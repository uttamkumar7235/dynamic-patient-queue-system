const express = require('express');
const { authenticate, authorize } = require('../middleware/auth');
const { createPatient, getPatientById } = require('../controllers/patientController');

const router = express.Router();

router.post('/', authenticate, authorize('PATIENT', 'STAFF'), createPatient);
router.get('/:id', authenticate, authorize('PATIENT', 'DOCTOR', 'STAFF'), getPatientById);

module.exports = router;

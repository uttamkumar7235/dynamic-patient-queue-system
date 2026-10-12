const express = require('express');
const { authenticate, authorize } = require('../middleware/auth');
const { listDoctors, getDoctorById, updateDoctorAvailability } = require('../controllers/doctorController');

const router = express.Router();

router.get('/', authenticate, authorize('PATIENT', 'DOCTOR', 'STAFF'), listDoctors);
router.get('/:id', authenticate, authorize('PATIENT', 'DOCTOR', 'STAFF'), getDoctorById);
router.patch('/:id/availability', authenticate, authorize('DOCTOR', 'STAFF'), updateDoctorAvailability);

module.exports = router;

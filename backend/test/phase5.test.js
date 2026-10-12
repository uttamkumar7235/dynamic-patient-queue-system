const test = require('node:test');
const assert = require('node:assert/strict');
const { createPatient, getPatientById } = require('../src/controllers/patientController');
const { listDoctors, getDoctorById, updateDoctorAvailability } = require('../src/controllers/doctorController');
const Doctor = require('../src/models/Doctor');
const Patient = require('../src/models/Patient');

async function makeReq(overrides = {}) {
  return {
    headers: {},
    params: {},
    body: {},
    user: { id: '507f1f77bcf86cd799439011', role: 'PATIENT' },
    ...overrides
  };
}

async function makeRes() {
  return {
    statusCode: 200,
    body: undefined,
    status(code) {
      this.statusCode = code;
      return this;
    },
    json(payload) {
      this.body = payload;
      return this;
    }
  };
}

test('POST /api/patients creates a patient for a PATIENT account and validates input', async () => {
  const originalCreate = Patient.create;
  const originalFindOne = Patient.findOne;

  try {
    Patient.create = async (data) => ({ _id: 'patient-1', ...data });
    Patient.findOne = async () => null;

    const req = await makeReq({
      user: { id: '507f1f77bcf86cd799439011', role: 'PATIENT' },
      body: {
        name: 'Test Patient',
        age: 29,
        gender: 'Female',
        contact: '+1234567890'
      }
    });
    const res = await makeRes();

    await createPatient(req, res);

    assert.equal(res.statusCode, 201);
    assert.equal(res.body.patient.name, 'Test Patient');
  } finally {
    Patient.create = originalCreate;
    Patient.findOne = originalFindOne;
  }
});

test('POST /api/patients rejects invalid input and unauthorized role', async () => {
  const badInput = await makeReq({
    user: { id: '507f1f77bcf86cd799439011', role: 'PATIENT' },
    body: { name: '', age: 'abc', gender: 'Male', contact: '+1' }
  });
  const badInputRes = await makeRes();
  await createPatient(badInput, badInputRes);
  assert.equal(badInputRes.statusCode, 400);

  const forbidden = await makeReq({
    user: { id: '507f1f77bcf86cd799439011', role: 'DOCTOR' },
    body: { name: 'Forbidden', age: 30, gender: 'Male', contact: '+123' }
  });
  const forbiddenRes = await makeRes();
  await createPatient(forbidden, forbiddenRes);
  assert.equal(forbiddenRes.statusCode, 403);
});

test('GET /api/patients/:id returns 404 for missing record and forbids PATIENT access to another patient', async () => {
  const originalFindById = Patient.findById;

  try {
    Patient.findById = async () => null;
    const missingReq = await makeReq({ params: { id: '507f1f77bcf86cd799439011' } });
    const missingRes = await makeRes();
    await getPatientById(missingReq, missingRes);
    assert.equal(missingRes.statusCode, 404);

    Patient.findById = async () => ({
      _id: 'patient-other',
      userId: '507f1f77bcf86cd799439013',
      name: 'Private Patient'
    });

    const forbiddenReq = await makeReq({
      user: { id: '507f1f77bcf86cd799439011', role: 'PATIENT' },
      params: { id: '507f1f77bcf86cd799439012' }
    });
    const forbiddenRes = await makeRes();
    await getPatientById(forbiddenReq, forbiddenRes);
    assert.equal(forbiddenRes.statusCode, 403);
  } finally {
    Patient.findById = originalFindById;
  }
});

test('GET /api/doctors returns list and GET by ID validates and handles missing records', async () => {
  const originalFind = Doctor.find;
  const originalFindById = Doctor.findById;

  try {
    Doctor.find = () => ({
      sort: () => [{ _id: 'doctor-1', name: 'Alpha Doctor' }]
    });
    const listReq = await makeReq({ user: { id: '507f1f77bcf86cd799439011', role: 'PATIENT' } });
    const listRes = await makeRes();
    await listDoctors(listReq, listRes);
    assert.equal(listRes.statusCode, 200);
    assert.ok(Array.isArray(listRes.body.doctors));

    Doctor.findById = async () => ({ _id: 'doctor-1', name: 'Alpha Doctor' });
    const foundReq = await makeReq({ user: { id: '507f1f77bcf86cd799439011', role: 'PATIENT' }, params: { id: '507f1f77bcf86cd799439011' } });
    const foundRes = await makeRes();
    await getDoctorById(foundReq, foundRes);
    assert.equal(foundRes.statusCode, 200);
    assert.equal(foundRes.body.doctor.name, 'Alpha Doctor');

    const invalidReq = await makeReq({ user: { id: '507f1f77bcf86cd799439011', role: 'PATIENT' }, params: { id: 'bad-id' } });
    const invalidRes = await makeRes();
    await getDoctorById(invalidReq, invalidRes);
    assert.equal(invalidRes.statusCode, 400);

    Doctor.findById = async () => null;
    const missingReq = await makeReq({ user: { id: '507f1f77bcf86cd799439011', role: 'PATIENT' }, params: { id: '507f1f77bcf86cd799439099' } });
    const missingRes = await makeRes();
    await getDoctorById(missingReq, missingRes);
    assert.equal(missingRes.statusCode, 404);
  } finally {
    Doctor.find = originalFind;
    Doctor.findById = originalFindById;
  }
});

test('PATCH /api/doctors/:id/availability updates only allowed roles and rejects invalid input', async () => {
  const originalFindById = Doctor.findById;

  try {
    const doctor = {
      _id: '507f1f77bcf86cd799439022',
      isAvailable: true,
      save: async function () {
        return this;
      }
    };

    Doctor.findById = async () => doctor;

    const allowedReq = await makeReq({
      user: { id: doctor._id, role: 'DOCTOR' },
      params: { id: doctor._id },
      body: { isAvailable: false }
    });
    const allowedRes = await makeRes();
    await updateDoctorAvailability(allowedReq, allowedRes);
    assert.equal(allowedRes.statusCode, 200);
    assert.equal(allowedRes.body.doctor.isAvailable, false);

    const forbiddenReq = await makeReq({
      user: { id: '507f1f77bcf86cd799439011', role: 'PATIENT' },
      params: { id: doctor._id },
      body: { isAvailable: true }
    });
    const forbiddenRes = await makeRes();
    await updateDoctorAvailability(forbiddenReq, forbiddenRes);
    assert.equal(forbiddenRes.statusCode, 403);

    const invalidReq = await makeReq({
      user: { id: doctor._id, role: 'DOCTOR' },
      params: { id: doctor._id },
      body: { isAvailable: 'nope' }
    });
    const invalidRes = await makeRes();
    await updateDoctorAvailability(invalidReq, invalidRes);
    assert.equal(invalidRes.statusCode, 400);
  } finally {
    Doctor.findById = originalFindById;
  }
});

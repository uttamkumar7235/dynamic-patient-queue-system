const dotenv = require('dotenv');
dotenv.config();

const mongoose = require('mongoose');

const User = require('./src/models/User');
const Patient = require('./src/models/Patient');
const Doctor = require('./src/models/Doctor');
const Queue = require('./src/models/Queue');

async function runModelTest() {
  const created = {};

  try {
    const mongoUri = process.env.MONGODB_URI;
    if (!mongoUri) {
      throw new Error('MONGODB_URI is not defined in the environment.');
    }

    await mongoose.connect(mongoUri, { serverSelectionTimeoutMS: 5000 });
    console.log('MongoDB connected successfully.');

    const user = await User.create({
      name: 'Temp Test User',
      email: 'temp.user@example.com',
      passwordHash: 'abcd'.repeat(15),
      role: 'PATIENT'
    });
    created.user = user;
    console.log('Created User:', user.toJSON());

    const patient = await Patient.create({
      name: 'Temp Test Patient',
      age: 32,
      gender: 'Male',
      contact: '+1234567890'
    });
    created.patient = patient;
    console.log('Created Patient:', patient.toJSON());

    const doctor = await Doctor.create({
      name: 'Temp Test Doctor',
      department: 'Cardiology',
      avgConsultTime: 15,
      isAvailable: true,
      shiftStart: '09:00',
      shiftEnd: '17:00'
    });
    created.doctor = doctor;
    console.log('Created Doctor:', doctor.toJSON());

    const queue = await Queue.create({
      patientId: patient._id,
      doctorId: doctor._id,
      tokenNumber: 1,
      queuePosition: 1,
      predictedWaitTime: 20
    });
    created.queue = queue;
    console.log('Created Queue:', queue.toJSON());

    if (queue.status !== 'WAITING') {
      throw new Error(`Queue default status test failed. Expected WAITING but received ${queue.status}`);
    }
    console.log('Queue default status check: PASS');

    const populatedQueue = await Queue.findById(queue._id).populate('patientId').populate('doctorId');
    if (!populatedQueue.patientId || !populatedQueue.doctorId) {
      throw new Error('Queue references are invalid or missing.');
    }
    console.log('Queue references check: PASS');

    try {
      await User.create({
        name: 'Invalid User',
        email: 'bad-email',
        passwordHash: 'abcd'.repeat(15),
        role: 'PATIENT'
      });
      throw new Error('Invalid User test failed: invalid email should have been rejected.');
    } catch (error) {
      console.log('Invalid User test: Mongoose rejected invalid data.');
    }

    try {
      await Patient.create({
        name: 'Invalid Patient',
        age: 150,
        gender: 'Male',
        contact: '+1234567890'
      });
      throw new Error('Invalid Patient test failed: age 150 should have been rejected.');
    } catch (error) {
      console.log('Invalid Patient test: Mongoose rejected invalid data.');
    }

    console.log('All model checks completed successfully.');
  } catch (error) {
    console.error('Model test failed:', error.message);
  } finally {
    try {
      if (mongoose.connection.readyState === 1) {
        const deleteTasks = [];

        if (created.queue) {
          deleteTasks.push(Queue.deleteOne({ _id: created.queue._id }));
        }
        if (created.doctor) {
          deleteTasks.push(Doctor.deleteOne({ _id: created.doctor._id }));
        }
        if (created.patient) {
          deleteTasks.push(Patient.deleteOne({ _id: created.patient._id }));
        }
        if (created.user) {
          deleteTasks.push(User.deleteOne({ _id: created.user._id }));
        }

        await Promise.all(deleteTasks);
        console.log('Temporary test documents deleted.');
      }
    } catch (cleanupError) {
      console.error('Cleanup failed:', cleanupError.message);
    }

    try {
      await mongoose.disconnect();
      console.log('MongoDB disconnected.');
    } catch (disconnectError) {
      console.error('MongoDB disconnect failed:', disconnectError.message);
    }
  }
}

runModelTest();

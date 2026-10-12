const mongoose = require('mongoose');

const queueSchema = new mongoose.Schema(
  {
    patientId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Patient',
      required: [true, 'Patient ID is required']
    },
    doctorId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Doctor',
      required: [true, 'Doctor ID is required']
    },
    tokenNumber: {
      type: Number,
      required: [true, 'Token number is required'],
      min: [1, 'Token number must be a positive number'],
      validate: {
        validator: (value) => Number.isInteger(value) && value > 0,
        message: 'Token number must be a positive integer'
      }
    },
    status: {
      type: String,
      required: [true, 'Queue status is required'],
      enum: {
        values: ['WAITING', 'CALLED', 'IN_CONSULTATION', 'COMPLETED', 'CANCELLED', 'NO_SHOW'],
        message: 'Status must be one of WAITING, CALLED, IN_CONSULTATION, COMPLETED, CANCELLED, or NO_SHOW'
      },
      default: 'WAITING',
      uppercase: true,
      trim: true
    },
    queuePosition: {
      type: Number,
      min: [1, 'Queue position must be a positive number'],
      validate: {
        validator: (value) => value === null || (Number.isInteger(value) && value > 0),
        message: 'Queue position must be a positive integer when provided'
      }
    },
    predictedWaitTime: {
      type: Number,
      default: 0,
      min: [0, 'Predicted wait time cannot be negative'],
      validate: {
        validator: (value) => Number.isFinite(value) && value >= 0,
        message: 'Predicted wait time must be a non-negative number in minutes'
      }
    },
    joinedAt: {
      type: Date,
      default: Date.now
    },
    consultationStartedAt: {
      type: Date
    },
    consultationCompletedAt: {
      type: Date
    }
  },
  {
    timestamps: true,
    versionKey: false
  }
);

queueSchema.index({ patientId: 1, doctorId: 1 });
queueSchema.index({ doctorId: 1, status: 1, queuePosition: 1 });
queueSchema.index({ status: 1, joinedAt: 1 });

queueSchema.set('toJSON', {
  transform: (doc, ret) => {
    delete ret.__v;
    return ret;
  }
});

queueSchema.set('toObject', {
  transform: (doc, ret) => {
    delete ret.__v;
    return ret;
  }
});

module.exports = mongoose.model('Queue', queueSchema);

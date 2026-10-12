const mongoose = require('mongoose');

const patientSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Name is required'],
      trim: true,
      minlength: [2, 'Name must be at least 2 characters long'],
      maxlength: [100, 'Name cannot exceed 100 characters']
    },
    age: {
      type: Number,
      required: [true, 'Age is required'],
      min: [0, 'Age cannot be negative'],
      max: [120, 'Age must be a realistic value'],
      validate: {
        validator: (value) => Number.isFinite(value) && value % 1 === 0,
        message: 'Age must be a whole number'
      }
    },
    gender: {
      type: String,
      required: [true, 'Gender is required'],
      trim: true,
      minlength: [1, 'Gender cannot be empty'],
      maxlength: [30, 'Gender is too long'],
      match: [/^[A-Za-z\s-]+$/, 'Gender can only contain letters, spaces, and hyphens']
    },
    contact: {
      type: String,
      required: [true, 'Contact information is required'],
      trim: true,
      minlength: [5, 'Contact information must be at least 5 characters long'],
      maxlength: [200, 'Contact information is too long'],
      match: [/^[A-Za-z0-9+()\s-]+$/, 'Contact information contains invalid characters']
    },
    registeredAt: {
      type: Date,
      default: Date.now
    }
  },
  {
    versionKey: false
  }
);

patientSchema.set('toJSON', {
  transform: (doc, ret) => {
    delete ret.__v;
    return ret;
  }
});

patientSchema.set('toObject', {
  transform: (doc, ret) => {
    delete ret.__v;
    return ret;
  }
});

module.exports = mongoose.model('Patient', patientSchema);

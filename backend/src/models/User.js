const mongoose = require('mongoose');

const userSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Name is required'],
      trim: true,
      minlength: [2, 'Name must be at least 2 characters long'],
      maxlength: [100, 'Name cannot exceed 100 characters']
    },
    email: {
      type: String,
      required: [true, 'Email is required'],
      unique: true,
      trim: true,
      lowercase: true,
      match: [/^[^\s@]+@[^\s@]+\.[^\s@]+$/, 'Please provide a valid email address']
    },
    passwordHash: {
      type: String,
      required: [true, 'Password hash is required'],
      trim: true,
      minlength: [60, 'Password hash must be a valid bcrypt hash'],
      maxlength: [255, 'Password hash is too long']
    },
    role: {
      type: String,
      required: [true, 'Role is required'],
      uppercase: true,
      trim: true,
      enum: {
        values: ['PATIENT', 'DOCTOR', 'STAFF'],
        message: 'Role must be one of PATIENT, DOCTOR, or STAFF'
      },
      default: 'PATIENT'
    }
  },
  {
    timestamps: true
  }
);

userSchema.index({ email: 1 }, { unique: true });

userSchema.set('toJSON', {
  transform: (doc, ret) => {
    delete ret.passwordHash;
    delete ret.__v;
    return ret;
  }
});

userSchema.set('toObject', {
  transform: (doc, ret) => {
    delete ret.passwordHash;
    delete ret.__v;
    return ret;
  }
});

module.exports = mongoose.model('User', userSchema);

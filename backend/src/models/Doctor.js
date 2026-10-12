const mongoose = require('mongoose');

const doctorSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Name is required'],
      trim: true,
      minlength: [2, 'Name must be at least 2 characters long'],
      maxlength: [100, 'Name cannot exceed 100 characters']
    },
    department: {
      type: String,
      required: [true, 'Department is required'],
      trim: true,
      minlength: [2, 'Department must be at least 2 characters long'],
      maxlength: [100, 'Department cannot exceed 100 characters']
    },
    avgConsultTime: {
      type: Number,
      required: [true, 'Average consultation time is required'],
      min: [1, 'Average consultation time must be greater than 0 minutes'],
      max: [300, 'Average consultation time must be realistic'],
      validate: {
        validator: (value) => Number.isFinite(value) && value > 0,
        message: 'Average consultation time must be a positive number in minutes'
      }
    },
    isAvailable: {
      type: Boolean,
      default: true
    },
    shiftStart: {
      type: String,
      trim: true,
      validate: {
        validator: function (value) {
          if (!value) return true;
          return /^([01]\d|2[0-3]):([0-5]\d)$/.test(value);
        },
        message: 'Shift start must be in HH:mm format'
      }
    },
    shiftEnd: {
      type: String,
      trim: true,
      validate: {
        validator: function (value) {
          if (!value) return true;
          return /^([01]\d|2[0-3]):([0-5]\d)$/.test(value);
        },
        message: 'Shift end must be in HH:mm format'
      }
    }
  },
  {
    timestamps: true,
    versionKey: false
  }
);

doctorSchema.set('toJSON', {
  transform: (doc, ret) => {
    delete ret.__v;
    return ret;
  }
});

doctorSchema.set('toObject', {
  transform: (doc, ret) => {
    delete ret.__v;
    return ret;
  }
});

module.exports = mongoose.model('Doctor', doctorSchema);

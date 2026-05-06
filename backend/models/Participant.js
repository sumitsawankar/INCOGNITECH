const mongoose = require('mongoose');

const participantSchema = new mongoose.Schema(
  {
    name: { type: String, required: true },
    email: { type: String, required: true },
    college: { type: String, required: true },
    eventId: {
      type: mongoose.Schema.Types.ObjectId,
      required: true,
      ref: 'Event',
    },
  },
  { timestamps: true }
);

module.exports = mongoose.model('Participant', participantSchema);

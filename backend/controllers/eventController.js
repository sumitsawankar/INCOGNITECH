const Event = require('../models/Event');
const Participant = require('../models/Participant');
const upload = require('../middleware/uploadMiddleware');
const { uploadBufferToCloudinary } = require('../utils/cloudinaryUpload');

const eventImageUpload = upload.single('image');

// @desc    Get all events
// @route   GET /api/events
// @access  Public
const getEvents = async (req, res) => {
  try {
    const events = await Event.find().sort({ date: -1 });
    res.json(events);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Create an event (admin)
// @route   POST /api/events
// @access  Private/Admin
const createEvent = async (req, res) => {
  try {
    const { title, description, date, location, image } = req.body;

    if (!title || !description || !date || !location) {
      return res.status(400).json({ message: 'title, description, date, location are required' });
    }

    let finalImage = image || '';
    if (req.file?.buffer) {
      const result = await uploadBufferToCloudinary(req.file.buffer, {
        folder: 'incognitech/events',
      });
      finalImage = result.secure_url;
    }

    const created = await Event.create({
      title,
      description,
      date,
      location,
      image: finalImage,
    });

    res.status(201).json(created);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Register for an event
// @route   POST /api/events/register
// @access  Private
const registerEvent = async (req, res) => {
  try {
    const { eventId, college } = req.body;

    if (!eventId || !college) {
      return res.status(400).json({ message: 'eventId and college are required' });
    }

    const event = await Event.findById(eventId);

    if (!event) {
      return res.status(404).json({ message: 'Event not found' });
    }

    // Check if already registered (by email + event)
    const alreadyRegistered = await Participant.findOne({
      email: req.user.email,
      eventId,
    });

    if (alreadyRegistered) {
      return res.status(400).json({ message: 'You have already registered for this event' });
    }

    const participant = await Participant.create({
      name: req.user.name,
      email: req.user.email,
      college,
      eventId,
    });

    res.status(201).json({
      success: true,
      message: 'Successfully registered for the event',
      participant,
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Register for an event (public endpoint to match spec)
// @route   POST /api/register-event
// @access  Public
const registerEventPublic = async (req, res) => {
  try {
    const { name, email, college, eventId } = req.body;

    if (!name || !email || !college || !eventId) {
      return res.status(400).json({ message: 'name, email, college, eventId are required' });
    }

    const event = await Event.findById(eventId);
    if (!event) {
      return res.status(404).json({ message: 'Event not found' });
    }

    const alreadyRegistered = await Participant.findOne({ email, eventId });
    if (alreadyRegistered) {
      return res.status(400).json({ message: 'You have already registered for this event' });
    }

    const participant = await Participant.create({ name, email, college, eventId });

    res.status(201).json({
      success: true,
      message: 'Successfully registered for the event',
      participant,
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Get participants for an event (useful for admin or the frontend logic)
// @route   GET /api/events/:id/participants
// @access  Private (Admin only later, or public depending on need. Making it Private for now generally to protect user data)
const getParticipants = async (req, res) => {
  try {
    const participants = await Participant.find({ eventId: req.params.id }).sort({ createdAt: -1 });
    res.json(participants);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Get all participants (admin)
// @route   GET /api/participants
// @access  Private/Admin
const getAllParticipants = async (req, res) => {
  try {
    const participants = await Participant.find({})
      .populate('eventId', 'title date location')
      .sort({ createdAt: -1 });
    res.json(participants);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

module.exports = {
  getEvents,
  createEvent,
  registerEvent,
  registerEventPublic,
  getParticipants,
  getAllParticipants,
  eventImageUpload,
};

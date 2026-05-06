const express = require('express');
const router = express.Router();
const {
  getEvents,
  createEvent,
  registerEvent,
  getParticipants,
  eventImageUpload,
} = require('../controllers/eventController');
const { protect, admin } = require('../middlewares/authMiddleware');

router.get('/', getEvents);
router.post('/', protect, admin, eventImageUpload, createEvent);
router.post('/register', protect, registerEvent);
router.get('/:id/participants', protect, admin, getParticipants); // Protect this endpoint to admin

module.exports = router;

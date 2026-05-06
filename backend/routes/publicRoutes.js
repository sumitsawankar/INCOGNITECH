const express = require('express');
const router = express.Router();

const {
  registerEventPublic,
  getAllParticipants,
} = require('../controllers/eventController');

const { protect, admin } = require('../middlewares/authMiddleware');

// Matches requested API spec
router.post('/register-event', registerEventPublic);
router.get('/participants', protect, admin, getAllParticipants);

module.exports = router;


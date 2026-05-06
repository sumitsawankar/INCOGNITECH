const express = require('express');
const router = express.Router();
const { getUserProfile, avatarUpload, updateUserAvatar } = require('../controllers/userController');
const { protect } = require('../middlewares/authMiddleware');

router.get('/profile', protect, getUserProfile);
router.put('/profile/avatar', protect, avatarUpload, updateUserAvatar);

module.exports = router;

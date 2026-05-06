const express = require('express');
const router = express.Router();
const { getUsers, deleteUser, getAdminEvents } = require('../controllers/adminController');
const { protect, admin } = require('../middlewares/authMiddleware');

router.route('/users').get(protect, admin, getUsers);
router.route('/user/:id').delete(protect, admin, deleteUser);
router.route('/events').get(protect, admin, getAdminEvents);

module.exports = router;

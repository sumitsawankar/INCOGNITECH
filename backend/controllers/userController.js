const User = require('../models/User');

// @desc    Get user profile
// @route   GET /api/user/profile
// @access  Private
const getUserProfile = async (req, res) => {
  try {
    const user = await User.findById(req.user._id);

    if (user) {
      res.json({
        _id: user._id,
        name: user.name,
        email: user.email,
        role: user.role,
        avatar: user.avatar,
      });
    } else {
      res.status(404).json({ message: 'User not found' });
    }
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Upload/update profile image (avatar)
// @route   PUT /api/user/profile/avatar
// @access  Private
const upload = require('../middleware/uploadMiddleware');
const { uploadBufferToCloudinary } = require('../utils/cloudinaryUpload');

const avatarUpload = upload.single('image');

const updateUserAvatar = async (req, res) => {
  try {
    if (!req.file?.buffer) {
      return res.status(400).json({ message: 'image file is required' });
    }

    const result = await uploadBufferToCloudinary(req.file.buffer, {
      folder: 'incognitech/avatars',
      publicId: `user_${req.user._id}`,
    });

    const user = await User.findById(req.user._id);
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    user.avatar = result.secure_url;
    await user.save();

    res.json({ avatar: user.avatar });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

module.exports = {
  getUserProfile,
  avatarUpload,
  updateUserAvatar,
};

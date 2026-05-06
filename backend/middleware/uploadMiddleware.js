const multer = require('multer');

// Store in memory, upload to Cloudinary from buffer.
const storage = multer.memoryStorage();

function fileFilter(req, file, cb) {
  // Accept images only for now (blog/event/profile)
  if (!file.mimetype || !file.mimetype.startsWith('image/')) {
    return cb(new Error('Only image files are allowed'));
  }
  return cb(null, true);
}

const upload = multer({
  storage,
  fileFilter,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
});

module.exports = upload;


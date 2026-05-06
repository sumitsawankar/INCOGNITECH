const streamifier = require('streamifier');
const { cloudinary } = require('../config/cloudinary');

function uploadBufferToCloudinary(buffer, { folder, publicId } = {}) {
  return new Promise((resolve, reject) => {
    const uploadStream = cloudinary.uploader.upload_stream(
      {
        folder,
        public_id: publicId,
        resource_type: 'image',
      },
      (err, result) => {
        if (err) return reject(err);
        return resolve(result);
      }
    );

    streamifier.createReadStream(buffer).pipe(uploadStream);
  });
}

module.exports = { uploadBufferToCloudinary };


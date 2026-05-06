const express = require('express');
const router = express.Router();
const {
  getBlogs,
  getBlogById,
  createBlog,
  updateBlog,
  deleteBlog,
  blogImageUpload,
} = require('../controllers/blogController');
const { protect, admin } = require('../middlewares/authMiddleware');

router.route('/').get(getBlogs).post(protect, admin, blogImageUpload, createBlog);
router
  .route('/:id')
  .get(getBlogById)
  .put(protect, admin, blogImageUpload, updateBlog)
  .delete(protect, admin, deleteBlog);

module.exports = router;

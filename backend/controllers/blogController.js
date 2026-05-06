const Blog = require('../models/Blog');
const upload = require('../middleware/uploadMiddleware');
const { uploadBufferToCloudinary } = require('../utils/cloudinaryUpload');

// Expose multer for routes
const blogImageUpload = upload.single('image');

// @desc    Get all blogs
// @route   GET /api/blogs
// @access  Public
const getBlogs = async (req, res) => {
  try {
    const blogs = await Blog.find().populate('author', 'name avatar').sort({ createdAt: -1 });
    res.json(blogs);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Get single blog
// @route   GET /api/blogs/:id
// @access  Public
const getBlogById = async (req, res) => {
  try {
    const blog = await Blog.findById(req.params.id).populate('author', 'name avatar');

    if (blog) {
      res.json(blog);
    } else {
      res.status(404).json({ message: 'Blog not found' });
    }
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Create a blog
// @route   POST /api/blogs
// @access  Private/Admin
const createBlog = async (req, res) => {
  try {
    const { title, description, content, image } = req.body;

    if (!title || !content) {
      return res.status(400).json({ message: 'title and content are required' });
    }

    let finalImage = image || '';
    if (req.file?.buffer) {
      const result = await uploadBufferToCloudinary(req.file.buffer, {
        folder: 'incognitech/blogs',
      });
      finalImage = result.secure_url;
    }

    const blog = new Blog({
      title,
      description: description || '',
      content,
      image: finalImage,
      author: req.user._id,
    });

    const createdBlog = await blog.save();
    res.status(201).json(createdBlog);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Update a blog
// @route   PUT /api/blogs/:id
// @access  Private/Admin
const updateBlog = async (req, res) => {
  try {
    const { title, description, content, image } = req.body;

    const blog = await Blog.findById(req.params.id);

    if (blog) {
      blog.title = title || blog.title;
      blog.description = description ?? blog.description;
      blog.content = content || blog.content;
      blog.image = image || blog.image;

      if (req.file?.buffer) {
        const result = await uploadBufferToCloudinary(req.file.buffer, {
          folder: 'incognitech/blogs',
        });
        blog.image = result.secure_url;
      }

      const updatedBlog = await blog.save();
      res.json(updatedBlog);
    } else {
      res.status(404).json({ message: 'Blog not found' });
    }
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Delete a blog
// @route   DELETE /api/blogs/:id
// @access  Private/Admin
const deleteBlog = async (req, res) => {
  try {
    const blog = await Blog.findById(req.params.id);

    if (blog) {
      await Blog.deleteOne({ _id: req.params.id });
      res.json({ message: 'Blog removed' });
    } else {
      res.status(404).json({ message: 'Blog not found' });
    }
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

module.exports = {
  getBlogs,
  getBlogById,
  createBlog,
  updateBlog,
  deleteBlog,
  blogImageUpload,
};

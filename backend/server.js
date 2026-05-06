const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');
const connectDB = require('./config/db');
const { notFound, errorHandler } = require('./middleware/errorMiddleware');
const { initCloudinary } = require('./config/cloudinary');

// Load env vars
dotenv.config();

// Connect to database
connectDB();

// Initialize Cloudinary (throws if env vars missing)
initCloudinary();

const app = express();

// Middleware
app.use(
  cors({
    origin: (origin, cb) => {
      // Allow same-origin / server-to-server / curl
      if (!origin) return cb(null, true);

      const allowed = [process.env.CLIENT_URL].filter(Boolean);
      // If CLIENT_URL isn't configured on the deployed backend, don't hard-block all browsers.
      // (Set CLIENT_URL in production for best security.)
      if (allowed.length === 0) return cb(null, true);
      if (allowed.includes(origin)) return cb(null, true);

      return cb(new Error('Not allowed by CORS'));
    },
    credentials: true,
  })
);
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Note: uploads are served from Cloudinary, not local disk.

// Define Routes
app.use('/api/auth', require('./routes/authRoutes'));
app.use('/api/user', require('./routes/userRoutes'));
app.use('/api/contact', require('./routes/contactRoutes'));
app.use('/api/events', require('./routes/eventRoutes'));
app.use('/api/blogs', require('./routes/blogRoutes'));
app.use('/api/blog', require('./routes/blogRoutes')); // alias to match spec
app.use('/api/admin', require('./routes/adminRoutes'));
app.use('/api', require('./routes/publicRoutes')); // /register-event, /participants

// Basic route
app.get('/', (req, res) => {
  res.send('API is running...');
});

// Error Handler Middleware
app.use(notFound);
app.use(errorHandler);

const PORT = process.env.PORT || 5000;

app.listen(PORT, console.log(`Server running in ${process.env.NODE_ENV} mode on port ${PORT}`));

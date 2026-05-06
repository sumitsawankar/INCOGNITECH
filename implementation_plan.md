# Backend Implementation Plan for Tech Community Platform

This document outlines the architecture and implementation steps for building the backend system using Node.js, Express, and MongoDB.

## User Review Required
> [!IMPORTANT]
> - Do you have a specific preference for the MongoDB connection string (e.g., local MongoDB or MongoDB Atlas)? I will use a placeholder (`mongodb://localhost:27017/tech_community`) by default.
> - For file upload, are you okay with using local storage inside the backend (`/uploads` folder) as a starting point, or do you explicitly need me to integrate Cloudinary/AWS S3 right now? I will implement a local setup using **Multer** for simplicity, and outline how it can be connected to Cloudinary.

## Proposed Changes

### Project Initialization
Initialize a new Node.js project in the `backend` directory and install dependencies: `express`, `mongoose`, `cors`, `dotenv`, `bcryptjs`, `jsonwebtoken`, and `multer`.

---

### Folder Structure
#### [NEW] `backend/server.js`
The main entry point for the application.

#### [NEW] `backend/config/db.js`
Handles MongoDB connection using Mongoose.

#### [NEW] `backend/.env`
Environment variables, including `PORT`, `MONGO_URI`, and `JWT_SECRET`.

---

### Models (Database Schema)
#### [NEW] `backend/models/User.js`
Schema for users with properties: `name`, `email`, `password`, `role` (user, admin), and `avatar`.

#### [NEW] `backend/models/ContactMessage.js`
Schema for contact forms: `name`, `email`, `message`, `date`.

#### [NEW] `backend/models/Event.js`
Schema for events/hackathons: `title`, `description`, `date`, `location`, `image`.

#### [NEW] `backend/models/Participant.js`
Schema for event registrations: tracking which `userId` registered for which `eventId`.

#### [NEW] `backend/models/Blog.js`
Schema for blog posts: `title`, `content`, `author` (admin id), `image`, `createdAt`.

---

### Middlewares
#### [NEW] `backend/middlewares/authMiddleware.js`
Verifies JWT tokens.

#### [NEW] `backend/middlewares/adminMiddleware.js`
Ensures the authenticated user has an admin role.

#### [NEW] `backend/middlewares/uploadMiddleware.js`
Configures Multer for handling file uploads.

---

### Controllers & Routes
#### [NEW] `backend/controllers/authController.js` & `backend/routes/authRoutes.js`
Handles `POST /api/auth/signup`, `POST /api/auth/login`.

#### [NEW] `backend/controllers/userController.js` & `backend/routes/userRoutes.js`
Handles `GET /api/user/profile`.

#### [NEW] `backend/controllers/contactController.js` & `backend/routes/contactRoutes.js`
Handles `POST /api/contact`.

#### [NEW] `backend/controllers/eventController.js` & `backend/routes/eventRoutes.js`
Handles `GET /api/events`, `POST /api/register-event`, `GET /api/participants`.

#### [NEW] `backend/controllers/blogController.js` & `backend/routes/blogRoutes.js`
Handles blog CRUD operations.

#### [NEW] `backend/controllers/adminController.js` & `backend/routes/adminRoutes.js`
Handles administrative operations like users, events, and blog management.

## Verification Plan

### Automated/Manual Verification
1. I will run the server locally and ensure no setup errors occur.
2. I will use the `run_command` and `read_url_content` (or `curl`) tools to verify API endpoints locally (e.g., creating a user, logging in, creating an event).
3. Ensure CORS is enabled to allow the `incognitech.vercel.app` frontend to communicate.

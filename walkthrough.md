# Backend Implementation Walkthrough

## Summary of Changes

A complete Node.js/Express backend has been built to support the Incognitech website. It connects to MongoDB and provides RESTful APIs for all required functionalities.

### Architecture
- **Tech Stack**: Node.js, Express.js, MongoDB + Mongoose, JWT authentication.
- **Project Structure**: Organized by `controllers/`, `models/`, `routes/`, `middlewares/`, and `config/`.

### Functionality Implemented

1. **Authentication System** (`api/auth` & `api/user`)
   - Secure passwords using `bcryptjs`.
   - Token-based auth using `jsonwebtoken`.
   - Support for [admin](file:///c:/Users/sumit/Desktop/ANTIGRAVITY/backend/middlewares/authMiddleware.js#35-43) vs `user` roles.
2. **Contact Form** (`api/contact`)
   - Accepts form submissions from the frontend and stores them.
3. **Event Management** (`api/events`)
   - List all available hackathons/events.
   - Allow users to register.
   - Admin view to get all participants.
4. **Blog System** (`api/blogs`)
   - Full CRUD support for blogs, restricted to Admin.
5. **Admin Dashboard** (`api/admin`)
   - View/delete users and view events.
6. **File Upload**
   - Configured `multer` locally to save user avatars, event posters, or blog images to `uploads/`.

## Verification Steps Performed

- Successfully executed `node server.js` which confirmed:
  - Dotenv correctly loads credentials.
  - Express router successfully wires all 6 modules (Auth, User, Contact, Event, Blog, Admin).
  - MongoDB connection string format is recognized.
  - Server starts locally and listens on Port `5000` (or the [.env](file:///c:/Users/sumit/Desktop/ANTIGRAVITY/backend/.env) provided port).

## Next Steps for the User

1. **Database Setup**: Currently, `MONGO_URI` in [backend/.env](file:///c:/Users/sumit/Desktop/ANTIGRAVITY/backend/.env) is set to `mongodb://localhost:27017/tech_community`. You should replace this with your MongoDB Atlas URI if you want to deploy to the web.
2. **Frontend Wiring**: Point your frontend API calls from `fetch('/api/...')` to your actual backend domain, or configure a proxy in Vercel.
3. **Deployment**: Upload this `backend` folder as its own project to Render or Railway. Make sure to define the [.env](file:///c:/Users/sumit/Desktop/ANTIGRAVITY/backend/.env) variables in their dashboards.

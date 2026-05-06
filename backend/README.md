# Tech Community Backend

This is the backend API for the Incognitech website. It is built using Node.js, Express, and MongoDB.

## Getting Started

### Prerequisites

- Node.js installed
- MongoDB installed locally or a MongoDB Atlas URI

### Setup

1. **Clone/Navigate to the backend directory**
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Environment Variables:**
   A `.env` file is already created. Make sure it contains correct values:
   ```env
   NODE_ENV=development
   PORT=5000
   MONGO_URI=mongodb://localhost:27017/tech_community
   JWT_SECRET=your_super_secret_jwt_key
   ```
4. **Run the server:**
   ```bash
   # Make sure MongoDB is running if using a local DB!
   node server.js
   ```

## Development and Deployment

*   To run in dev mode with auto-reload, you can install `nodemon` (`npm install -g nodemon`) and run `nodemon server.js`.
*   To deploy on platforms like Render or Railway, simply upload the `backend` folder as the root directory of your repo and specify `node server.js` as the start command. Set up Environment Variables on the platform.

## API Endpoints Overview

### Authentication
*   `POST /api/auth/signup` - Register a user (Requires: name, email, password)
*   `POST /api/auth/login` - Authenticate a user & get token (Requires: email, password)

### User Profile
*   `GET /api/user/profile` - Get the logged-in user's profile (Requires: Bearer token)

### Contact Forms
*   `POST /api/contact` - Submit the contact form (Requires: name, email, message)

### Events / Hackathons
*   `GET /api/events` - Get all events
*   `POST /api/events/register` - Register for a specific event (Requires Bearer token, and `eventId` in body)
*   `GET /api/events/:id/participants` - (Admin only) Get participants for an event (Requires Bearer token)

### Blogs
*   `GET /api/blogs` - Get all blogs
*   `GET /api/blogs/:id` - Get a single blog by ID
*   `POST /api/blogs` - (Admin only) Create a new blog post
*   `PUT /api/blogs/:id` - (Admin only) Update a blog post
*   `DELETE /api/blogs/:id` - (Admin only) Delete a blog post

### Admin Dashboard
*   `GET /api/admin/users` - (Admin only) Get all users
*   `DELETE /api/admin/user/:id` - (Admin only) Delete a specific user
*   `GET /api/admin/events` - (Admin only) Get events for dashboard management

## Connection to Frontend

To use this backend from the frontend:
1. Since we use `cors()` in `server.js`, requests from the frontend domain (or `localhost`) will be permitted.
2. In the Vercel deployed frontend (or local dev environment), prepend endpoints with the deployed backend URL (e.g., `https://my-backend.onrender.com/api/contact`).

const mongoose = require('mongoose');

// Define User schema
const userSchema = new mongoose.Schema({
  firstName: String,
  lastName: String,
  username: { type: String, unique: true },
  email: { type: String, unique: true },
  password: String
});

// Create User model
const User = mongoose.model('User', userSchema);

module.exports = User;

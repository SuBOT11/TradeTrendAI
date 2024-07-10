
const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const User = require('../userModel');

const router = express.Router();
const { MongoClient } = require('mongodb');


// MongoDB connection URL
const url = 'mongodb://172.18.0.2:27017/Users';

// Connect to MongoDB
const client = new MongoClient(url, { useNewUrlParser: true, useUnifiedTopology: true });

client.connect()
  .then(() => {
    console.log('Connected to MongoDB');
  })
  .catch(err => {
    console.error('Failed to connect to MongoDB', err);
  });




// Route to handle user registration
router.post('/register', async (req, res) => {
    console.log(req.body)
  try {
    const db = client.db();
    const collection = db.collection('user');
    // Check if the user already exists
    let existingUser = await collection.findOne({ username: req.body.username });
    if (existingUser) {
      return res.status(400).json({ message: 'Username already exists' });
    }

    // Hash the password
    const hashedPassword = await bcrypt.hash(req.body.password, 10);

    // Create a new user
    const newUser = new User({
      firstName: req.body.firstName,
      lastName: req.body.lastName,
      username: req.body.username,
      email: req.body.email,
      password: hashedPassword
    });

    // Save the user to the database
    await collection.insertOne(newUser);

    // Respond with a success message
    res.status(201).json({ message: 'User registered successfully' });
  } catch (error) {
    // Handle errors
    console.error('Error registering user', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// Route to handle user login
router.post('/login', async (req, res) => {
  try {
    // Check if the user exists
    const db = client.db();
    const collection = db.collection('user');
    const user = await collection.findOne({ username: req.body.username });
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    // Check if the password is correct
    const passwordMatch = await bcrypt.compare(req.body.password, user.password);
    if (!passwordMatch) {
      return res.status(401).json({ message: 'Invalid password' });
    }

    // Generate JWT token
    const token = jwt.sign({ username: user.username }, 'my-secret-key');

    // Respond with token
    res.status(200).json({ token:token , message:"registration successful"});
  } catch (error) {
    // Handle errors
    console.error('Error logging in user', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

module.exports = router;

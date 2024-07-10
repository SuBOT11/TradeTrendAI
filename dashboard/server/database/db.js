
const { MongoClient } = require('mongodb');

// Connection URI
const uri = 'mongodb://172.18.0.2:27017';

// Create a new MongoClient
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

// Connect to the MongoDB server and return the specified database
async function connect(databaseName) {
  try {
    await client.connect();
    console.log('Connected to MongoDB');
    return client.db(databaseName);
  } catch (error) {
    console.error('Error connecting to MongoDB:', error);
    throw error;
  }
}

module.exports = { connect };
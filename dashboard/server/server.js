// server.js
const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser');
const PORT = process.env.PORT || 5000;
const cors = require('cors');
const graphRoutes = require('./routes/graphRoutes')
const infoRoutes = require('./routes/infoRoutes')
const authRoutes = require('./routes/authRoutes')

const app = express();

app.use(morgan('dev'));

app.use(bodyParser.json());
app.use(cors());
// Routes
app.use('/api/info',infoRoutes)
app.use('/api/graph',graphRoutes)
app.use('/api/auth',authRoutes)



app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});






// Start server


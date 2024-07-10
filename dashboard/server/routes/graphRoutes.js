const express = require('express');
const router = express.Router();
const { MongoClient } = require('mongodb');

// MongoDB connection URL
const url = 'mongodb://172.18.0.2:27017/prediction_db';

// Connect to MongoDB
const client = new MongoClient(url, { useNewUrlParser: true, useUnifiedTopology: true });

client.connect()
  .then(() => {
    console.log('Connected to MongoDB');
  })
  .catch(err => {
    console.error('Failed to connect to MongoDB', err);
  });

// Define routes
router.get('/search', async (req, res) => {
  // Access MongoDB collections using client.db()
  const db = client.db();

  // Perform database operations
  const historyCollection = db.collection('history');
  const predictionsCollection = db.collection('history');
  const {symbol} = req.query;
  const documents = await historyCollection.find({ symbol }).toArray();

    // Send the documents as the response
    res.json(documents);
});

router.get('/stock/candle',async(req,res) => {
    console.log(req.query)
   let  symbol = req.query.symbol;
    let resolution = req.query.resolution;
    let from = req.query.from;
   let  to = req.query.to;
   const res_dic = {
     "1" : "15",
     "15" :"1W",
     "60" : "1M",
     "D" : "1Y"
   }
   const keys = Object.keys(res_dic);
   if (keys.includes(resolution)){
    resolution = res_dic[resolution]

   }
    console.log(keys)
    console.log(resolution)

    let url = `https://merolagani.com/handlers/TechnicalChartHandler.ashx?type=get_advanced_chart&symbol=${symbol}&resolution=${resolution}&rangeStartDate=${from}&rangeEndDate=${to}&from=&isAdjust=1&currencyCode=NPR`
    console.log(url)
    let resp_data;
    fetch(url)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    resp_data = data
    console.log(data); // Process the JSON data here
  res.json(resp_data)
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });

} )

router.get('/prediction',async(req,res) => {
  const db = client.db();

  // Perform database operations

  const predictionsCollection = db.collection('predictions');
  const {symbol} = req.query;
  const documents = await predictionsCollection.find({ symbol }).sort({'last_date':-1}).limit(1).toArray();

  res_document = {
    "c" : [],
    "t" : [],
    "type" : "predicted"
  }
  try{
  pre_arr = documents[0]['prediction_values']
  pre_arr.forEach(doc => {
    res_document["t"].push(Date.parse(doc['Date'])/1000)

    function randomIntFromInterval(min, max) { // min and max included 
        return Math.floor(Math.random() * (max - min + 1) + min)
}

      


    res_document['c'].push((doc['Prediction']).toFixed(2))


  })
}catch (err){
  console.log(err,"error occured")
}
  res.send(res_document)  

  
})

module.exports = router;


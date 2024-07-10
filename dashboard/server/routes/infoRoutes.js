const express = require('express');
const router = express.Router();
const { MongoClient } = require('mongodb');

// MongoDB connection URL
const url = 'mongodb://localhost:27017/ss_summary_db';

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
  const {symbol}  = req.query
  // Perform database operations
  const collection = db.collection('summary');
  fields_to_return = {'symbol':1,'full_name':1}
  const documents = await collection.find({symbol}).toArray();
  console.log(documents)
  new_documents = [] 
  documents.forEach(doc=> {
    new_documents.push({'symbol' : doc['symbol'], 'description' : doc['full_name']})
    
  });

    // Send the documents as the response
    res.json({"result":new_documents});
});



router.get('/stock/profile', async (req, res) => {
  // Access MongoDB collections using client.db()
  const db = client.db();
  const {symbol}  = req.query
  // Perform database operations
  const collection = db.collection('summary');
  fields_to_return = {'symbol':1,'full_name':1}
  const documents = await collection.find({symbol}).toArray();
  new_documents = [] 
  documents.forEach(doc=> {
    new_documents.push({
        'symbol' : doc['symbol'], 
        'description' : doc['full_name'],
        'market_capitalization':doc['market_cap'],
        "sector":doc['sector'],
        "pe_ratio":doc['PE_ratio'],
        "dividend_yield":doc['dividend_yield'],
        "size":doc['size'],
        'eps':doc['earning_per_share'],
        "net_profit":doc['NetProfit'],
        'net_margin' : doc['net_margin'],
        'ROE' : doc['ROE'],
        'ROA': doc['ROA'],
        'book_value' : doc['book_value_per_share'],
        

    })
    
  });

    // Send the documents as the response
    res.json(new_documents[0]);
});

router.get('/quote', async (req, res) => {
  // Access MongoDB collections using client.db()
  const db = client.db();
  const {symbol}  = req.query
  // Perform database operations
  const collection = db.collection('summary');
  fields_to_return = {'symbol':1,'full_name':1}
  const documents = await collection.find({symbol}).toArray();
  new_documents = [] 
  documents.forEach(doc=> {
    new_documents.push({
        "open" : doc['Open'],
        "close" : doc['Close'],
        "high" : doc['High'],
        "low" : doc['Low'],
        "volume" : doc['Volume'],
        "pc_change" : doc['PC_Change'] ,
        "change" : doc['Change'],
        "volume" : doc['Volume'],
        "rsi" : doc['RSI_14'],
        "macd" : doc['MACD'],
        'sma_50' : doc['SMA_50'],
        'volume_trend' : doc['volume_trend'],
        'trend_info' : doc['trend_info'],
    })
    
  });

    // Send the documents as the response
    console.log(new_documents[0])
    res.json(new_documents[0]);
});


router.get('/compare',(req,res) => {
  

})

router.get('/recommend',async (req,res) =>{
  console.log("recieved request")
  const db = client.db();
  const {symbol}  = req.query
  // Perform database operations
  const collection = db.collection('summary');
    
 
  const symbolData = await collection.findOne({ symbol: symbol });
        if (!symbolData) {
            return 'Symbol not found';
        }
  const similarSymbols = await collection.find({
      symbol: { $ne: symbol } // Exclude the input symbol from results
  }).toArray();

  const fil_similar_sym =  similarSymbols.filter(doc => {
            // Check similarity of each field
            let similarFieldsCount = 0;
            for (const key in doc) {
                if (doc.hasOwnProperty(key) && typeof doc[key] === 'number' && doc[key] >= 1) {
                    if (Math.abs(doc[key] - symbolData[key]) <= 2) {
                        similarFieldsCount++;
                    }
                }
            }
            // Consider the document similar if at least one field matches
            return similarFieldsCount > 0;
        }).map(doc => {
            // Extract symbol and similar fields
            const similarFields = {};
            for (const key in doc) {
                if (doc.hasOwnProperty(key) && typeof doc[key] === 'number' && doc[key] >= 1 && Math.abs(doc[key] - symbolData[key]) <= 2) {
                    similarFields[key] = doc[key];
                }
            }
            return { symbol: doc.symbol, similarFields: similarFields };
        });

  const documents = []
  fil_similar_sym.forEach(doc => {
    if ((Object.keys(doc['similarFields'])).length === 3 && documents.length < 10){
      documents.push(doc)
    }
  })


      
  res.json(documents)


})
module.exports = router;

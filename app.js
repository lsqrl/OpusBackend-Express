const express = require('express');
const axios = require('axios');
const cors = require('cors');
const { spawn } = require('child_process');
const bodyParser = require('body-parser');

const http = require('http');
const fs = require('fs');

const app = express();
const server = http.createServer(app);

const FENICS_API = "http://18.159.213.75:8500";
const PORT = 3000;

app.use(cors({
  origin: '*', // Allow all origins
  methods: ['GET', 'POST'], // Allow specific methods
  allowedHeaders: ['Content-Type'] // Allow specific headers
}));

app.use(bodyParser.json());

app.post('/store-number', (req, res) => {
  const { number } = req.body;
  fs.writeFile('number.txt', number.toString(), (err) => {
    if (err) {
      return res.status(500).send('Failed to store number');
    }
    res.send('Number stored successfully');
  });
});

app.get('/get-number', (req, res) => {
  console.log('Detected query', req.query);
  const filename = req.query.filename;

  if (!filename) {
    return res.status(400).send('Filename is required');
  }

  fs.readFile(filename, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).send('Failed to read number');
    }
    res.json({ number: data });
  });
});


app.post('/increase-number', (req, res) => {
  
  console.log('Received POST request at /increase-number');
  const { delta, filename } = req.body;
  console.log('Increase by:', delta);

  fs.readFile(filename, 'utf8', (err, data) => {
    if (err) {
      console.error('Failed to read number', err);
      return res.status(500).send('Failed to read number');
    }
    const number = parseInt(data, 10) + delta;
    fs.writeFile(filename, number.toString(), (err) => {
      if (err) {
        console.error('Failed to store number', err);
        return res.status(500).send('Failed to store number');
      }
      res.json({ number });
    });
  });
});

app.post('/decrease-number', (req, res) => {
  
  console.log('Received POST request at /decrease-number');
  const { delta, filename } = req.body;
  console.log('Decrease by:', delta);

  fs.readFile(filename, 'utf8', (err, data) => {
    if (err) {
      console.error('Failed to read number', err);
      return res.status(500).send('Failed to read number');
    }
    const number = parseInt(data, 10) - delta;
    fs.writeFile(filename, number.toString(), (err) => {
      if (err) {
        console.error('Failed to store number', err);
        return res.status(500).send('Failed to store number');
      }
      res.json({ number });
    });
  });
});

app.get('/price-european-option', (req, res) => {
        const currency = req.query.currency;
    	const ctrCcy = req.query.ctrCcy;
    	const strategy = req.query.strategy;
    	const maturity = req.query.maturity;
    	const strike = req.query.strike;

	const pythonProcess = spawn('python3', ['xmlposter.py', 
		'--currency', currency,
		'--ctrCcy', ctrCcy,
		'--strategy', strategy,
		'--maturity', maturity,
		'--strike', strike]);

	let data = '';
    	let errorData = '';

    	pythonProcess.stdout.on('data', (chunk) => {
        	data += chunk.toString();
    	});

    	pythonProcess.stderr.on('data', (chunk) => {
        	errorData += chunk.toString();
    	});

   	pythonProcess.on('close', (code) => {
        	if (code !== 0) {
            		console.error(`Python script exited with code ${code}`);
            		console.error(errorData);
            		res.status(500).send('<error>An error occurred while executing the Python script</error>');
        	} else {
            		res.header('Content-Type', 'application/xml');
            		res.send(data);       
		}
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
})
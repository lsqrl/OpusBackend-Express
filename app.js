const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());

app.get('/', (req, res) => {
    let now = Date.now().toString(); // Convert the current date to a string
    res.send(now); // Send '42' as a response to the client
});

app.listen(5000, '0.0.0.0', () => {
    console.log('Server is running on http://localhost:5000');
});

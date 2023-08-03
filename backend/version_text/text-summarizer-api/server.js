const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
const port = 6000;

app.use(bodyParser.json());

app.post('/summarize', async (req, res) => {
  try {
    const { text, num_sentences } = req.body;

    const response = await axios.post('http://localhost:5000/summarize', {
      text,
      num_sentences,
    });

    res.json({ summary: response.data.summary });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'An error occurred.' });
  }
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});

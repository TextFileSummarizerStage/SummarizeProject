const express = require('express');
const bodyParser = require('body-parser');
const shell = require('shelljs');

const app = express();
const port = 8000; // Choisissez le port que vous souhaitez utiliser pour l'API

app.use(bodyParser.json());

const run_cap = (filePath) => {
  return new Promise((resolve, reject) => {
    shell.exec(`python file_summarizer.py ${filePath}`, (code, stdout, stderr) => {
      if (code !== 0) {
        reject(new Error('Failed to execute the Python script.'));
      } else {
        resolve(stdout);
      }
    });
  });
};

app.post('/summarize', async (req, res) => {
  const filePath = req.body.filePath;

  if (!filePath) {
    return res.status(400).json({ error: 'File path is required.' });
  }

  try {
    const summary = await run_cap(filePath);
    return res.json({ summary });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
const port = 6000;

const {spawn} = require('child_process');

app.use(bodyParser.json());

app.post('/summarize', async (req, res) => {
    try {
        const pythonProcess = spawn('python', ['path/to/your/python_script.py']);

        const dataToSend = JSON.stringify({text, num_sentences});
        pythonProcess.stdin.write(dataToSend);
        pythonProcess.stdin.end();

        let pythonResponse = '';
        pythonProcess.stdout.on('data', (data) => {
            pythonResponse += data;
        });

        let pythonError = '';
        pythonProcess.stderr.on('data', (data) => {
            pythonError += data;
        });

        pythonProcess.on('close', (code) => { // ... handle the Python script's response and errors
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({error: 'An error occurred.', error});
    }
});

// app.post('/summarize', async (req, res) => {
// try {
//     const { text, num_sentences } = req.body;
//     const response = await axios.post('http://localhost:5000/summarize', {
//       text,
//       num_sentences,
//     });

//     res.json({ summary: response.data.summary });
// } catch (error) {
//     console.error(error);
//     res.status(500).json({ error: 'An error occurred.', error });
// }
// });

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});

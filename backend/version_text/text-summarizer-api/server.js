const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
const port = 6000;

const {spawn} = require('child_process');

app.use(bodyParser.json());

app.post('/summarize', async (req, res) => {
    try { // Spawn a child process to run the Python script
        const pythonProcess = spawn('python', ['../text_summarizer.py']);

        // Send the data to the Python script through stdin
        const dataToSend = JSON.stringify("saaaample text");
        // const dataToSend = JSON.stringify({text, num_sentences});
        pythonProcess.stdin.write(dataToSend);
        pythonProcess.stdin.end();

        // Listen for data from the Python script's stdout
        let pythonResponse = '';
        pythonProcess.stdout.on('data', (data) => {
            pythonResponse += data;
        });

        // Listen for errors from the Python script's stderr
        let pythonError = '';
        pythonProcess.stderr.on('data', (data) => {
            pythonError += data;
        });

        // Handle the Python script's exit event
        pythonProcess.on('close', (code) => {
            if (code === 0) {
                try {
                    const parsedResponse = JSON.parse(pythonResponse);
                    res.json({summary: parsedResponse.summary});
                } catch (error) {
                    console.error('Error parsing Python response:', error);
                    res.status(500).json({error: 'An error occurred while processing the Python response.'});
                }
            } else {
                console.error('Python process exited with code:', code);
                console.error('Python error:', pythonError);
                res.status(500).json({error: 'An error occurred while running the Python script.'});
            }
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

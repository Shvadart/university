const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs').promises;
const cors = require('cors');

const app = express();
const port = 3000;

app.use(cors());

app.use(bodyParser.json());

// Serve static files from the 'public' directory
app.use(express.static('public'));

app.post('/saveComments', async (req, res) => {
  const { comments } = req.body;

  try {
    const commentsString = JSON.stringify(comments, null, 2);
    await fs.writeFile('public/comments.json', commentsString);
    res.status(200).send('Comments saved successfully.');
  } catch (error) {
    console.error('Error saving comments:', error);
    res.status(500).send('Error saving comments.');
  }
});

app.get('/loadComments', async (req, res) => {
  try {
    const data = await fs.readFile('public/comments.json', 'utf-8');
    const comments = JSON.parse(data);
    res.json(comments);
  } catch (error) {
    console.error('Error loading comments:', error);
    res.status(500).send('Error loading comments.');
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

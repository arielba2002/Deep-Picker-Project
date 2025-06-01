import express from 'express';
import path from 'path';
import cors from 'cors';

const app = express();
const port = process.env.PORT || 8080;

// Enable CORS for all routes
app.use(cors());

// Serve static files from the React app
app.use(express.static(path.join(process.cwd(), 'dist')));

// Handle API requests
app.use('/api', express.raw(), async (req, res) => {
  try {
    // Manually construct the target URL to avoid path-to-regexp issues
    const targetUrl = `http://backend.deep.svc.cluster.local:8888${req.url}`;
    
    // Remove any query parameters from the URL
    const url = new URL(targetUrl);
    url.search = ''; // Clear query parameters
    
    const response = await fetch(url.toString(), {
      method: req.method,
      headers: req.headers,
      body: req.body
    });

    const data = await response.text();
    res.status(response.status).send(data);
  } catch (error) {
    console.error('Error proxying to backend:', error);
    res.status(500).send('Error proxying to backend');
  }
});

// Handle all other routes by returning the index.html file
app.get('*', (req, res) => {
  res.sendFile(path.join(process.cwd(), 'dist', 'index.html'));
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

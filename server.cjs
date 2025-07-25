const express = require('express');
const cors = require('cors');
const ytdl = require('ytdl-core');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Create downloads directory
const downloadsDir = path.join(__dirname, 'downloads');
if (!fs.existsSync(downloadsDir)) {
  fs.mkdirSync(downloadsDir);
}

// Route to get video info
app.post('/video-info', async (req, res) => {
  try {
    const { url } = req.body;
    
    if (!url) {
      return res.status(400).json({ error: 'URL is required' });
    }

    // Validate YouTube URL
    if (!ytdl.validateURL(url)) {
      return res.status(400).json({ error: 'Invalid YouTube URL' });
    }

    // Get video info
    const info = await ytdl.getInfo(url);
    const videoDetails = info.videoDetails;

    const videoInfo = {
      id: videoDetails.videoId,
      title: videoDetails.title,
      thumbnail: videoDetails.thumbnails[videoDetails.thumbnails.length - 1].url,
      duration: formatDuration(videoDetails.lengthSeconds),
      author: videoDetails.author.name,
      views: parseInt(videoDetails.viewCount).toLocaleString(),
      uploadDate: videoDetails.publishDate,
      description: videoDetails.description?.substring(0, 200) + '...' || 'No description',
      url: url
    };

    res.json(videoInfo);
  } catch (error) {
    console.error('Error fetching video info:', error);
    res.status(500).json({ error: 'Failed to fetch video information' });
  }
});

// Route to download video
app.post('/download', async (req, res) => {
  try {
    const { url, format, quality } = req.body;
    
    if (!url) {
      return res.status(400).json({ error: 'URL is required' });
    }

    // Validate YouTube URL
    if (!ytdl.validateURL(url)) {
      return res.status(400).json({ error: 'Invalid YouTube URL' });
    }

    // Get video info for filename
    const info = await ytdl.getInfo(url);
    const title = info.videoDetails.title.replace(/[^\w\s-]/gi, '').trim();
    const sanitizedTitle = title.substring(0, 50);

    let options = {};
    let filename = '';

    if (format === 'mp3') {
      // Audio only
      options = {
        filter: 'audioonly',
        quality: 'highestaudio'
      };
      filename = `${sanitizedTitle}.mp3`;
    } else {
      // Video with audio
      const qualityMap = {
        '360p': '18',
        '720p': '22',
        '1080p': '137+140'
      };
      
      options = {
        quality: qualityMap[quality] || 'highest',
        filter: 'videoandaudio'
      };
      filename = `${sanitizedTitle}.${format}`;
    }

    // Set response headers
    res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
    res.setHeader('Content-Type', format === 'mp3' ? 'audio/mpeg' : 'video/mp4');

    // Stream the video/audio directly to response
    const stream = ytdl(url, options);
    
    stream.on('error', (error) => {
      console.error('Stream error:', error);
      if (!res.headersSent) {
        res.status(500).json({ error: 'Failed to download video' });
      }
    });

    stream.pipe(res);

  } catch (error) {
    console.error('Download error:', error);
    if (!res.headersSent) {
      res.status(500).json({ error: 'Failed to download video' });
    }
  }
});

// Helper function to format duration
function formatDuration(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = seconds % 60;
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  } else {
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  }
}

// Start server
app.listen(PORT, () => {
  console.log(`YouTube Downloader backend running on port ${PORT}`);
});
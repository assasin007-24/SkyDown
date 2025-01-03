// api/download.js

const ytdl = require('ytdl-core');

module.exports = async (req, res) => {
    const { URL } = req.query;

    if (!URL) {
        return res.status(400).json({ error: 'URL parameter is required' });
    }

    try {
        // Send the URL as a response, or you can handle downloading with ytdl here.
        res.json({ url: URL });
    } catch (error) {
        res.status(500).json({ error: 'An error occurred' });
    }
};

const { Router } = require('express');
const { appendLine, readLogs } = require('../services/logService');

const router = Router();

router.post('/', (req, res) => {
    const body = (req.body || '').toString();

    if (!body) {
        return res.status(400).send('No log line provided');
    }

    appendLine(body);
    res.status(204).end();
});

router.get('/', (req, res) => {
    try {
        const data = readLogs();
        res.set('Content-Type', 'text/plain').send(data);
    } catch (error) {
        res.status(500).send('error');
    }
});

module.exports = router;

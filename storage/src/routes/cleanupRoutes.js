const { Router } = require('express');
const { clearLogs } = require('../services/logService');

const router = Router();

router.post('/', (_req, res) => {
    clearLogs();
    res.status(200).send('Cleaned up');
});

module.exports = router;

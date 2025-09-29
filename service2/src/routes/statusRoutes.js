const { Router } = require('express');
const { buildStatusRecord } = require('../services/metricsService');
const { appendToVstorage } = require('../services/vstorageService');
const { postToStorage } = require('../services/storageClient');

const router = Router();

router.get('/', async (_req, res, next) => {
    try {
        const record = await buildStatusRecord();

        await postToStorage(record);

        try {
            await appendToVstorage(record);
        } catch (error) {
            console.warn('Failed to append to VSTORAGE_PATH', error);
        }

        res.type('text/plain').send(record);
    } catch (error) {
        next(error);
    }
});

module.exports = router;

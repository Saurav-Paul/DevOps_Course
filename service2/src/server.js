const express = require('express');
const statusRoutes = require('./routes/statusRoutes');
const healthRoutes = require('./routes/healthRoutes');

const app = express();

app.use('/status', statusRoutes);
app.use('/health', healthRoutes);

const PORT = process.env.PORT || 8081;
app.listen(PORT, () => {
    console.log(`Service2 listening on port :${PORT}`);
});

const express = require('express');
const logRoutes = require('./routes/logRoutes');
const healthRoutes = require('./routes/healthRoutes');
const cleanupRoutes = require('./routes/cleanupRoutes');

const app = express();
app.use(express.text({ type: '*/*' }));

app.use('/log', logRoutes);
app.use('/health', healthRoutes);
app.use('/cleanup', cleanupRoutes);

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log(`Storage server listening on port :${PORT}`);
});

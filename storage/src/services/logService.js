const fs = require('fs');
const path = require('path');

const LOG_PATH = process.env.LOG_PATH || '/var/storage/log.txt';

function ensureLogDirectory() {
    fs.mkdirSync(path.dirname(LOG_PATH), { recursive: true });
}

function appendLine(line) {
    ensureLogDirectory();

    if (!line.endsWith('\n')) {
        line += '\n';
    }

    fs.appendFileSync(LOG_PATH, line, { encoding: 'utf8' });
}

function readLogs() {
    try {
        return fs.readFileSync(LOG_PATH, { encoding: 'utf8' });
    } catch (error) {
        if (error.code === 'ENOENT') {
            return '';
        }

        throw error;
    }
}

function clearLogs() {
    ensureLogDirectory();
    fs.writeFileSync(LOG_PATH, '', { encoding: 'utf8' });
}

module.exports = {
    appendLine,
    readLogs,
    clearLogs,
};

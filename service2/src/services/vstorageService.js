const fs = require('fs');
const path = require('path');

const DEFAULT_VSTORAGE_PATH = '/data/vstorage';
const DEFAULT_FILENAME = 'vstorage.log';

function resolveTargetPath() {
    const rawPath = process.env.VSTORAGE_PATH || DEFAULT_VSTORAGE_PATH;

    if (rawPath.endsWith(path.sep)) {
        return path.join(rawPath, DEFAULT_FILENAME);
    }

    try {
        const stats = fs.statSync(rawPath);
        if (stats.isDirectory()) {
            return path.join(rawPath, DEFAULT_FILENAME);
        }
    } catch (error) {
        if (error.code !== 'ENOENT') {
            throw error;
        }
    }

    return rawPath;
}

async function appendToVstorage(line) {
    const targetPath = resolveTargetPath();
    const normalizedLine = line.endsWith('\n') ? line : `${line}\n`;

    await fs.promises.mkdir(path.dirname(targetPath), { recursive: true });

    const handle = await fs.promises.open(targetPath, 'a');
    try {
        await handle.write(normalizedLine);
        await handle.sync();
    } finally {
        await handle.close();
    }
}

module.exports = {
    appendToVstorage,
};

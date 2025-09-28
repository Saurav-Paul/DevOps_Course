const fs = require('fs');
const path = require('path');

const DEFAULT_VSTORAGE_PATH = '/data/vstorage';

async function appendToVstorage(line) {
    const filePath = process.env.VSTORAGE_PATH || DEFAULT_VSTORAGE_PATH;
    const normalizedLine = line.endsWith('\n') ? line : `${line}\n`;

    await fs.promises.mkdir(path.dirname(filePath), { recursive: true });

    const handle = await fs.promises.open(filePath, 'a');
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

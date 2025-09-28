const fs = require('fs');

async function readUptimeHours() {
    const data = await fs.promises.readFile('/proc/uptime', 'utf8');
    const [secondsStr] = data.trim().split(/\s+/);
    const seconds = parseFloat(secondsStr);

    if (Number.isNaN(seconds)) {
        throw new Error('Unable to parse uptime from /proc/uptime');
    }

    return seconds / 3600;
}

function readFreeDiskMiB() {
    const stats = fs.statfsSync('/');
    const freeBytes = BigInt(stats.bavail) * BigInt(stats.bsize);
    const mib = Number(freeBytes / BigInt(1024 * 1024));
    return mib;
}

function formatTimestamp() {
    return new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
}

async function buildStatusRecord() {
    const [uptimeHours, freeDiskMiB] = await Promise.all([
        readUptimeHours(),
        Promise.resolve(readFreeDiskMiB()),
    ]);

    const timestamp = formatTimestamp();
    const uptimeFormatted = uptimeHours.toFixed(2);

    return `${timestamp}: uptime ${uptimeFormatted} hours, free disk in root: ${freeDiskMiB} MBytes`;
}

module.exports = {
    buildStatusRecord,
};

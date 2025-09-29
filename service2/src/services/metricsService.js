const fs = require('fs');

function readUptimeHours() {
    return process.uptime() / 3600;
}

function readFreeDiskMiB() {
    const stats = fs.statfsSync('/');
    const freeBytes = BigInt(stats.bavail) * BigInt(stats.bsize);
    return Number(freeBytes / BigInt(1024 * 1024));
}

function formatTimestamp() {
    const iso = new Date().toISOString();
    return iso.replace(/\.\d{3}Z$/, 'Z');
}

async function buildStatusRecord() {
    const [uptimeHours, freeDiskMiB] = await Promise.all([
        Promise.resolve(readUptimeHours()),
        Promise.resolve(readFreeDiskMiB()),
    ]);

    const timestamp = formatTimestamp();
    const uptimeFormatted = uptimeHours.toFixed(2);

    return `${timestamp}: uptime ${uptimeFormatted} hours, free disk in root: ${freeDiskMiB} MBytes`;
}

module.exports = {
    buildStatusRecord,
};

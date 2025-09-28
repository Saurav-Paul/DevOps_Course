const DEFAULT_STORAGE_URL = 'http://storage:8080';
const fetchFn = typeof globalThis.fetch === 'function' ? globalThis.fetch.bind(globalThis) : null;

async function postToStorage(message) {
    if (!fetchFn) {
        return;
    }

    const baseUrl = process.env.STORAGE_URL || DEFAULT_STORAGE_URL;
    const target = `${baseUrl.replace(/\/$/, '')}/log`;

    try {
        await fetchFn(target, {
            method: 'POST',
            headers: { 'Content-Type': 'text/plain' },
            body: message,
        });
    } catch (error) {
        console.warn('Failed to POST log to storage service', error);
    }
}

module.exports = {
    postToStorage,
};

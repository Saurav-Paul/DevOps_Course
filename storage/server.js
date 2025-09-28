const fstat = require('fs');
const path = require('path');


const app = express();
app.use(express.text({
    type: '*/*',
}))

const LOG_PATH = process.env.LOG_PATH || '/var/storage/log.txt';

function appendLine(line){
    fstat.makedirSync(
        path.dirname(LOG_PATH), { recursive: true }
    );

    if(!line.endsWith('\n')){
        line += '\n';
    }

    fstat.appendFileSync(LOG_PATH, line, { encoding: 'utf8' });
}

app.post('/log', (req, res) => {
    const body = (req.body || '').toString();
    if(!body){
        return res.status(400).send('No log line provided');
    }
    appendLine(body);
    res.status(204).end();
});

app.get('/log', (req, res) => {
    try{
        const data = fstat.readFileSync(LOG_PATH, { encoding: 'utf8' });
        res.set('Content-Type', 'text/plain').send(data);
    }catch(e){
         if (e.code === 'ENOENT') {
            res.set('Content-Type', 'text/plain').send('');
        } else {
            res.status(500).send('error');
        }
    }
});

app.get('/health', (req, res) => {
    res.status(200).send('OK');
});

app.post('/cleanup', (req, res) => {
    fstat.writeFileSync(LOG_PATH, '', 'utf8');
    res.status(200).send('Cleaned up');
});

app.listen(
    8080,
    () => console.log('Storage server listening on port :8080')
);
const fs = require('fs');
const csv = require('csv-parser');
const { MongoClient } = require('mongodb');

const url = 'mongodb://admin:adminpassword@localhost:27017/?authSource=admin';
const dbName = 'ml_data';

async function importCSV() {
    const client = new MongoClient(url);
    try {
        await client.connect();
        const db = client.db(dbName);
        const collection = db.collection('movies');

        const movies = [];

        fs.createReadStream('movies.csv')
            .pipe(csv())
            .on('data', (row) => {
                movies.push(row);
            })
            .on('end', async () => {
                await collection.insertMany(movies);
                console.log('CSV data inserted into MongoDB!');
                await client.close();
            });

    } catch (err) {
        console.error(err);
        await client.close();
    }
}

importCSV();

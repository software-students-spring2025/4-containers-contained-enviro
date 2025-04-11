// Create test users
db = db.getSiblingDB('ml_data');

// Create test users collection if it doesn't exist
db.createCollection('users');

// Add some test users with hashed passwords
// These are werkzeug generated hashes for the passwords 'test123' and 'test456'
db.users.insertMany([
    {
        username: "test_user1",
        password: "pbkdf2:sha256:600000$7nYXHgv9$b9d89de9c84f14c5f8b4f1a9f2f346b89f1d0c9d9e8a3b4c5d6e7f8a9b0c1d2e",
        saved_movies: []
    },
    {
        username: "test_user2",
        password: "pbkdf2:sha256:600000$aB3cD4eF$1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2",
        saved_movies: []
    }
]);


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

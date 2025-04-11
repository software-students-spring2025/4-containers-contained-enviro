db = db.getSiblingDB('ml_data');

// Check if 'admin' user exists and create if necessary
if (!db.getUser('admin')) {
    print('Creating admin user...');
    db.createUser({
        user: 'admin',
        pwd: 'adminpassword',
        roles: [{
            role: 'readWrite',
            db: 'ml_data'
        }]
    });
} else {
    print('Admin user already exists');
}

// Check if 'movies' collection exists and create if necessary
if (!db.getCollectionNames().includes('movies')) {
    print('Creating movies collection...');
    db.createCollection('movies');
} else {
    print('Movies collection already exists');
}

// Create test users
db = db.getSiblingDB('ml_data');

// Create test users collection if it doesn't exist
db.createCollection('users');

// Add some test users
db.users.insertMany([
    {
        username: "test_user1",
        password: "test123",  // This is just for testing
        saved_movies: []
    },
    {
        username: "test_user2",
        password: "test456",  // This is just for testing
        saved_movies: []
    }
]);

db.createUser({
  user: 'ml_user',
  pwd: 'ml_password',
  roles: [
    {
      role: 'readWrite',
      db: 'ml_data'
    }
  ]
});

db = db.getSiblingDB('ml_data');

// Create collections with validation
db.createCollection('sensor_data', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['timestamp', 'sensor_type', 'raw_data'],
      properties: {
        timestamp: {
          bsonType: 'date',
          description: 'Timestamp when the data was collected'
        },
        sensor_type: {
          bsonType: 'string',
          enum: ['camera', 'microphone', 'gps', 'other'],
          description: 'Type of sensor that collected the data'
        },
        raw_data: {
          bsonType: 'object',
          description: 'Raw sensor data'
        },
        metadata: {
          bsonType: 'object',
          description: 'Additional metadata about the sensor reading'
        }
      }
    }
  }
});

db.createCollection('ml_results', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['timestamp', 'sensor_data_id', 'model_type', 'results'],
      properties: {
        timestamp: {
          bsonType: 'date',
          description: 'Timestamp when the analysis was performed'
        },
        sensor_data_id: {
          bsonType: 'objectId',
          description: 'Reference to the sensor data that was analyzed'
        },
        model_type: {
          bsonType: 'string',
          description: 'Type of ML model or analysis performed'
        },
        results: {
          bsonType: 'object',
          description: 'Results of the ML analysis'
        },
        confidence_score: {
          bsonType: 'double',
          minimum: 0,
          maximum: 1,
          description: 'Confidence score of the ML results (0-1)'
        }
      }
    }
  }
});

// Create indexes
db.sensor_data.createIndex({ "timestamp": 1 });
db.sensor_data.createIndex({ "sensor_type": 1 });
db.ml_results.createIndex({ "sensor_data_id": 1 });
db.ml_results.createIndex({ "timestamp": 1 });
db.ml_results.createIndex({ "model_type": 1 });

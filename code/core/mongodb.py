from pymongo import MongoClient
from django.conf import settings
from datetime import datetime

class MongoDBClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._instance.client = MongoClient(settings.MONGO_URI)
            cls._instance.db = cls._instance.client[settings.MONGO_DB_NAME]
        return cls._instance

    def log_activity(self, user_id, action, details):
        collection = self.db['activity_logs']
        log_entry = {
            'user_id': user_id,
            'action': action,
            'details': details,
            'timestamp': datetime.utcnow()
        }
        return collection.insert_one(log_entry)

    def log_analytics(self, user_id, course_id, event_type, data):
        collection = self.db['learning_analytics']
        analytics_entry = {
            'user_id': user_id,
            'course_id': course_id,
            'event_type': event_type,
            'data': data,
            'timestamp': datetime.utcnow()
        }
        return collection.insert_one(analytics_entry)

    def get_activity_report(self, user_id=None):
        collection = self.db['activity_logs']
        query = {'user_id': user_id} if user_id else {}
        return list(collection.find(query).sort('timestamp', -1).limit(100))

    def get_learning_stats(self, course_id):
        collection = self.db['learning_analytics']
        pipeline = [
            {'$match': {'course_id': course_id}},
            {'$group': {'_id': '$event_type', 'count': {'$sum': 1}}}
        ]
        return list(collection.aggregate(pipeline))

mongo_client = MongoDBClient()

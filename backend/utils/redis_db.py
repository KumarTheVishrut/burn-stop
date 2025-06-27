import redis
import json
import os
from typing import Optional, Any

class RedisDB:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            decode_responses=True
        )
    
    def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """Set a key-value pair in Redis"""
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            return self.redis_client.set(key, value, ex=ex)
        except Exception as e:
            print(f"Error setting key {key}: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from Redis"""
        try:
            value = self.redis_client.get(key)
            if value is None:
                return None
            
            # Try to parse as JSON, if it fails return as string
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        except Exception as e:
            print(f"Error getting key {key}: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """Delete a key from Redis"""
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            print(f"Error deleting key {key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if a key exists in Redis"""
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            print(f"Error checking existence of key {key}: {e}")
            return False
    
    def zadd(self, key: str, mapping: dict) -> int:
        """Add elements to a sorted set"""
        try:
            return self.redis_client.zadd(key, mapping)
        except Exception as e:
            print(f"Error adding to sorted set {key}: {e}")
            return 0
    
    def zrange(self, key: str, start: int = 0, end: int = -1, withscores: bool = False):
        """Get elements from a sorted set"""
        try:
            return self.redis_client.zrange(key, start, end, withscores=withscores)
        except Exception as e:
            print(f"Error getting from sorted set {key}: {e}")
            return []
    
    def zrem(self, key: str, *values) -> int:
        """Remove elements from a sorted set"""
        try:
            return self.redis_client.zrem(key, *values)
        except Exception as e:
            print(f"Error removing from sorted set {key}: {e}")
            return 0
    
    def zrangebyscore(self, key: str, min_score: float, max_score: float, withscores: bool = False):
        """Get elements from a sorted set by score range"""
        try:
            return self.redis_client.zrangebyscore(key, min_score, max_score, withscores=withscores)
        except Exception as e:
            print(f"Error getting from sorted set by score {key}: {e}")
            return []
    
    def keys(self, pattern: str = "*"):
        """Get all keys matching a pattern"""
        try:
            return self.redis_client.keys(pattern)
        except Exception as e:
            print(f"Error getting keys with pattern {pattern}: {e}")
            return []

# Global Redis instance
redis_db = RedisDB()

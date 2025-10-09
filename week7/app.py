import boto3
import redis
import json

# Initialize DB
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-west-2'
)
table = dynamodb.table('Assignment7_LazyLoading')

# Initialize Redis
redis_client = redis.Redis(
    host = 'localhost',
    port = '6379',
    db = 0,
    decode_response=True
)

def put_user(UserID, flavor):
    user_data = {
        'UserID': user_id,
        'flavor': flavor
    }
    table.put_item(Item=user_data)
    print(f"{user_id} Stored in Database")
    return user_data

def get_user_with_cache(UserID):
    cache_key = f"user: {user_id}"
    cached_value = redis_client.get(cache_key)

    if cached_value:
        print(f"Cache found for {user_id}")
        return json.loads(cached_value)
    print(f"No cache hit for user {user_id}")

    response = table.get_item(Key={'UserID': user_id})

    if 'Item' not in response:
        print(f"User {user_id} not found in Database")
        return None

    user_data = response['Item']
    print(f"User {user_id} found in Database")

    redis_client.set(
        cache_key,
        json.dumps(user_data),
        ex=3600
    )
    print(f"User {user_id} Cached in Redis")
    return user_data

def get_user(user_id: str):
    return get_user_with_cache(user_id)

if __name__ == "__main__":
    put_user("user123", "chocolate")

    user = get_user("user123")
    print(f"\nUser {user} found in database!")
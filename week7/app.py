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
        'UserID': UserID,
        'flavor': flavor
    }
    table.put_item(Item=user_data)
    print(f"{UserID} Stored in Database")
    return user_data

def get_user_with_cache(UserID):
    cache_key = f"user: {UserID}"
    cached_value = redis_client.get(cache_key)

    if cached_value:
        print(f"Cache found for {UserID}")
        return json.loads(cached_value)
    print(f"No cache hit for user {UserID}")

    response = table.get_item(Key={'UserID': UserID})

    if 'Item' not in response:
        print(f"User {UserID} not found in Database")
        return None

    user_data = response['Item']
    print(f"User {UserID} found in Database")

    redis_client.set(
        cache_key,
        json.dumps(user_data),
        ex=3600
    )
    print(f"User {UserID} Cached in Redis")
    return user_data

def get_user(UserID: str):
    return get_user_with_cache(UserID)

if __name__ == "__main__":
    put_user("user123", "chocolate")

    user = get_user("user123")
    print(f"\nUser {user} found in database!")
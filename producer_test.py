from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

test_message = {
    "title": "Test message après correction config Kafka",
    "created_utc": 1234567890
}

future = producer.send("reddit_posts", test_message)
result = future.get(timeout=10)  # attend la confirmation d'envoi
print("✅ Message envoyé, résultat:", result)

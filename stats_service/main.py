from concurrent import futures
import grpc
from stats_service_pb2 import GetStatsResponse
from stats_service_pb2_grpc import StatsServiceServicer, add_StatsServiceServicer_to_server
from clickhouse_driver import Client
from kafka import KafkaConsumer
import json
import threading

likes_dict = {}
comment_dict = {}

class StatisticsService(StatsServiceServicer):
    def __init__(self):
        self.clickhouse = Client(
        host='localhost',
        port=9000,
        secure=False,
        database='statistics',
        connect_timeout=10
    )
        
    def GetStats(self, request, context):
        try:
            
            """likes = self.clickhouse.execute(
                "SELECT count() FROM likes WHERE source_id = %(post_id)s",
                {'post_id': request.post_id}
            )[0][0]
            
            comments = self.clickhouse.execute(
                "SELECT count() FROM comments WHERE source_id = %(post_id)s",
                {'post_id': request.post_id}
            )[0][0]"""
            
            if int(request.post_id) in likes_dict:
                likes = likes_dict[int(request.post_id)]
            else:
                likes = 0
                
            if int(request.post_id) in comment_dict:
                comments = comment_dict[int(request.post_id)]
            else:
                comments = 0
            
            return GetStatsResponse(
                likes=likes,
                comments=comments
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return GetStatsResponse(likes=0, comments=0)

def consume_kafka_messages():
    consumer = KafkaConsumer(
        'like', 'comment',
        bootstrap_servers=['localhost:29092'],
        group_id='statistics-group',
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    clickhouse = Client(
        host='localhost',
        port=9000,
        secure=False,
        database='statistics',
        connect_timeout=10
    )
    
    
    for message in consumer:
        print("New message", message.topic, message.value)
        print(likes_dict)
        try:
            if message.topic == 'comment':
                """clickhouse.execute(
                    "INSERT INTO comments (comment_id, author_id, source_id, timestamp) VALUES",
                    [(
                        message.value['comment_id'],
                        message.value['author_id'],
                        message.value['source_id'],
                        message.value['timestamp']
                    )]
                )"""
                if int(message.value['source_id']) not in comment_dict:
                    comment_dict[int(message.value['source_id'])] = 0
                comment_dict[int(message.value['source_id'])] += 1
            elif message.topic == 'like':
                """clickhouse.execute(
                    "INSERT INTO likes (author_id, source_id, timestamp) VALUES",
                    [(
                        message.value['author_id'],
                        message.value['source_id'],
                        message.value['timestamp']
                    )]
                )"""
                if int(message.value['source_id']) not in likes_dict:
                    likes_dict[int(message.value['source_id'])] = 0
                likes_dict[int(message.value['source_id'])] += 1
        except Exception as e:
            print(f"Error processing {message.topic}: {e}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_StatsServiceServicer_to_server(
        StatisticsService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("gRPC server started on port 50052")
    
    kafka_thread = threading.Thread(target=consume_kafka_messages)
    kafka_thread.daemon = True
    kafka_thread.start()
    
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
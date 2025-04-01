from concurrent import futures
import grpc
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
import asyncio

from content_service_pb2_grpc import PostServiceServicer
from content_service_pb2 import (
    PostResponse,
    StatusResponse,
    ListResponse
)
from database.models import Post
from database.dao import PostDAO

class PostService(PostServiceServicer):
        
    def _get_session(self):
        return self.session_maker()
            
    async def CreatePost(self, request, context):
        print("Create post todo")
        res = await PostDAO.add(name=request.title,
                           description=request.description,
                           user_id=request.creator_id,
                           is_private=request.private,
                           tags="")
        print(res)
        return PostResponse(
            id=res.id,
            title=request.title,
            description=request.description,
            creator_id=request.creator_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            tags=request.tags,
            private=request.private
        )
        
            
    def DeletePost(self, request, context):
        print("Detele post todo")

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    from content_service_pb2_grpc import add_PostServiceServicer_to_server
    add_PostServiceServicer_to_server(PostService(), server)
    
    
    server.add_insecure_port('localhost:50051')
    await server.start()
    print("gRPC сервер запущен на порту 50051")
    await server.wait_for_termination()
    
if __name__ == '__main__':
    asyncio.run(serve())
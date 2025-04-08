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
        print("Create post")
        res = await PostDAO.add(name=request.title,
                           description=request.description,
                           user_id=request.creator_id,
                           is_private=request.private,
                           tags="")
        return PostResponse(
            id=res.id,
            title=res.name,
            description=res.description,
            creator_id=res.user_id,
            created_at=res.created_at,
            updated_at=res.updated_at,
            tags=res.tags,
            private=res.is_private
        )
        
    async def GetPost(self, request, context):
        print("Get post")
        res = await PostDAO.find_by_id(request.post_id)
        if res is None:
            return PostResponse(
            id=-1,
            title="",
            description="",
            creator_id=-1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            tags=[""],
            private=False
        )
        return PostResponse(
            id=res.id,
            title=res.name,
            description=res.description,
            creator_id=res.user_id,
            created_at=res.created_at,
            updated_at=res.updated_at,
            tags=res.tags,
            private=res.is_private
        )

    async def DeletePost(self, request, context):
        print("Delete post todo")
        res = await PostDAO.delete(request.post_id, -1)
        if "error" in res:
            return StatusResponse(
                success = False,
                message = res["error"]
            )
        return StatusResponse(
            success = True,
            message = res["message"]
        )

async def main():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    from content_service_pb2_grpc import add_PostServiceServicer_to_server
    add_PostServiceServicer_to_server(PostService(), server)
    
    
    server.add_insecure_port('localhost:50051')
    await server.start()
    print("gRPC сервер запущен на порту 50051")
    await server.wait_for_termination()
    
if __name__ == '__main__':
    asyncio.run(main())
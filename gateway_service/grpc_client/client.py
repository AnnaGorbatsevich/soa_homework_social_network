# grpc/client.py
from concurrent import futures
import grpc
from .content_service_pb2_grpc import PostServiceStub
from .content_service_pb2 import (
    PostRequest,
    DeleteRequest,
    UpdateRequest,
    GetRequest,
    ListRequest
)

class PostClient:
    def __init__(self, host='localhost:50051'):
        self.channel = grpc.aio.insecure_channel(host)
        self.stub = PostServiceStub(self.channel)
    
    async def create_post(self, title: str, description: str, creator_id: int, 
                   tags: list[str], private: bool = False):
        print("CREATOR ID", creator_id)
        request = PostRequest(
            title=title,
            description=description,
            creator_id=int(creator_id),
            tags=tags,
            private=private
        )
        return await self.stub.CreatePost(request)
    
    async def delete_post(self, post_id: int):
        request = DeleteRequest(post_id=post_id)
        return await self.stub.DeletePost(request)
    
    async def update_post(self, post_id: int, title: str = None, 
                   description: str = None, tags: list[str] = None,
                   private: bool = None):
        request = UpdateRequest(
            post_id=post_id,
            title=title,
            description=description,
            tags=tags,
            private=private
        )
        return await self.stub.UpdatePost(request)
    
    async def get_post(self, post_id: int, viewer_id: int = None):
        request = GetRequest(
            post_id=post_id,
            viewer_id=viewer_id
        )
        return await self.stub.GetPost(request)

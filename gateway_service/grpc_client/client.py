# grpc/client.py
from concurrent import futures
import grpc
from .content_service_pb2_grpc import PostServiceStub
from .content_service_pb2 import (
    PostRequest,
    DeleteRequest,
    UpdateRequest,
    GetRequest,
    ListRequest,
    LikeRequest,
    CommentRequest,
    GetCommentRequest
)


from .stats_service_pb2_grpc import StatsServiceStub
from .stats_service_pb2 import (
    GetStatsRequest,
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
    
    async def add_comment(self, source_type, description, source_id, user_id):
        request = CommentRequest(
            source_type=source_type,
            description=description,
            source_id = source_id,
            user_id = user_id
        )
        return await self.stub.AddComment(request)
    
    async def add_comment_like(self, comment_id: int, user_id: int = None):
        request = LikeRequest(
            source_id=comment_id,
            user_id=user_id,
            source_type="comment"
        )
        return await self.stub.AddCommentLike(request)
    
    async def add_post_like(self, post_id: int, user_id: int = None):
        request = LikeRequest(
            source_id=post_id,
            user_id=user_id,
            source_type="post"
        )
        return await self.stub.AddPostLike(request)
    
    async def get_comment(self, comment_id: int, user_id: int):
        request = GetCommentRequest(
            comment_id=comment_id,
            user_id=user_id
        )
        print("Client get comment")
        return await self.stub.GetComment(request)


class StatsClient:
    def __init__(self, host='localhost:50052'):
        self.channel = grpc.aio.insecure_channel(host)
        self.stub = StatsServiceStub(self.channel)
    
    async def get_stats(self, post_id: int):
        request = GetStatsRequest(
            post_id = post_id,
        )
        return await self.stub.GetStats(request)
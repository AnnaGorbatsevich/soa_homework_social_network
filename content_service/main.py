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
    ListResponse,
    LikeResponse,
    CommentResponse
)
from database.models import Post
from database.dao import PostDAO, CommentDAO, LikeDAO

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
        if res.user_id != request.viewer_id and res.is_private:
            return PostResponse(
                id=-2,
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
    
    async def AddComment(self, request, context):
        print("Add Comment")
        res = await CommentDAO.add(source_type = request.source_type,
                                    description = request.description,
                                    source_id = request.source_id,
                                    user_id = request.user_id)
        return CommentResponse(
            id = res.id,
            user_id = res.user_id,
            source_id = res.source_id,
            source_type = res.source_type,
            description = res.description
        )
    
    async def AddCommentLike(self, request, context):
        print("Add Comment Like")
        res = await LikeDAO.add(source_type = "comment",
                                    source_id = request.source_id,
                                    user_id = request.user_id)
        return LikeResponse(
            success = True,
            message = "OK",
        )
    
    async def AddPostLike(self, request, context):
        print("Add Post Like")
        res = await LikeDAO.add(source_type = "post",
                                    source_id = request.source_id,
                                    user_id = request.user_id)
        return LikeResponse(
            success = True,
            message = "OK",
        )
    
    async def GetComment(self, request, context):
        print("Get Comment")
        res = await CommentDAO.find_by_id(request.comment_id)
        if res is None:
            return CommentResponse(
                id=-1,
                user_id=-1,
                source_id=-1,
                source_type="",
                description="",
            )
        return CommentResponse(
            id=res.id,
            user_id=res.user_id,
            source_id=-res.source_id,
            source_type=res.source_type,
            description=res.description,
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
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCommentOwner(BasePermission):
    """해당 댓글을 작성한 사람만이 게시물을 수정/삭제할 수 있는 권한을 부여"""
    message = "You can only modify your own comments"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
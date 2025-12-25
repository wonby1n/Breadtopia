from rest_framework import serializers
from .models import Post, PostComment

class PostCommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = ('id', 'post', 'user', 'user_nickname', 'content', 'created_at', 'parent', 'replies')
        read_only_fields = ('user', 'post', 'parent')

    def get_replies(self, obj):
        if obj.replies.exists():
            return PostCommentSerializer(obj.replies.all(), many=True).data
        return []

class PostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)
    comments_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    store_name = serializers.CharField(source='store.name', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'author_nickname',
            'title',
            'content',
            'category',
            'image',  # 🚨 [수정] photo_url -> image
            'store',  # ✅ [추가] 빵집 연결 필드
            'store_name',  # ✅ [추가] 빵집 이름 (read-only)
            'created_at',
            'updated_at',
            'like_users',
            'comments_count',
            'like_count',
        ]
        read_only_fields = ['author', 'like_users', 'store_name']

    def get_comments_count(self, obj):
        return obj.comments.filter(parent__isnull=True).count()

    def get_like_count(self, obj):
        return obj.like_users.count()
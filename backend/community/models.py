from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50)

    # 🚨 [수정] URLField -> ImageField로 변경
    # photo_url = models.URLField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='community/images/%Y/%m/%d/', blank=True, null=True)

    # ✅ [추가] 빵집 추천 카테고리를 위한 store 필드
    store = models.ForeignKey(
        'stores.Store',
        on_delete=models.CASCADE,
        related_name='community_posts',
        null=True,
        blank=True,
        help_text='빵집 추천 카테고리일 경우 연결된 빵집'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.category}] {self.title} by {self.author.username}'

# PostComment 모델은 그대로 유지...
class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.user.nickname}'
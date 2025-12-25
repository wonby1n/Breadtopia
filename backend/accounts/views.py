from rest_framework import generics
from dj_rest_auth.views import UserDetailsView
from .serializers import CustomUserDetailsSerializer, UserSerializer
from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView  # APIView 추가
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from stores.models import Store # Store 모델 필요 (스탬프용)
from django.shortcuts import get_object_or_404


User = get_user_model()


# dj-rest-auth의 UserDetailsView를 상속받아 우리가 만든 Serializer를 사용하도록 설정
class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserDetailsSerializer
    queryset = User.objects.all()
    
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_preferences(request):
    """빵 선호도 업데이트"""
    bread_preferences = request.data.get('bread_preferences', '')
    
    # 사용자 모델에 직접 저장
    request.user.bread_preferences = bread_preferences
    request.user.save()
    
    return Response({
        'bread_preferences': bread_preferences,
        'message': '빵 선호도 업데이트 완료'
    }, status=status.HTTP_200_OK)
    
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_image(request):
    """프로필 이미지 업데이트"""
    if 'profile_image' not in request.FILES:
        return Response({'error': '이미지 파일이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    profile_image = request.FILES['profile_image']
    
    # media/profile_images/ 폴더에 저장
    filename = default_storage.save(
        f'profile_images/{request.user.id}_{profile_image.name}', 
        profile_image
    )
    image_url = default_storage.url(filename)
    
    # DB에 URL만 저장
    request.user.profile_image_url = image_url
    request.user.save()
    
    return Response({
        'profile_image_url': image_url,
        'message': '프로필 이미지가 업데이트되었습니다.'
    }, status=status.HTTP_200_OK)
    
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    """현재 로그인한 사용자 정보 반환"""
    serializer = UserSerializer(request.user)  # UserSerializer 필요
    return Response(serializer.data)


# [추가] 마이페이지용 통합 데이터 조회 API (스탬프, 취향 분석 등 포함)
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user

            # 1. 📜 스탬프 데이터: 내가 리뷰를 남긴 가게들 + 빵집 추천 게시글을 쓴 가게들 (중복 제거)
            try:
                from django.db.models import Max, Q
                from community.models import Post

                # Review를 통해 방문한 가게 + Post를 통해 방문한 가게를 합침
                visited_stores_qs = Store.objects.filter(
                    Q(reviews__user=user) | Q(community_posts__author=user)
                ).distinct().annotate(
                    # Review 또는 Post 중 가장 최근 날짜를 visited_date로 사용
                    visited_date=Max('reviews__created_at')
                ).values('id', 'name', 'category', 'address', 'visited_date')

                # datetime 객체를 ISO 문자열로 변환
                visited_stores = []
                for store in visited_stores_qs:
                    store_data = dict(store)
                    if store_data.get('visited_date'):
                        store_data['visited_date'] = store_data['visited_date'].isoformat()
                    visited_stores.append(store_data)
            except Exception as e:
                print(f"visited_stores 에러: {e}")
                import traceback
                traceback.print_exc()
                visited_stores = []

            # 1-2. 📌 북마크한 빵집 목록
            try:
                from stores.serializers import StoreListSerializer
                bookmarked_stores_qs = user.bookmarked_stores.all()
                bookmarked_stores = StoreListSerializer(bookmarked_stores_qs, many=True, context={'request': request}).data
            except Exception as e:
                print(f"bookmarked_stores 에러: {e}")
                bookmarked_stores = []

            # 2. 🔮 취향 분석 데이터: 내가 쓴 리뷰들의 menu_items 집계
            all_menus = []
            try:
                for review in user.review_set.all():
                    if review.menu_items:
                        # 콤마로 구분된 메뉴들을 분리해서 리스트에 추가
                        menus = [m.strip() for m in review.menu_items.split(',') if m.strip()]
                        all_menus.extend(menus)
            except Exception as e:
                print(f"menu_items 에러: {e}")

            # 메뉴 빈도수 계산
            from collections import Counter
            menu_counts = Counter(all_menus)
            # 예: {'소금빵': 12, '크루아상': 8}

            # 많이 먹은 순서대로 정렬 (상위 10개)
            sorted_menus = dict(sorted(menu_counts.items(), key=lambda item: item[1], reverse=True)[:10])

            # 3. 커뮤니티 게시글 및 댓글 수 집계
            try:
                from community.models import Post
                from reviews.models import Comment

                post_count = Post.objects.filter(author=user).count()
                comment_count = Comment.objects.filter(user=user).count()
            except Exception as e:
                print(f"post/comment count 에러: {e}")
                post_count = 0
                comment_count = 0

            # 4. 팔로워/팔로잉 수
            try:
                follower_count = user.followers.count()
                following_count = user.follows.count()
            except Exception as e:
                print(f"follower/following count 에러: {e}")
                follower_count = 0
                following_count = 0

            # 5. 뱃지 데이터 (임시 더미 데이터)
            badges = [
                { 'name': '첫 리뷰', 'icon': '📝' },
                { 'name': '소금빵 러버', 'icon': '🥐' },
                { 'name': '오픈런', 'icon': '🏃' },
                { 'name': '빵지순례자', 'icon': '🗺️' }
            ]

            # 6. 최근 데이터 조회
            try:
                # 리뷰 데이터에 store 이름 포함 (select_related로 조인)
                user_reviews_qs = user.review_set.select_related('store').all().values('id', 'content', 'rating', 'created_at', 'store__name')
                user_reviews = []
                for review in user_reviews_qs:
                    review_data = dict(review)
                    if review_data.get('created_at'):
                        review_data['created_at'] = review_data['created_at'].isoformat()
                    user_reviews.append(review_data)
            except Exception as e:
                print(f"user_reviews 에러: {e}")
                user_reviews = []

            try:
                from community.models import Post
                # 전체 게시글 가져오기
                user_posts_qs = Post.objects.filter(author=user).values('id', 'title', 'category', 'created_at')
                user_posts = []
                for post in user_posts_qs:
                    post_data = dict(post)
                    if post_data.get('created_at'):
                        post_data['created_at'] = post_data['created_at'].isoformat()
                    user_posts.append(post_data)
            except Exception as e:
                print(f"user_posts 에러: {e}")
                user_posts = []

            try:
                from reviews.models import Comment
                user_comments_qs = Comment.objects.filter(user=user)[:3].values('id', 'content', 'created_at')
                user_comments = []
                for comment in user_comments_qs:
                    comment_data = dict(comment)
                    if comment_data.get('created_at'):
                        comment_data['created_at'] = comment_data['created_at'].isoformat()
                    user_comments.append(comment_data)
            except Exception as e:
                print(f"user_comments 에러: {e}")
                user_comments = []

            return Response({
                "username": user.username,
                "nickname": user.nickname if hasattr(user, 'nickname') else user.username,
                "level": user.level if hasattr(user, 'level') else 1,
                "exp": user.exp if hasattr(user, 'exp') else 0,
                "max_exp": (user.level if hasattr(user, 'level') else 1) * 100,
                "character_type": user.character_type if hasattr(user, 'character_type') else 'hamster',
                "profile_image_url": user.profile_image_url if hasattr(user, 'profile_image_url') else None,
                "visit_count": len(visited_stores),
                "review_count": user.review_set.count() if hasattr(user, 'review_set') else 0,
                "post_count": post_count,
                "comment_count": comment_count,
                "follower_count": follower_count,
                "following_count": following_count,
                "visited_stores": list(visited_stores),
                "bookmarked_stores": bookmarked_stores,
                "taste_stats": sorted_menus,
                "badges": badges,
                "user_reviews": user_reviews,
                "user_posts": user_posts,
                "user_comments": user_comments,
                "date_joined": user.date_joined.isoformat() if hasattr(user, 'date_joined') else None,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"UserProfileView 전체 에러: {e}")
            import traceback
            traceback.print_exc()
            return Response({
                "error": "프로필을 불러오는 중 오류가 발생했습니다.",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def check_nickname(request):
    nickname = request.GET.get('nickname', '').strip()

    # 비어있으면 사용 불가로 처리
    if not nickname:
        return JsonResponse({'available': False}, status=200)

    # 현재 로그인 유저는 자기 닉네임 그대로 쓰는 건 허용
    if request.user.is_authenticated and request.user.nickname == nickname:
        return JsonResponse({'available': True}, status=200)

    exists = User.objects.filter(nickname=nickname).exists()
    return JsonResponse({'available': not exists}, status=200)


# 팔로우/언팔로우 API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    """특정 사용자를 팔로우/언팔로우합니다."""
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    # 자기 자신을 팔로우할 수 없음
    if request.user == target_user:
        return Response({'error': '자기 자신을 팔로우할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # 이미 팔로우 중이면 언팔로우, 아니면 팔로우
    if target_user in request.user.follows.all():
        request.user.follows.remove(target_user)
        return Response({
            'status': 'unfollowed',
            'message': f'{target_user.nickname}님을 언팔로우했습니다.'
        }, status=status.HTTP_200_OK)
    else:
        request.user.follows.add(target_user)
        return Response({
            'status': 'followed',
            'message': f'{target_user.nickname}님을 팔로우했습니다.'
        }, status=status.HTTP_200_OK)


# 팔로워 목록 조회 API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def followers_list(request):
    """현재 사용자를 팔로우하는 사람들의 목록을 반환합니다."""
    followers = request.user.followers.all()
    followers_data = [{
        'id': user.id,
        'username': user.username,
        'nickname': getattr(user, 'nickname', user.username),  # ✅ 안전하게
        'profile_image_url': getattr(user, 'profile_image_url', None),  # ✅ 안전하게
        'level': getattr(user, 'level', 1),  # ✅ 안전하게
        'level_title': getattr(user, 'level_title', '아기빵쥐'),  # ✅ 안전하게
        'character_type': getattr(user, 'character_type', 'hamster'),  # ✅ 안전하게
    } for user in followers]

    return Response({
        'count': len(followers_data),
        'followers': followers_data
    }, status=status.HTTP_200_OK)


# 팔로잉 목록 조회 API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def following_list(request):
    """현재 사용자가 팔로우하는 사람들의 목록을 반환합니다."""
    following = request.user.follows.all()
    following_data = [{
        'id': user.id,
        'username': user.username,
        'nickname': getattr(user, 'nickname', user.username),  # ✅ 안전하게
        'profile_image_url': getattr(user, 'profile_image_url', None),  # ✅ 안전하게
        'level': getattr(user, 'level', 1),  # ✅ 안전하게
        'level_title': getattr(user, 'level_title', '아기빵쥐'),  # ✅ 안전하게
        'character_type': getattr(user, 'character_type', 'hamster'),  # ✅ 안전하게
    } for user in following]

    return Response({
        'count': len(following_data),
        'following': following_data
    }, status=status.HTTP_200_OK)



# accounts/views.py
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail_by_id(request, user_id):
    print('user_detail_by_id 호출됨, user_id =', user_id)
    user = get_object_or_404(User, id=user_id)
    print('조회된 user pk =', user.pk, 'nickname =', user.nickname)
    serializer = UserSerializer(user)
    return Response(serializer.data)

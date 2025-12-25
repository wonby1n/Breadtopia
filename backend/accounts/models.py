from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Badge(models.Model):
    """
    🏅 뱃지 정의 모델 (행동, 지역, 히든 등)
    """
    CATEGORY_CHOICES = [
        ('ACTION', '행동 기반'), # 크루아상 헌터 등
        ('REGION', '지역 기반'), # 부산 빵지순례자 등
        ('EVENT', '희귀/이벤트'), # 새벽빵 요정 등
    ]

    name = models.CharField(max_length=50, unique=True) # 뱃지 이름 (예: 식빵 장인)
    description = models.CharField(max_length=200)      # 설명 (예: 같은 빵집 5회 방문)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='ACTION')
    image_url = models.CharField(max_length=500, blank=True) # 뱃지 이미지 아이콘 경로
    condition_threshold = models.IntegerField(default=1) # 획득 조건 수치 (예: 10회)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.name}"

class User(AbstractUser):
    # --- 기존 필드 유지 ---
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    nickname = models.CharField(max_length=50, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    profile_image_url = models.CharField(max_length=500, blank=True)
    bread_preferences = models.CharField(max_length=255, blank=True)
    follows = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    # --- 2. 🐣 캐릭터 성장 시스템 확장 ---
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)
    
    # 캐릭터 등급명 (프론트엔드 표시용)
    level_title = models.CharField(max_length=50, default="아기빵쥐")
    
    # 획득한 뱃지 (Many-to-Many 관계)
    badges = models.ManyToManyField(Badge, through='UserBadge', related_name='holders')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    # --- 📈 레벨 데이터 정의 (상수) ---
    LEVEL_SYSTEM = {
        1: {'title': '아기빵쥐', 'threshold': 0, 'next_exp': 100},
        2: {'title': '식빵햄찌', 'threshold': 100, 'next_exp': 200},
        3: {'title': '호빵토끼', 'threshold': 200, 'next_exp': 300},
        4: {'title': '모닝코기', 'threshold': 300, 'next_exp': 400},
        5: {'title': '크루아상여우', 'threshold': 400, 'next_exp': 500},
        6: {'title': '브리오슈곰', 'threshold': 500, 'next_exp': 700},
        7: {'title': '사워도우울프', 'threshold': 700, 'next_exp': 800},
        8: {'title': '초코표범', 'threshold': 800, 'next_exp': 1000},
        9: {'title': '바게트호크', 'threshold': 1000, 'next_exp': 1500},
        10: {'title': '황금밀 유니콘', 'threshold': 1500, 'next_exp': 999999},
    }

    def __str__(self):
        return f"{self.nickname} (Lv.{self.level} {self.level_title})"

    # --- 3. 🚀 레벨업 및 경험치 로직 ---
    def gain_exp(self, amount):
        """
        경험치를 획득하고 레벨업 여부를 체크합니다.
        usage: user.gain_exp(20)
        """
        self.exp += amount
        self.save()
        return self.check_level_up()

    def check_level_up(self):
        """
        현재 경험치를 기준으로 레벨과 칭호를 재설정합니다.
        """
        current_level_info = self.LEVEL_SYSTEM.get(self.level)
        next_level_info = self.LEVEL_SYSTEM.get(self.level + 1)

        # 만약 다음 레벨이 있고, 현재 경험치가 다음 레벨 요구치보다 높다면
        if next_level_info and self.exp >= current_level_info['next_exp']:
            self.level += 1
            self.level_title = next_level_info['title']
            self.save()
            return True # 레벨업 함! (프론트에서 축하 알림 띄우기용)
        
        return False

    # --- 4. 🪪 빵 여권 데이터 메서드 ---
    def get_passport_stats(self):
        """
        마이페이지 '빵 여권'에 표시할 통계 데이터를 반환합니다.
        """
        # 가입일로부터 며칠 지났는지 계산 (First Bake)
        days_since_join = (timezone.now() - self.date_joined).days + 1
        
        # 스탬프 개수 (방문 인증 모델이 있다고 가정)
        # stamp_count = self.visits.count() 
        
        return {
            "nickname": self.nickname,
            "level": self.level,
            "title": self.level_title,
            "bread_power": self.exp, # 빵력
            "days_since_bake": days_since_join,
            "stamp_count": 0, # 임시
            "badges": [badge.name for badge in self.badges.all()]
        }

class UserBadge(models.Model):
    """
    🏅 뱃지 획득 기록 (획득 날짜 저장용)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    acquired_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge') # 중복 획득 방지
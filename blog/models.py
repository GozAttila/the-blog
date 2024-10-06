from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('User', 'User'),
        ('Blogger', 'Blogger'),
        ('Moderator', 'Moderator'),
        ('Subadmin', 'Subadmin'),
        ('Admin', 'Admin'),
    ]
    email = models.EmailField(unique=True)
    avatar = models.URLField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='User')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True
    )

    def __str__(self):
        return self.username

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_private = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    blocked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='blocked_blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class BlogTranslation(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(max_length=10)  # ISO 639-1 kódok
    translated_title = models.CharField(max_length=255)
    translated_content = models.TextField()

    def __str__(self):
        return f"{self.blog.title} ({self.language})"

class Invitation(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_blocked = models.BooleanField(default=False)
    blocked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='blocked_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.blog.title}"

class BlogLike(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blog', 'user')  # Egy felhasználó csak egyszer interakciózhat egy bloggal.

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')  # Egy felhasználó csak egyszer interakciózhat egy kommenttel.

class AdminLog(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_logs')
    action_type = models.CharField(max_length=100)
    target_id = models.IntegerField()  # Célzott entitás azonosítója
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Action by {self.admin.username}: {self.action_type}"

class Report(models.Model):
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50)  # Lehet 'comment', 'blog', 'message', stb.
    report_target_id = models.IntegerField()  # Jelentett entitás azonosítója
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.reported_by.username} ({self.report_type})"

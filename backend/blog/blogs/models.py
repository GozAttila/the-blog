from django.db import models
from django.conf import settings


class Blog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_private = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    blocked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='blocked_blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class BlogTranslation(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(max_length=10)
    translated_title = models.CharField(max_length=255)
    translated_content = models.TextField()

    def __str__(self):
        return f"{self.blog.title} ({self.language})"

class Invitation(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    invited_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitations')
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_invitations')
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

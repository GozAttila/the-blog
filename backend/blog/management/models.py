from django.db import models
from django.conf import settings
from django.utils.timezone import now

class ChangeRequest(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('name_change', 'Name Change'),
        ('email_change', 'Email Change')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    requested_name = models.CharField(max_length=150, blank=True, null=True)
    requested_email = models.EmailField(blank=True, null=True)
    reason = models.TextField()
    is_approved = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    changelog = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    handled_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='handled_requests', null=True, blank=True, on_delete=models.SET_NULL)
    handled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.request_type} request"

    def add_to_changelog(self, action, admin_user=None, old_value=None, new_value=None):
        timestamp = now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f"{timestamp} - {action}"
        if old_value and new_value:
            entry += f" (changed from {old_value} to {new_value})"
        if admin_user:
            entry += f" by {admin_user.username}"
        entry += "\n"
        self.changelog += entry
        self.save()

    def approve(self, admin_user):
        self.is_approved = True
        self.is_archived = True
        self.handled_by = admin_user
        self.handled_at = now()

        if self.request_type == 'name_change':
            old_name = self.user.username
            self.user.username = self.requested_name
            self.user.save()
            self.add_to_changelog("Request approved", admin_user, old_value=old_name, new_value=self.requested_name)

        elif self.request_type == 'email_change':
            old_email = self.user.email
            self.user.email = self.requested_email
            self.user.save()
            self.add_to_changelog("Request approved", admin_user, old_value=old_email, new_value=self.requested_email)

        self.save()

    def deny(self, admin_user):
        self.is_approved = False
        self.is_archived = True
        self.handled_by = admin_user
        self.handled_at = now()
        self.add_to_changelog("Request denied", admin_user)
        self.save()

    def reopen(self, admin_user):
        self.is_archived = False
        self.add_to_changelog("Request reopened", admin_user)
        self.save()

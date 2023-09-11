from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Task(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=2000)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title[:20]} & created by {self.user.username}"

    def get_details(self):
        return {
            "task_id": str(self.task_id),
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user_name": self.user.username,
        }

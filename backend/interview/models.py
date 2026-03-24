from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    ROLE_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('dsa', 'DSA'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    question_text = models.TextField()
    keywords = models.TextField()  # comma separated

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}"
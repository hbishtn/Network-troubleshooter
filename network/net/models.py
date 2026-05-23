from django.db import models
from django.contrib.auth.models import User


class Problem(models.Model):
    issue = models.TextField()
    solution = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

#for date and time save and user history of problems and solutions
class NetworkIssue(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    problem = models.TextField()

    response = models.TextField()
                                            
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.problem[:50]


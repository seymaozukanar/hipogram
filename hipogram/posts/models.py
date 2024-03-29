from django.db import models
from django.db.models import Avg


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Post(models.Model):
    image = models.ImageField()
    text = models.TextField()
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, help_text="Ctrl + click to select multiple", blank=True)

    def __str__(self):
        return self.created_by.username

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def average_rate(self):
        return self.rates.aggregate(Avg("value"))["value__avg"]


class Like(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} liked {self.post.created_by}'s post"


class Rate(models.Model):
    value = models.PositiveSmallIntegerField(choices=[(i, i) for i in [0, 1, 2, 3, 4, 5]], default=0)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="rates")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["post", "user"], name="unique_rate")
        ]

    def __str__(self):
        return f"{self.user} rated {self.value} to {self.post.created_by}'s post"

from django.db import models
from user.models import Profile
from PIL import Image


class Post(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to="photos")
    update = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.user}:{self.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width < 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    @property
    def image_url(self):

        if self.image:
            return self.image.url
        return ''

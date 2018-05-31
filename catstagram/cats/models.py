from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200)
    following = models.ManyToManyField('self', related_name='followers', blank=True)
    profile_picture = models.ImageField(upload_to='profile/', blank=True, default='default/profile/default-cat.jpeg')

    def __str__(self):
        return self.user.username

def user_directory_path(instance, filename):
    return '{}/{}'.format(instance.author.username, filename)

class Post(models.Model):
    caption = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    likers = models.ManyToManyField(User, blank=True)
    picture = models.ImageField(upload_to=user_directory_path, blank=True)

    def __str__(self):
        if len(self.caption) > 15:
            return self.caption[15]
        else:
            return self.caption

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=200)

    def __str__(self):
        if len(self.content) > 15:
            content = self.content[15]
        else:
            content = self.content

        return '@{} to @{} : {}...'.format(self.author.username,
                                        self.post.author.username,
                                        content)

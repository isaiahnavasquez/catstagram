from django.db import models
from django.contrib.auth.models import User

RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200)
    relationships = models.ManyToManyField('self',
                                            through='Relationship',
                                            symmetrical=False,
                                            related_name='related_to')
    profile_picture = models.ImageField(upload_to='profile/', default='default/profile/default-cat.jpeg')

    def add_relationship(self, person, status):
        relationship, created = Relationship.objects.get_or_create(
            from_person=self,
            to_person=person,
            status=status)
        return relationship

    def remove_relationship(self, person, status):
        Relationship.objects.filter(
            from_person=self,
            to_person=person,
            status=status).delete()
        return

    def get_relationships(self, status):
        return self.relationships.filter(
            to_people__status=status,
            to_people__from_person=self)

    def get_related_to(self, status):
        return self.related_to.filter(
            from_people__status=status,
            from_people__to_person=self)

    def get_following(self):
        return self.get_relationships(RELATIONSHIP_FOLLOWING)

    def get_followers(self):
        return self.get_related_to(RELATIONSHIP_FOLLOWING)

    def __str__(self):
        return self.user.username

class Relationship(models.Model):
    from_person = models.ForeignKey(Profile, related_name='from_people', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Profile, related_name='to_people', on_delete=models.CASCADE)
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)

def user_directory_path(instance, filename):
    return '{}/{}'.format(instance.author.username, filename)

class Post(models.Model):
    caption = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=user_directory_path)

    @property
    def likers(self):
        """Gets the ids of user that liked this post,
        used to determine in the template
        if a specific user is involved
        """
        likes = self.likes.all().values()
        users = [x['user_id'] for x in likes]
        return users

    def is_liked_by(self, user):
        """Checks if post is liked by a certain user"""
        output = Like.objects.filter(user=user, post=self)
        return True if output.count() == 1 else False

    def toggle_like(self, user):
        """Toggles like from user
        returns True if post is liked,
        returns False if unliked
        """
        if self.is_liked_by(user):
            Like.objects.get(post=self, user=user).delete()
            return False
        else:
            Like(post=self, user=user).save()
            return True

    def __str__(self):
        return str(self.pub_date) + self.caption

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'@{self.user.username} to {self.post.id}'

class Hashtag(models.Model):
    name = models.CharField(max_length=50)
    post = models.ManyToManyField(Post)

    def __str__(self):
        return '#' + str(self.name)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=200)

    def __str__(self):
        if len(self.content) > 15:
            content = self.content[15]
        else:
            content = self.content

        return '@{} to @{} : {}...'.format(self.author.username,
                                        self.post.author.username,
                                        content)

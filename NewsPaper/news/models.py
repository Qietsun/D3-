from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    author_User = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_Author = models.SmallIntegerField(default=0)

    def update_rating(self):
        post_Rat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += post_Rat.get('post_Rating')

        comment_Rat = self.author_User.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += comment_Rat.get('comment_Rating')

        self.rating_Author = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f'{self.author_User}, {self.rating_Author}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = "AR"
    CATEGORY_CHOICE = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    category_Type = models.CharField(max_length=2, choices=CATEGORY_CHOICE, default=ARTICLE)
    date_Creation = models.DateTimeField(auto_now_add=True)
    post_Category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating += 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def __str__(self):
        return f'{self.title}, {self.author}, {self.category_Type}, {self.text}, {self.date_Creation}, {self.post_Category}, {self.rating}'


class PostCategory(models.Model):
    post_Thorough = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_Through = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post_Thorough}, {self.category_Through}'


class Comment(models.Model):
    comment_Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_User = models.ForeignKey(User, on_delete=models.CASCADE)
    texst = models.TextField()
    dete_Creation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating += 1
        self.save()

    def __str__(self):
        return f'{self.comment_User}, {self.comment_Post}, {self.texst}, {self.dete_Creation}, {self.rating}'
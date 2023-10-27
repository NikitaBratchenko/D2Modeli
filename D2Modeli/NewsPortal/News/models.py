from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('ratingPost'))
        pRating = 0
        pRating += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('ratingCom'))
        cRating = 0
        cRating += commentRat.get('commentRating')

        self.ratingAuthor = pRating * 3 + cRating
        self.save()


class Category(models.Model):
    CategoryNewsState = models.CharField(max_length=64,
                                         unique=True)


class Post(models.Model):
    Author = models.ForeignKey(Author, on_delete=models.CASCADE)
    News = 'NW'
    Article = 'AR'
    CATEGORY_CHOICES = [
        (News, 'Новость'),
        (Article, 'Статья')
    ]
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=Article)
    dataCreation = models.DateTimeField(auto_now_add=True)
    post = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    ratingPost = models.IntegerField(default=0)

    def like(self):
        self.ratingPost += 1
        self.save()

    def dislike(self):
        self.ratingPost -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'


class PostCategory(models.Model):
    PostThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    CategoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    CommentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    CommentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    textCom = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    ratingCom = models.IntegerField(default=0)

    def like(self):
        self.ratingCom += 1
        self.save()

    def dislike(self):
        self.ratingCom -= 1
        self.save()

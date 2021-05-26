from django.db import models

class User(models.Model):
    email       = models.CharField(max_length=128)
    korean_name = models.CharField(max_length=64)
    password    = models.CharField(max_length=64, default="")
    kakao_id    = models.IntegerField(default=None, null=True)
    coupon      = models.ManyToManyField('Coupon', through='UserCoupon', related_name='users')
    comment     = models.ManyToManyField('courses.Review', through='Comment', related_name='reviewer')
    like        = models.ManyToManyField('courses.Course', through='Like', related_name='liked_user')
    look        = models.ManyToManyField('courses.Course', through='Look', related_name='looked_user')

    class Meta:
        db_table = 'users'

class Coupon(models.Model):
    name          = models.CharField(max_length=128)
    discount_rate = models.IntegerField()

    class Meta:
        db_table = 'coupons'

class UserCoupon(models.Model):
    coupon = models.ForeignKey('Coupon', on_delete=models.CASCADE)
    user   = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_coupon'

class Comment(models.Model):
    review = models.ForeignKey('courses.Review', on_delete=models.CASCADE)
    user   = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comments')
    text   = models.TextField(default=None)

    class Meta:
        db_table = 'comments'

class Like(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    user   = models.ForeignKey('User', on_delete=models.CASCADE, related_name='likes')

    class Meta:
        db_table = 'likes'

class Look(models.Model): 
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    user   = models.ForeignKey('User', on_delete=models.CASCADE, related_name='looks')

    class Meta:
        db_table = 'looks'

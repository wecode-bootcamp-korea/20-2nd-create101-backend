from django.db import models

class User(models.Model):
    email       = models.CharField(max_length=128)
    korean_name = models.CharField(max_length=64)
    password    = models.CharField(max_length=64)
    first_login = models.BooleanField()
    coupon      = models.ManyToManyField('Coupon', through='UserCoupon', related_name='user')
    comment     = models.ManyToManyField('course.Review', through='Comment', related_name='user')
    like        = models.ManyToManyField('course.Course', through='Like', related_name='user')
    look        = models.ManyToManyField('course.Course', through='Look', related_name='user')

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
    review = models.ForeignKey('course.Review', on_delete=models.CASCADE)
    user   = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'

class Like(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE)
    user   = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'

class Look(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE)
    user   = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'looks'


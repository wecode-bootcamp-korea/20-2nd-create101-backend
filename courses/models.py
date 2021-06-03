from django.db     import models


class Course(models.Model):
    target       = models.ForeignKey('Target', on_delete=models.CASCADE)
    # 설명에 html 코드가 들어갑니다.
    description  = models.TextField()
    # 이미지는 한장만 사용됩니다.
    thumbnail    = models.FileField()
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    title        = models.CharField(max_length=300)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    month        = models.IntegerField()
    created_at   = models.DateTimeField(auto_now_add=True)
    review       = models.ManyToManyField('users.User', related_name='reviewed_course')

    class Meta:
        db_table = 'courses'

class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'categories'

class SubCategory(models.Model):
    name     = models.CharField(max_length=64)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='sub_categorys')

    class Meta:
        db_table='sub_categories'

class Target(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'targets'

class Review(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='course_review')
    user   = models.ForeignKey('users.User', on_delete=models.CASCADE)
    text   = models.TextField()

    class Meta:
        db_table = 'reviews'

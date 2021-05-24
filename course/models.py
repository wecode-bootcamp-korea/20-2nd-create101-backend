from django.db                 import models

class Course(models.Model):
    target       = models.ForeignKey('Target', on_delete=models.CASCADE, related_name='course')
    description  = models.TextField()
    thumbnail    = models.CharField(max_length=2000)
    price        = models.DecimalField(max_digits=8, decimal_places=2)
    title        = models.CharField(max_length=300)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE, related_name='course')
    user         = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='course')
    month        = models.IntegerField()
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'courses'

class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'categories'

class SubCategory(models.Model):
    name     = models.CharField(max_length=64)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='sub_category')

    class Meta:
        db_table='sub_categories'

class Target(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'targets'

class Review(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    user   = models.ForeignKey('user.User', on_delete=models.CASCADE)
    text   = models.TextField()

    class Meta:
        db_table = 'reviews'

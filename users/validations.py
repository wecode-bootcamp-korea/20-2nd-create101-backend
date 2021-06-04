from django.db.models   import Count

def validate_courses(name, user):
    if name == 'user_craete_course':
        user_courses = user.course_set.all()
    elif name == 'liked_course':
        user_courses = user.like.all()
    elif name == 'looked_course':
        user_courses = user.look.all()
        
    all_courses = [{ 
        'id'          : course.id,
        'title'       : course.title,
        'sub_category': course.sub_category.name,
        'user'        : course.user.korean_name,
        'like'        : course.like_set.all().aggregate(user_count=Count('user'))['user_count'],
        'price'       : int(course.price),
        'thumbnail'   : str(course.thumbnail),
        'month'       : course.month,
        'liked'       : user in course.liked_user.all()
    } for course in user_courses]
    
    return all_courses
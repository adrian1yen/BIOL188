import factory
from users import models as user_models
from django.contrib.auth.models import User
from users import keys as user_keys

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Faker('first_name')

class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = user_models.UserProfile

    user = factory.SubFactory(UserFactory)

class TeacherFactory(UserProfileFactory):
    class Meta:
        model = user_models.Teacher

    role = user_keys.TEACHER

class MentorFactory(UserProfileFactory):
    class Meta:
        model = user_models.Mentor

    role = user_keys.MENTOR

class StudentFactory(UserProfileFactory):
    class Meta:
        model = user_models.Student

    role = user_keys.STUDENT

class ClassroomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = user_models.Classroom

    name = factory.Faker('company')
    teacher = factory.SubFactory(TeacherFactory)

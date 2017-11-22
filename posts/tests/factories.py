import factory
from posts import models as post_models
from users.tests.factories import StudentFactory, ClassroomFactory, UserProfileFactory

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = post_models.Post

    author = factory.SubFactory(StudentFactory)
    classroom = factory.SubFactory(ClassroomFactory)
    content = factory.Faker('sentence')

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = post_models.Comments

    author = factory.SubFactory(UserProfileFactory)
    post = factory.SubFactory(PostFactory)
    content = factory.Faker('sentence')

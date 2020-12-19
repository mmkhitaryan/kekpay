import factory


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'users.User'

    id = factory.Faker('uuid4')
    phone = factory.Iterator(['77082334567', '77772334567'])


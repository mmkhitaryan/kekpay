import factory

class AccountFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'accounts.Account'

    id = factory.Faker('uuid4')
    balance = 0


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'users.User'

    id = factory.Faker('uuid4')
    phone = factory.Iterator(['77082334567', '77772334567'])

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        self.accounts.add(AccountFactory())

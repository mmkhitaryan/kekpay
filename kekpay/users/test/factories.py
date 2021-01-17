import factory

class AccountFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'accounts.Account'

    balance = 0


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'users.User'

    phone = factory.Iterator(['77082334567', '77772334567'])

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        self.accounts.add(AccountFactory())

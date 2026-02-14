import factory

from app.db.db_user import User, pwd_context


class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Sequence(lambda n: f"User{n}")
    email = factory.LazyAttribute(
        lambda obj: f"{obj.name.lower()}@example.com"
    )
    password = factory.LazyAttribute(
        lambda o: pwd_context.hash("DefaultP@ssw0rd!")
    )

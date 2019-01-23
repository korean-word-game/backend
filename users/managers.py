from django.contrib.auth.models import BaseUserManager
from config.utils import get_sha512, get_token


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.token = get_token(user.uuid.urn.__str__())
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            password=password,
            username=username,
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user

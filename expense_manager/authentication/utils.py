from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class UserVerificationToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: AbstractBaseUser, timestamp: int) -> str:
        return (text_type(user.pk)+text_type(user.is_active)+text_type(timestamp))

token_generator = UserVerificationToken()

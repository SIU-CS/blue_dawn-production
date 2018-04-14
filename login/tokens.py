from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class Account_Activation(PasswordResetTokenGenerator):
	def hashValue(self, user, timestamp):
		return (
			six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.confirm.confirmation)

			)
accountActivation = Account_Activation()
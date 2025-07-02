from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

#archivo creado ya que el backend por defecto de django sigue esperando username
#cambia: UserModel.objects.get(username=username)
#por: UserModel.objects.get(email=username)
#evitando usar username=email que rompe el sistema

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

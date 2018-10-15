from django.contrib.auth import get_user_model
from django.http import Http404, JsonResponse
from django.views.generic import View

from utils.mixins.views import SuperuserRequiredMixin

UserModel = get_user_model()


class GetUserFromFormGenerateCodeApiView(SuperuserRequiredMixin, View):
    """Obtener username y email del usuario en el form GenerateCodePromoToUserForm
    para estar seguros de a quien se le enviá el code.
    """
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        if not request.is_ajax():
            raise Http404
        user_data = {
            'username': 'No existe un usuario con la id <strong>{}</strong>'.format(user_id),
            'email': 'El usuario no existe'
        }
        try:
            user_id = int(user_id)
        except ValueError:
            user_id = 0
        if user_id > 0:
            try:
                user = UserModel.objects.get(pk=user_id)
                user_data = {
                    'username': user.username,
                    'email': user.email
                }
            except UserModel.DoesNotExist:
                pass
        return JsonResponse(user_data)

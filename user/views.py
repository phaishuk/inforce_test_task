from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from user.permissions import IsOwnerOrAdminOrReadOnly
from user.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    model = get_user_model()
    queryset = get_user_model().objects.all()
    # permission_classes = (IsOwnerOrAdminOrReadOnly,)

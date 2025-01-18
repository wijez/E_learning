from rest_framework import status, permissions, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import LimitOffsetPagination


class BaseUserViewSet(GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data, context={'request': request, 'user': user})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)

    def filter_queryset(self, queryset):
        queryset = queryset.filter(user=self.request.user).order_by('-created_at')
        return queryset

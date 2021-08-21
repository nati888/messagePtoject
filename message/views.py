from django.contrib.auth import get_user, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from message.models import Message, User
from message.permissions import IsOwnerOrReceiver
from message.serializers import MessageSerializer, UserSerializer


class LoginViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        data = request.data
        username = data.get("username")
        password = data.get("password")

        if username is None or password is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Invalid request, data is missing.")

        user = authenticate(username=username, password=password)
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Invalid credentials, please try again.")

        login(request=request, user=user)

        return Response(UserSerializer(user).data)


class LogoutViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request: Request) -> Response:
        logout(request=request)
        return Response(status=status.HTTP_200_OK)


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsOwnerOrReceiver]

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def my_messages(self, request: Request, *args, **kwargs):
        instance: User = get_user(request=request)

        page = self.paginate_queryset(instance.get_messages_as_receiver())
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(instance.get_messages_as_receiver(), many=True)
        return Response(serializer.data)


class UserViewSet(GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(methods=["GET"], detail=True)
    def messages(self, request: Request, *args, **kwargs) -> Response:
        """
        Return back all the messages that the user receives.
        Example >> users/<user_id>/messages. Return the user_id messages.
        """
        # get query params with the argument ?seen=True/False
        seen_messages = request.query_params.get("seen")

        # get the user instance by the id in the url
        instance: User = super().get_object()

        messages = instance.get_messages_as_receiver()

        if seen_messages is not None:
            messages = instance.get_messages_as_receiver(seen=seen_messages)

        serializer = MessageSerializer(instance=messages, many=True)

        # mark messages as seen
        Message.objects.mark_messages_as_seen(messages=messages)
        return Response(serializer.data)

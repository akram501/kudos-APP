from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from core.models import User, Kudo
from kudoapp.serializers import UserListSerializer, GiveKudoSerializer, ReceivedKudoSerializer


class UserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        org_users = current_user.organization.user_set.exclude(id=current_user.id)

        serializer = UserListSerializer(org_users, many=True)
        return Response({
            "message": "User list fetched successfully",
            "data": serializer.data
        })


class GiveKudoAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GiveKudoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            giver = request.user
            receiver = User.objects.get(id=serializer.validated_data['receiver_id'])
            message = serializer.validated_data['message']

            kudo = Kudo.objects.create(
                sender=giver,
                receiver=receiver,
                message=message
            )

            return Response({
                "status": True,
                "message": "Kudo given successfully.",
                "data": {
                    "id": kudo.id,
                    "receiver": {
                        "id": receiver.id,
                        "name": receiver.name,
                        "email": receiver.email
                    },
                    "message": kudo.message,
                    "given_at": kudo.created_at
                }
            })
        else:
            # errors will be formatted by your custom_exception_handler
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReceivedKudosAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        kudos = user.received_kudos.select_related('sender').order_by('-created_at')
        serializer = ReceivedKudoSerializer(kudos, many=True)
        return Response({
            "status": True,
            "message": "Success",
            "data": serializer.data
        })


class RemainingKudosAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        now = timezone.now()
        start_of_week = now - timedelta(days=now.weekday())  # Monday 00:00

        kudos_given_count = user.given_kudos.filter(
            created_at__gte=start_of_week
        ).count()

        remaining = max(0, settings.NO_OF_KUDO_PER_WEEK - kudos_given_count)

        return Response({
            "status": True,
            "message": "Success",
            "data": {
                "kudos_given": kudos_given_count,
                "kudos_remaining": remaining
            }
        }, status=status.HTTP_200_OK)

from django.conf import settings
from rest_framework import serializers
from core.models import User, Kudo
from django.utils import timezone
from datetime import timedelta


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')


class GiveKudoSerializer(serializers.Serializer):
    receiver_id = serializers.UUIDField()
    message = serializers.CharField(max_length=500)

    def validate(self, data):
        giver = self.context['request'].user
        try:
            receiver = User.objects.get(id=data['receiver_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Receiver not found.")

        if receiver.organization_id != giver.organization_id:
            raise serializers.ValidationError("Cannot give kudos outside your organization.")

        if receiver.id == giver.id:
            raise serializers.ValidationError("You cannot give kudos to yourself.")

        # Check kudos count for this week
        now = timezone.now()
        start_of_week = now - timedelta(days=now.weekday())  # Monday 00:00

        kudos_given = Kudo.objects.filter(
            sender=giver,
            created_at__gte=start_of_week
        ).count()

        if kudos_given >= settings.NO_OF_KUDO_PER_WEEK:
            raise serializers.ValidationError("You have already given your 3 kudos for this week.")

        return data


class ReceivedKudoSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()

    class Meta:
        model = Kudo
        fields = ['id', 'from_user', 'message', 'created_at']

    def get_from_user(self, obj):
        return {
            "id": obj.sender.id,
            "name": obj.sender.name,
            "email": obj.sender.email
        }

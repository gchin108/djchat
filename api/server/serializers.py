from rest_framework import serializers
from .models import Server, Category, Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"


class ServerSerializer(serializers.ModelSerializer):
    num_members = serializers.SerializerMethodField()
    channel_server = ChannelSerializer(many=True)

    class Meta:
        model = Server
        fields = "__all__"
        # exclude = [
        #     "member",
        # ]

    def get_num_members(self, obj):
        """
        returns the number of members for a Server object (obj). The method first checks if the obj (the Server instance being serialized) has an attribute called num_members. If the Server instance has a num_members attribute, the function returns it. Otherwise, it returns None.
        """
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        num_members = self.context.get("num_members")
        if not num_members:
            data.pop("num_members", None)
        return data

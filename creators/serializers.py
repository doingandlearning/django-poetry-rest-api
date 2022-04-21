from rest_framework import serializers

from creators.models import Creator


class CreatorSerializer(serializers.ModelSerializer):
    creations = serializers.StringRelatedField(read_only=True, many=True)

    link = serializers.SerializerMethodField("get_link_from_id")

    class Meta:
        model = Creator
        fields = ("first_name", "last_name", "creations", "link")

    def get_link_from_id(self, creator):
        return f"http://localhost:8000/creators/{creator.id}"

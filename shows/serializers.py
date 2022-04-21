from rest_framework import serializers

from actors.models import Actor
from creators.models import Creator
from .models import Show


class CreatorSerializer(serializers.ModelSerializer):

   #  link = "http://localhost:8000/creators/id"

    class Meta:
        model = Creator
        fields = ("first_name", "last_name")


class ShowSerializer(serializers.ModelSerializer):
    """ Serializer of a show """

    creator = CreatorSerializer()
    supporting_actors = serializers.StringRelatedField(
        many=True, read_only=True)

    class Meta:
        model = Show
        fields = '__all__'

    # to serialize the creation of the nested resources
    def create(self, data):
        creator_data = data.pop("creator")

        show = Show(**data)
        creator, _created = Creator.objects.get_or_create(**creator_data)
        show.creator = creator
        show.save()
        # data doesn't have creator_data
        return show

    def update(self, show, data):
        creator_data = data.pop("creator")

        show.title = data.get("title", show.title)
        show.image = data.get("image", show.image)
        show.year = data.get("year", show.year)
        show.number_of_seasons = data.get(
            "number_of_seasons", show.number_of_seasons)
        show.worth_a_watch = data.get("worth_a_watch", show.worth_a_watch)

        if creator_data:
            creator, _created = Creator.objects.get_or_create(**creator_data)
            show.creator = creator

        show.save()

        return show

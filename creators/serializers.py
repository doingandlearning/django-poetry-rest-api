from tkinter.filedialog import askdirectory
from rest_framework import serializers

from creators.models import Creator


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = "__all__"

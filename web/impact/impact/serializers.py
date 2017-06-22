# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from rest_framework import serializers


class GeneralSerializer(serializers.ModelSerializer):

    class Meta:
        model = None
        fields = '__all__'

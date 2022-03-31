from django.contrib.auth.models import User
from forum.models import Question, Tag
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        #securitée
        extra_kwargs = {'password':{'write_only':True}}
    def create (self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class QuestionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'body']


class QuestionDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'body', 'created_at', 'tags', 'user']


class TagFilterSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'slug']


class TagFilterSlugModelSerializer(serializers.ModelSerializer):
    tags = TagFilterSerializer()
    class Meta:
        model = Question
        #element a passer dans le json, récupérable dans le ajax
        fields = ['tags', 'title', 'body', 'pk']
        # en activant la variable ci-dessous nous rendrons le remplissage du champs tag obligatoire
        extra_kwargs = {'tags': {'required': True}, 'title': {'required': True}}
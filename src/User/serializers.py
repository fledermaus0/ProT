from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

User =get_user_model()
class UserCreateSerializer(UserCreateSerializer):
	class Meta(UserCreateSerializer.Meta):
		model =User
		fields =('id','username','first_name','last_name','email','CIN','birthdate','phone','password','admin')

class UserBrefSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields=('id','username','first_name','last_name')

class UserSimpleSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields=('id','username')

class UserMainSerializer(serializers.ModelSerializer):
	class Meta:
		model =User
		fields =('id','username','first_name','last_name','email','CIN','birthdate','phone','is_admin','profile','last_login','admin')
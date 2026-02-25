from rest_framework import serializers
import datetime
from account.models import User,  Profile, Box, ProfilePersonalRecord
from django.core.validators import MaxValueValidator, MinValueValidator


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['username','first_name','last_name', 'email', 'password1', 'password2']


    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Usuário já existe')
        return username
    
    def clean_email (self):
        email = self.cleaned_data['email']
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email já existe')
        return email
    

class CreateProfileSerializer(serializers.ModelSerializer):

    birthday = data = serializers.DateField(
    format="%d/%m/%Y",              # como será exibido na resposta
    input_formats=["%d/%m/%Y"]      # como será aceito na requisição
)
    class Meta:
        model = Profile
        fields = ['photo','birthday', 'category', 'box', 'genre', 'weight', 'height', ]


    def clean_birthday (self):
        value = self.cleaned_data.get('birthday')
    

        if  value.year <  1925 or value.year > datetime.datetime.now().year:
            raise serializers.ValidationError( 'DATA INVALIDA')
        return value
        
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
 
 
class UserUpdateSerializer(serializers.ModelSerializer):
    box = serializers.PrimaryKeyRelatedField(
        queryset=Box.objects.all(),
        required=False
    )
    category = serializers.ChoiceField(
        choices=Profile.CATEGORY_CHOICES,
        required=False
    )
    genre = serializers.ChoiceField(
        choices=Profile.GENRE_CHOICES,
        required=False
    )
    weight = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False
    )
    height = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'box',
            'category',
            'genre',
            'weight',
            'height'
        ]

    def update(self, instance, validated_data):
        # Dados do profile
        box = validated_data.pop('box', None)
        category = validated_data.pop('category', None)
        genre = validated_data.pop('genre', None)
        weight = validated_data.pop('weight', None)
        height = validated_data.pop('height', None)

        # Atualiza campos do User
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Atualiza Profile
        profile, created = Profile.objects.get_or_create(user=instance)

        if box is not None:
            profile.box = box
        if category is not None:
            profile.category = category
        if genre is not None:
            profile.genre = genre
        if weight is not None:
            profile.weight = weight
        if height is not None:
            profile.height = height

        profile.save()

        return instance


class UserUpdatePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['photo']


class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        instance.set_password(password)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

    def get_photo(self, obj):
        request = self.context.get("request")
        if obj.photo:
            return request.build_absolute_uri(obj.photo.url)
        return None


class PrivacySerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['view_weight', 'view_height', 'view_category', 'view_box','view_personal_record']
        read_only_fields = ["id"]  #impede  que a  view  valide o id. Ele não será atualizado, apenas retornado.

    


class PersonalRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfilePersonalRecord
        fields = ['moviment','date','personal_record',]
        read_only_fields = ["athlete"]


class UserNestedSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["photo","box"]

    def get_photo(self, obj):
        request = self.context.get("request")
        if obj.photo:
            return request.build_absolute_uri(obj.photo.url)
        return None


class UserSerializer(serializers.ModelSerializer):

    profile = UserNestedSerializer(read_only=True) 
    class Meta:
        model = User
        fields = ["id", "profile", "username", "email", "first_name", "last_name" ]


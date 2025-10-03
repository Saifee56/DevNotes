from rest_framework import serializers
from api.models import CustomUserModel,Category,Blogs,Comment,Contact
from django.contrib.auth import get_user_model

class CustomUserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=CustomUserModel
        fields=['id','username','email','first_name','last_name','password']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def create(self,validated_data):
        username=validated_data["username"]
        email=validated_data["email"]
        first_name=validated_data["first_name"]
        last_name=validated_data["last_name"]
        password = validated_data.pop("password")   

        user=get_user_model()

        new_user=user.objects.create(username=username,email=email,first_name=first_name,
                            last_name=last_name)
        
        new_user.set_password(password)
        new_user.save()
        return new_user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

    def validate_name(self, value):
        """Prevent duplicate category names"""
        cleaned_name = value.strip().title()
        
        # Check for duplicates (excluding current instance if updating)
        existing = Category.objects.filter(name__iexact=cleaned_name)
        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise serializers.ValidationError("Category with this name already exists")
        
        return cleaned_name


    
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    blogs = serializers.PrimaryKeyRelatedField(queryset=Blogs.objects.all(),required=False) 
    class Meta:
        model=Comment
        fields=['id','content','time','blogs','user']
        read_only_fields = ['user', 'time']

class BlogsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True) 
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)  
    class Meta:
        model=Blogs
        fields=['id','title','category','description','time','total_likes','user','comments','user_id','category_name']
        read_only_fields = ['user'] 

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields=['id','name','email','subject','message']
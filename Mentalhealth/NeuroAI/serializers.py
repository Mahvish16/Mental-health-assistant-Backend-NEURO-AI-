from rest_framework import serializers
from .models import RegisterUser, Questions, Response, Disorder, DisorderSave

class RegisterSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True)
    class Meta:
        model = RegisterUser
        fields = ('name','email','phone_number','dob','age','address','occupation','password')
    def create(self, validated_data):
        user = RegisterUser.objects.create_user(
            name = validated_data['name'],
            email = validated_data['email'],
            phone_number = validated_data['phone_number'],
            dob = validated_data['dob'],
            age =  validated_data['age'],
            address = validated_data['address'],
            occupation = validated_data['occupation'],
            password = validated_data['password'],
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

class QuestionsSerializer(serializers.Serializer):
    class Meta:
        model = Questions
        fields = ('question')

# class ResponseSerializer(serializers.Serializer):
#     class Meta:
#         model = Response
#         fields = ['id','question','response','user']
#         read_only_fields = ['user']

#     def create(self, validated_data):
#         print(validated_data)
#         return Response.objects.create(**validated_data)
class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id','question','response','user']
        read_only_fields = ['id','user']

class BulkResponseSerializer(serializers.Serializer):
    responses = ResponseSerializer(many=True)
    def create(self, validated_data):
        responses_data = validated_data['responses']
        user = self.context['request'].user
        responses = [Response(user=user, **response) for response in responses_data]
        return Response.objects.bulk_create(responses)

class DisorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disorder
        fields = ['disorder', 'exercise', 'meditation']
    

        

    

 
  
    






    

        




        

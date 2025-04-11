from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from .models import RegisterUser, Questions, Response as ResponseTable , DisorderSave,Disorder,PasswordReset
from .serializers import RegisterSerializer,LoginSerializer, QuestionsSerializer, ResponseSerializer,BulkResponseSerializer, DisorderSerializer, LogoutSerializer,ResetPasswordRequestSerializer,ResetPasswordSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response 
from rest_framework import status,permissions
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import ValidationError


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = RegisterUser.objects.all()
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request,*args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request,email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"message": "Invalid credentials"}, status=401)
        
class logoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request,*args, **kwargs):
        serializer =  self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(serializer)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            print('email', email)
            user = RegisterUser.objects.filter(email=email).first()
            print(user)

            if user:
               token_generator = PasswordResetTokenGenerator()
               token = token_generator.make_token(user)
               reset = PasswordReset(email=email, token=token)
               reset.save()
            #       Add your frontend url of forgot password
               reset_url = f'http://localhost:9000/resetpassword.html?token={token}'  
               send_mail(
                   'Password Reset Request',
                   f'Please go to the following link to reset your password: {reset_url}',
                   'mahvish.ruhi@gmail.com',
                   [email],
                   fail_silently=False
                   )
               return Response({"message": "Password reset link sent to your email"}, status=200)
            else:
               return Response({"message": "User not found"}, status=404)
        return Response(serializer.errors, status=400)
                
class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        new_password = data['password']
        confirm_password = data['confirmpassword']
        
        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)
        
        reset_obj = PasswordReset.objects.filter(token=token).first()
        
        if not reset_obj:
            return Response({'error':'Invalid token'}, status=400)
        
        user = RegisterUser.objects.filter(email=reset_obj.email).first()
        
        if user:
            user.set_password(request.data['password'])
            user.save()
            
            reset_obj.delete()
            
            return Response({'success':'Password updated'})
        else: 
            return Response({'error':'No user found'}, status=404)
                
class QuestionsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,*args, **kwargs):
        questions = Questions.objects.all()
        question_list = [{"id":q.id,"question": q.question} for q in questions]
        question_res = {'questions': question_list}
        return Response(question_res)
    
# class ResponseView(viewsets.ModelViewSet):
#     serializer_class = ResponseSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     # def get_queryset(self):
#     #     return ResponseTable.objects.filter(user = self.request.user)
#     def perform_create(self, serializer):
#         print(serializer)
#         serializer.save(user=self.request.user)

class ResponseView(generics.GenericAPIView):
    serializer_class = ResponseSerializer
    permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user= self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BulkResponseView(generics.GenericAPIView):
    serializer_class = BulkResponseSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            responses_data = serializer.save()
            responses_serialized_data = ResponseSerializer(responses_data, many=True).data
            return Response({"responses": responses_serialized_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])    
def Disorder_recommendation(request):
    if request.method == 'GET':
        user_responses = ResponseTable.objects.filter(user=request.user, response = "Yes")
        print(user_responses)
        count = user_responses.count()
        print(count)
        question_id = user_responses.values_list('question_id', flat = True)
        print(question_id)
        disorder_id = DisorderSave.objects.filter(question_id__in=question_id).values_list('disorder_id', flat=True)
        print(disorder_id)
        disorders = Disorder.objects.filter(id__in=disorder_id).distinct()
        print(disorders)
        disorder_serializer = DisorderSerializer(disorders, many=True)
        print(disorder_serializer)
        data = {
            "disorders": disorder_serializer.data
        }
        
        return Response(data, status=status.HTTP_200_OK)
        






        
    




       
        

            

            

        

        
            
        
    
    

        

        
        
    

    





    
        



    


    

    
        

        

    
       



        


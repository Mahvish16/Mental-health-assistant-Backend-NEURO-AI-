from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import RegisterUser, Questions, Response as ResponseTable , DisorderSave,Disorder
from .serializers import RegisterSerializer,LoginSerializer, QuestionsSerializer, ResponseSerializer,BulkResponseSerializer, DisorderSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response 
from rest_framework import status,permissions
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse


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
        






        
    




       
        

            

            

        

        
            
        
    
    

        

        
        
    

    





    
        



    


    

    
        

        

    
       



        


from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Movie, Rating
from django.contrib.auth.models import User
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            try:
                movie = Movie.objects.get(id = pk)
            except:
                return Response({'message': 'Invalid index for movie'}, status=status.HTTP_400_BAD_REQUEST)
            stars = request.data['stars']
            user = request.user
            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                message = 'Rating Updated Successfully!'
            except:
                rating = Rating.objects.create(user=user, movie = movie, stars = stars)
                message = 'Rating Created Successfully!'
            serializer = RatingSerializer(rating, many=False)
            response = {'message': message, 'result': serializer.data}
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {'message': 'Please provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
 
        
        
        
    
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
       #Overriding predetermined methods of the Viewset so that user cannot use update and create requests on movie api
    def update(self, request, pk):
        return Response({'message': 'METHOD UPDATE NOT ALLOWED'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request):
        return Response({'message': 'METHOD CREATE NOT ALLOWED'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
    
    

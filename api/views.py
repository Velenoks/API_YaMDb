from django.shortcuts import render
from rest_framework import status

from .models import Titles, Genre, Category, GenreTitle

class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    # тут, по идее, не должно быть ограничений вообще. или только Администратор на создание, патч и удаление

    def perform_create(self, serializer):
        serializer.save()
    #     пока не пойму - тут делать проверку на права администратора. или в сериализаторе?
    # и вообще - эта операция справляется со всей троицей put/patch/delete?

    def get_titles(self):
        titles = Titles.objects.all().filter('pub_date')
        if request.method == 'GET':
            serializer = TitlesSerializer(Titles)
            if serializer.is_valid():
                serializer = TitlesSerializer(Titles, titles, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_titles(self, id):
        titles = Titles.objects.get(pk=id)
        if request.method == 'GET':
            serializer = TitlesSerializer(Titles)
            if serializer.is_valid():
                serializer = TitlesSerializer(Titles, titles)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
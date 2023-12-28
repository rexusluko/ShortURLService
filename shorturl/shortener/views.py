from django.http import HttpResponseRedirect, Http404
from rest_framework.generics import CreateAPIView, get_object_or_404, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .utils import next_code
from .serializers import LinkSerializer,DecodeLinkSerializer
from django.utils import timezone

def redirect_original_url(request, short_url):
    try:
        link = Link.objects.get(short_url=short_url)  # Получаем объект Link по короткой ссылке
    except Link.DoesNotExist:
        raise Http404("Ссылка не найдена")  # Возбуждаем 404 ошибку, если ссылка не найдена

    # Обновляем время последнего доступа к ссылке
    link.last_accessed = timezone.now()
    link.save(update_fields=['last_accessed'])

    return HttpResponseRedirect(link.original_url)  # Перенаправляем на оригинальную ссылку
class CreateLinkAPIView(CreateAPIView):
    """Создаёт короткую ссылку по оригинальной ссылке для авторизованного пользователя"""
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        original_url = request.data.get('original_url')
        existing_link = Link.objects.filter(original_url=original_url).first()

        if existing_link:
            serializer = LinkSerializer(existing_link)
            return Response(serializer.data, status=status.HTTP_200_OK)

        free_code = DeletedCode.objects.filter(code__isnull=False).first()
        if free_code:
            free_code.delete()  # Удаляем использованный свободный код
            short_url_code = free_code.code
        else: # Если не нашёлся код для переиспользования, то генерируем новый
            code_state = CodeState.objects.first()
            last_code = code_state.last_code
            if last_code == 'zzzzzzzz':
                return Response({'message': 'Нет свободных кодов для использования.'},
                                status=status.HTTP_400_BAD_REQUEST)
            short_url_code = next_code(last_code)  # Генерируем новый код
            code_state.last_code = short_url_code
            code_state.save()

        # Создаем новую ссылку с подобранным кодом
        link_data = {'original_url': original_url, 'short_url': short_url_code}
        serializer = LinkSerializer(data=link_data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLinksAPIView(ListAPIView):
    """Возвращает все ссылки у авторизованного пользователя"""
    serializer_class = LinkSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)

class DecodeLinkAPIView(RetrieveAPIView):
    """Возвращает оригинальную ссылку по короткой ссылке"""
    serializer_class = DecodeLinkSerializer

    def retrieve(self, request, short_url):
        link = Link.objects.filter(short_url=short_url).first()
        if link:
            serializer = self.get_serializer(link)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Ссылка не найдена'}, status=status.HTTP_404_NOT_FOUND)
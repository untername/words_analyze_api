from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from typing import Any, Dict, Set
from .serializers import WordSerializer
from .models import Analyzer
from .handlers import text_handler


class HomeView(ModelViewSet):

    """
    ViewSet-класс с переопределенным методом create(). Сохраняет вводные данные, но не отображает их.
    Но впоследствии, например, можно изучить, на что больший спрос, и развивать это.

    В ответ отправляется лишь респонс.
    """

    queryset = Analyzer.objects.none()
    serializer_class = WordSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)

            method: Set[str] = serializer.data.get('method')
            text: str = serializer.data.get('text')
            analyzed: Dict = text_handler(method, text)
            headers = self.get_success_headers(serializer.data)

            return Response(
                data={"query": serializer.data, "data": analyzed},
                status=status.HTTP_202_ACCEPTED, headers=headers)

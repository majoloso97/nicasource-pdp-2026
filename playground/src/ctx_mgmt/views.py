from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from .workflows.context_assistant import (
    ChatRequest,
    context_assistant_workflow,
    seed_fake_data,
)
from .workflows.joke import State, optimizer_workflow


class HelloWorldView(APIView):
    def post(self, request):
        ser = State.drf_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        state = optimizer_workflow.invoke(ser.validated_data)
        return Response({"joke": state["joke"]}, status=HTTP_200_OK)


class ContextAssistantChatView(APIView):
    def post(self, request):
        ser = ChatRequest.drf_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        state = context_assistant_workflow.invoke(ser.validated_data)
        return Response(
            {
                "conversation_id": state["conversation_pk"],
                "response": state["response"],
                "debug": state["debug_info"],
            },
            status=HTTP_200_OK,
        )


class ContextAssistantSeedView(APIView):
    def post(self, request):
        seed_fake_data()
        return Response({"ok": True}, status=HTTP_200_OK)

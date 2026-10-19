from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import AIInvestigation
from .chat_models import ChatMessage
from .serializers import AIInvestigationSerializer
from ai.providers.openai import OpenAIProvider
from platform.permissions.permissions import IsOrganizationMember

class AIInvestigationChatViewSet(viewsets.GenericViewSet):
    """
    Handles the interactive chat for a specific AI investigation.
    """
    queryset = AIInvestigation.objects.all()
    serializer_class = AIInvestigationSerializer
    permission_classes = [IsOrganizationMember]

    @action(detail=True, methods=['post'])
    def chat(self, request, pk=None):
        investigation = self.get_object()
        user_message = request.data.get('message')

        if not user_message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Store User Message
        ChatMessage.objects.create(
            investigation=investigation,
            user=request.user,
            role='user',
            content=user_message
        )

        # 2. Build Contextual Prompt (Retrieving last 5 messages)
        history = ChatMessage.objects.filter(investigation=investigation).order_by('-timestamp')[:5]
        context_string = "\n".join([f"{m.role}: {m.content}" for m in reversed(history)])

        # 3. Get AI Response
        provider = OpenAIProvider()
        prompt = f"Context of investigation: {investigation.incident.title}\nHistory:\n{context_string}\nUser: {user_message}\nAI:"
        ai_response = provider.generate(prompt, system_prompt="You are the OpsPilot AI Assistant. Help the SRE debug this incident.")

        # 4. Store AI Response
        ChatMessage.objects.create(
            investigation=investigation,
            user=request.user, # AI as user for simplicity in model
            role='assistant',
            content=ai_response
        )

        return Response({"response": ai_response})

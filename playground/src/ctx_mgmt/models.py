import uuid

from django.db import models

from pgvector.django import VectorField


class Client(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.slug


class Document(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="documents"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("client", "title")]

    def __str__(self) -> str:
        return f"{self.client.slug}:{self.title}"


class DocumentChunk(models.Model):
    """Chunked document content with an embedding for simple RAG."""

    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="chunks"
    )

    idx = models.PositiveIntegerField()

    content = models.TextField()

    token_estimate = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    embedding = VectorField(dimensions=1536, null=True, blank=True)

    class Meta:
        unique_together = [("document", "idx")]


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="conversations"
    )

    running_summary = models.TextField(blank=True, default="")

    summary_updated_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.client.slug}:{self.id}"


class Message(models.Model):
    class Role(models.TextChoices):
        SYSTEM = "system", "system"
        USER = "user", "user"
        ASSISTANT = "assistant", "assistant"

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(max_length=16, choices=Role.choices)
    content = models.TextField()
    token_estimate = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["conversation", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.conversation_id}:{self.role}"

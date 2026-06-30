from ctx_mgmt.models import Client, Document

from .services import ensure_document_chunks


def seed_fake_data() -> None:
    client_a, _ = Client.objects.get_or_create(
        slug="client_a", defaults={"name": "Client A"}
    )
    client_b, _ = Client.objects.get_or_create(
        slug="client_b", defaults={"name": "Client B"}
    )

    docs_a = {
        "architecture.md": "Client A architecture: Django monolith on ECS Fargate. Analytics uses Athena + QuickSight. Data lands in S3.",
        "deployment.md": "Client A deployment: Docker images built in CI, pushed to ECR, deployed to ECS Fargate. Infra via Terraform.",
        "analytics.md": "Client A analytics: Athena queries over S3 data lake; QuickSight dashboards for reporting.",
    }
    docs_b = {
        "frontend.md": "Client B frontend: Next.js deployed on Vercel. Uses edge caching and incremental static regeneration.",
        "auth.md": "Client B auth: Supabase Auth with magic links and JWT-based sessions.",
        "infra.md": "Client B infra: Vercel for web, Supabase for Postgres + auth; no AWS ECS usage.",
    }

    for title, content in docs_a.items():
        doc, _ = Document.objects.get_or_create(
            client=client_a, title=title, defaults={"content": content}
        )
        if doc.content != content:
            doc.content = content
            doc.save(update_fields=["content", "updated_at"])
        ensure_document_chunks(doc)

    for title, content in docs_b.items():
        doc, _ = Document.objects.get_or_create(
            client=client_b, title=title, defaults={"content": content}
        )
        if doc.content != content:
            doc.content = content
            doc.save(update_fields=["content", "updated_at"])
        ensure_document_chunks(doc)

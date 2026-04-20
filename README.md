# Nicasource PDP 2026

## About

This is a repository for the Nicasource PDP 2026. It's intended to contain evidences to the work being done, collect resources and journal entries following the learning process.

If code snippets are used, they'll also be contained here.

## Learning path
My learning path for 2025, in the context of Nicasource AI strategy, focuses on building the ability to design and implement AI features that work reliably within real systems, rather than treating AI as a standalone or self-contained tool. It emphasizes practical areas such as handling context, preparing data, evaluating outputs, and ensuring quality, which are often the main challenges when applying AI in production.

My overall goal is to develop a more structured approach to using AI so that it delivers consistent value while fitting within existing technical and business constraints. Rather than following a fixed set of resources, I intend to treat any materials as starting points for deeper exploration. In some cases, those entry points may not be defined upfront, since part of the process is to discover what to learn next through exploration itself, keeping the focus on continuous research driven by curiosity.

There are 4 concrete goals to be tackled:
### Understand AI System Architecture Patterns
Develop a clear understanding of the main architectural approaches for AI systems (prompt-based, RAG, tool calling, agents), including their tradeoffs and appropriate use cases. Focus on selecting the simplest effective pattern based on problem constraints. Resources: DeepLearning.AI – Building Systems with the ChatGPT API OpenAI Cookbook (RAG + tool usage sections) LangChain conceptual docs (architecture overviews only)

### Design Context Management Strategies
Learn how to structure, select, and optimize context provided to LLMs, including retrieval, summarization, and multi-step context flows. Emphasis is placed on tradeoffs between relevance, cost, and performance at scale. Resources: Anthropic prompting & context guides “Lost in the Middle” paper (Liu et al.) OpenAI Cookbook (context + prompt design sections)

### Design AI-Ready Data Pipelines
Understand how to prepare and structure application data for AI usage, including preprocessing, filtering, and defining what data is suitable for retrieval or inference. This includes designing lightweight pipelines and defining “AI-ready” datasets. Resources: LlamaIndex conceptual docs (data ingestion & indexing) Pinecone learning/blog content on data preparation & retrieval

### Implement Evaluation and Quality Assurance Mechanisms
Develop approaches to evaluate AI system outputs using structured criteria, including correctness, grounding, and consistency. Focus on defining simple evaluation datasets and validation mechanisms to ensure reliable behavior. Resources: OpenAI evals documentation & examples DeepLearning.AI – Evaluating and Debugging Generative AI (short course) Designing Machine Learning Systems (evaluation & iteration concepts)

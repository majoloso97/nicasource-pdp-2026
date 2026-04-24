---
date: 2026-04-20
objectives: 
    - define learning materials
    - create progress tracking artifacts (repo, drive)
---

### Main tasks
- Create repo to contain journal entries, learning plans, ai generated summaries, code snippets, etc
- Generate overview summary of AI architectural patterns with AI-powered research tools
- Polish collection of sources to use as learning guide


### Journal
There's a diverse array of AI usage strategies and architecture patterns, and there's no standardized way to use the LLMs with traditional software.

At first glance, the ecosystem feels often changing, with new state-of-art tools and strategies coming out frequently. This changing environment makes finding sources that contrast the main strategies harder due to lack of concensus.

However, there are some strategies that seem to be very robust and foundational, so that newer methodologies are often new perspectives over the same foundational idea. For example: agents build over the idea of simple tool calling, RAG pipelines are a more effective strategy for context building over manual context provisioning, etc. That's not to say that newer strategies are simple, on the contrary, the simplicity of the core ideas seem to quickly increase in complexity as bigger problems are tackled. Thus, the question of 'what tool is better for this problem' still has a lot of value, specially in business contexts that are new to using AI tools and processes.


---
date: 2026-04-22
objectives: 
    - build a mental map of knowns, gaps, and unknowns
---

### Main tasks
    - Read through ai-generated summaries
    - Detect topics with least knowledge/more questions to focus on later
    - Explore ai provided sources on less known topics


### Journal
Original perception of AI integration techniques was overall accurate though with some details: After no-AI, the simplest systems are prompt based, single turn, bound to provided context. Most prone to hallucinate, most 'unstructured'. 

Then, tool calling and RAG techniques are the next step in complexity, but also in controlling context and behavior under more structured constraints: the LLM can do what the tools allow, and/or the LLM will use what the RAG returns. 

Seems the authors tend to layer tool calling over RAG in terms of complexity, as if, in an evolutionary sense, RAG comes first, and then tool calling evolves as a next step. To me, it feels like they're equally relevant techniques for two diverging purposes: Provide more accurate context (all RAG flavors are variations that specialize in optimizing for a specific purpose) and make the AI an active piece of the systems it works with ('an model is as good as the tools you give it').

It's interesting to see that there are LOTS of specialized techniques in each layer of these AI-systems integration: prompt engineering caveats and opinionated techniques, several mainstream RAG flavors, and the ability to create whatever tool its relevant for a context and make it available to the LLM for execution. It feels overwhelming at first, and I think is a domain where the generalistic approach to learning works best: knowing what's out there, pick a couple things to dig into, and be open to change.

Finally, the topmost layer of complexity are the so called agent loops. Personally, it feels this is where the most promising use cases appear, but where there's the least standardization on, and where it gets really easy to get lost in. Topics get mixed around: Agentic RAG is an interesting one: it's a RAG technique, but it loops over using tools to increase the accuracy of the retrieved context. 

I find super relevant that the higher we climb on these complexity layers, the less deterministic the systems are, the more relevant orchestration becomes (against 'correctness' of the code) and the system reliability paradigm changes towards guardrails and oversight.


date: 2026-04-24
objectives: 
    - finish DLAI course: Building Systems with the ChatGPT API
---

### Main tasks
    - Complete short course


### Journal
Going through this introductory course, I notice that the most basic form of 'control' over the LLM behavior is mostly guidelines, constraints, and post-execution evaluations. Interesting that regardless of the provider, it all comes down to gathering inputs, controling the flow of those inputs to the context so that the context is properly managed and then orchestration: handling usual system errors (network failure, rate limits, etc) + all the control layer of what to do when the LLM does something it's not supposed to do.

Taking that complexity out (which really is most of the job) the usual loop of generation for the simplest LLM integration in a chat, considering some sort of in-loop sanitization/evaluation is:
```
    prepare_system_prompt
    loop starts
        receive input
        sanitize input
        send input to LLM
        receive output
        evaluate output
        return output
    repeat
    
```

Steps of RAG or tools can be added in the loop for these types of user-driven interactions

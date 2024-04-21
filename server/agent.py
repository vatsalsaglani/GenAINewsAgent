from llms.groq import GroqLLMStream
from configs import GROQ_API_KEY, GROQ_MODEL_NAME
from news import getNews
from prompts import SYSTEM_PROMPT

llm = GroqLLMStream(GROQ_API_KEY)


async def newsAgent(query: str):
    retrieved_news_items = await getNews(query)
    # print(retrieved_news_items)
    if not retrieved_news_items:
        yield "\n_Cannot fetch any relevant news related to the search query._"
        return
    retrieved_news_items = retrieved_news_items.get("results")
    useful_meta_keys = [
        "title", "link", "keywords", "creator", "description", "country",
        "category"
    ]
    news_items = [{
        k: d[k]
        for k in useful_meta_keys
    } for d in retrieved_news_items]
    messages = [{
        "role": "user",
        "content": f"Query: {query}\n\nNews Items: {news_items}"
    }]
    async for chunk in llm(GROQ_MODEL_NAME,
                           messages,
                           system=SYSTEM_PROMPT,
                           max_tokens=1024,
                           temperature=0.2):
        yield chunk

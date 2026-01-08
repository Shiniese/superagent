import argparse
import asyncio
from dotenv import load_dotenv
import os
from io import BytesIO

import zendriver as zd
from ddgs import DDGS
from readability import Document
from markitdown import MarkItDown

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_ollama import OllamaEmbeddings

load_dotenv()

# Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

model_embedding = OllamaEmbeddings(
    model="qwen3-embedding:0.6b-q8_0", 
    base_url=OLLAMA_BASE_URL
)


def get_search_urls(query: str) -> list[str]:
    """
    根据给定的查询词，从多个搜索引擎（Google、Bing、DuckDuckGo）获取搜索结果的URL列表。

    功能：
        该函数使用 DDGS（DuckDuckGo Search）库执行搜索，并返回搜索结果中前10个结果的链接。

    参数：
        query (str): 要搜索的查询字符串，必须是有效的文本内容。

    返回：
        list[str]: 包含搜索结果URL的字符串列表。如果未找到结果或发生错误，将返回空列表。若底层搜索失败，则抛出异常。

    示例：
        urls = get_search_urls("Python编程教程")
        for url in urls:
            print(url)
    """

    params = {
        "region": "us-en",
        "safesearch": "moderate",
        "timelimit": None, 
        "max_results": 10,  
        "page": 1, 
        "backend": "google, bing, duckduckgo", 
    }
    
    try:
        results = DDGS().text(query, **params)
        return [item["href"] for item in results]

    except Exception as e:
        raise Exception(f"Error getting search urls: {str(e)}")
    
def RAG(query: str, markdown_text: str) -> list[object]:
    """
    执行基于 Markdown 文档的检索增强生成（RAG）查询。

    功能：
        query → 分割标题片段 → 嵌入向量 → 存入内存数据库 → MMR检索 → 返回匹配片段（含标题与内容）。

    参数：
        query (str): 用户提出的自然语言查询，用于检索相关文档内容。
        markdown_text (str): 一段结构化的 Markdown 文本，包含标题和段落，用于作为知识源。

    返回值：
        list[object]: 一个包含多个文档片段的列表，每个片段是包含标题和内容的字典或对象，具体结构取决于 langchain 的输出格式。

    示例使用：
        result = RAG("什么是机器学习？", "# xxx")
        for item in result:
            print(item.page_content)
    """

    try:
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
        ]

        # MD splits
        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on, strip_headers=False
        )
        md_header_splits = markdown_splitter.split_text(markdown_text)

        vectorstore = InMemoryVectorStore.from_documents(documents=md_header_splits, embedding=model_embedding)
        retriever = vectorstore.as_retriever(
            search_type="mmr", 
            search_kwargs={
                "k": 10, 
                "lambda_mult": 0.25
            }
        )
        return retriever.invoke(query)

    except Exception as e:
        raise Exception(f"Error RAG searching: {str(e)}")
    

async def fetch_page_content(browser, url):
    """
    从指定URL的网页中提取标题和可读内容。

    功能说明:
        打开网页 → 等待加载 → 提取正文 → 用Readability解析 → 转为Markdown并提取文本 → 异常则返回默认值 → 关闭标签页。

    参数:
        browser (Browser): 浏览器实例，用于打开新标签页并操作网页。
        url (str): 要抓取的网页URL地址。

    返回:
        tuple: 包含三个元素的元组：
            - title (str): 页面标题，若提取失败则返回 "NO_TITLE"。
            - url (str): 原始URL，用于标识来源。
            - content (str): 提取后的文章正文内容，以纯文本形式呈现；若提取失败则返回 "NO_CONTENT"。

    示例:
        result = await fetch_page_content(browser, "https://example.com/article")
        title, url, content = result
        print(f"标题: {title}")
        print(f"内容: {content}")
    """

    try:
        tab = await browser.get(url, new_tab=True)
        await tab.sleep(10)
        await tab.select('body')
        content = await tab.get_content()

        # 使用 Readability-lxml 提取文章内容
        doc = Document(content)
        title = doc.title()
        content = MarkItDown().convert(BytesIO(doc.summary().encode('utf-8'))).text_content

        await tab.close()  # 可选：立即关闭 tab，节省资源
        return title, url, content
    except Exception as e:
        return "NO_TITLE", url, "NO_CONTENT"
    
async def web_search(english_query: str) -> list[str]:
    """
    一个使代理能够基于用户查询进行网络搜索的工具，可快速访问最新的在线信息。
    你必须首先理解我的问题，然后重构成英文关键词来调用此工具。

    Args:
        english_query: English reconstructed keywords derived from my question.
    """

    try:
        search_urls = get_search_urls(english_query)
        browser = await zd.start(
            headless=True,
            browser_args=[
                "--disable-images",
                "--disable-fonts",
                "--disable-features=TranslateUI",
                "--disable-features=Translate"
            ]
        )
        # 并发获取所有页面内容
        tasks = [fetch_page_content(browser, url) for url in search_urls]
        results = await asyncio.gather(*tasks)

        # 打印结果
        md_texts = ""
        for title, url, content in results:
            if title == "NO_TITLE" or len(content) < 500:
                continue
            md_texts += f"# {title}\n\n{content}\n\n"
            print(f"✅ Fetched 「{title}」 {url}: {len(content)} characters")
    
        rag_results = RAG(query=english_query, markdown_text=md_texts)
        rag_results = [rag_result.page_content for rag_result in rag_results]
        return rag_results
    
    except Exception as e:
        print(f"Error web searching: {str(e)}")
        return f"Error web searching: {str(e)}"
    
    finally:
        await browser.stop()

# 主函数：处理命令行参数并执行搜索
async def main():
    parser = argparse.ArgumentParser(description="Run web search using RAG and browser.")
    parser.add_argument("query", type=str, help="The search query (e.g., 'what is AI')")
    args = parser.parse_args()

    # 执行搜索
    results = await web_search(args.query)
    print(results)

# 作为入口点运行
if __name__ == "__main__":
    try:
        asyncio.run(main())

    except Exception as e:
        print(f"❌ Unexpected error: {e}")

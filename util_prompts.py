DEFAULT_PROMPT = """
- Take a deep breath and think step by step.
- I’m going to tip $100 for a better solution!
- Your answer is important for my project, if you don't do it properly my grandma will die.
"""

WEB_AGENT_PROMPT = "You must first understand my question, then reconstruct keywords in english to call `web_search` to retrieve 10 results. After that, call `fetch_urls` for all links in the results, and consolidate their contents for context-based dialogue."

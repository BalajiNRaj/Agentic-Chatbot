from langchain_core.prompts import ChatPromptTemplate
from tavily import TavilyClient
from langchain_core.messages import HumanMessage, SystemMessage


class AiNews:
    def __init__(self, llm):
        """
            Initializes the AI News Node with API Keys of Tavily Client
        """

        self.tavily = TavilyClient()
        self.llm = llm
        self.state = {}

    def fetch_news(self, state: dict) -> dict:
        """
         Fetch AI News based on the specified frequency

         Args: 
            state(dict): The state dictionary containing frequency

        Returns:
            dict: Update the state with 'news_date' key containing fetched news.
        """ 

        freq = state['messages'][0].content.lower()
        self.state['frequency'] = freq
        days_map = {'daily': 1, 'weekly': 7, 'monthly': 30, 'year': 365}
        time_range_map = {'daily': 'd', 'weekly': 'm', 'monthly': 'm', 'year': 'y'}

        response = self.tavily.search(
            query="Top Artificial Intelligence (AI) technology news India and globally",
            topic="news",
            time_range=time_range_map[freq],
            include_answer="advanced",
            max_results=15,
            days=days_map[freq]
        )

        state['news_data'] = response.get('results', [])
        self.state['news_data'] = state['news_data']
        return state
    

    def summarize(self, state: dict) -> dict:
        """
        Summarizes the new data to particular format
        Args:
            state(dict): The state dictionary containing 'news_data'
        
        Returns:
            dict: Updated state with 'summary' key containing the summarized news.
        """

        news_items = self.state['news_data']

        prompt_tempalte = ChatPromptTemplate.from_messages([
            ("system", """
                Summarize the AI News articles into Markdown format. For each item include:
                - Date in **YYYY-MM-DD** format in IST timezone
                - Concise sentences summary from latest news
                - Sort news by date wise (lastest first)
                - Source URL as link

                Use Format:
                    ### [Date]
                    - [Summary] (URL)
            """),
            ("user", """
                Articles: \n {articles}
            """)
        ])

        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')} \n URL: {item.get('url', '')} \n {item.get('published_date', '')}"
            for item in news_items
        ])

        # print(f"news_items : {news_items}\n\n")

        response = self.llm.invoke(prompt_tempalte.format(articles=articles_str))
        state['summary'] = response.content
        self.state['summary'] = state['summary']
        
        # print(f"Summary : {state['summary']}\n\n")

        return {'messages': self.state['summary']}
    
    def save_results(self, state: dict) -> dict:
        return self.state
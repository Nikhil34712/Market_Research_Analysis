from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search.tool import TavilySearchResults
import os
import markdown
from datetime import datetime

class MarketResearchSystem:
    def __init__(self, company: str, industry: str, openai_api_key: str, tavily_api_key: str):
        os.environ["OPENAI_API_KEY"] = openai_api_key
        os.environ["TAVILY_API_KEY"] = tavily_api_key
        
        self.company = company
        self.industry = industry
        
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7,
            max_tokens=4000
        )
        
        self.search_tool = TavilySearchResults(
            tavily_api_key=tavily_api_key,
            max_results=5,
            search_depth="advanced"
        )

    def create_agents(self):
        resource_specialist = Agent(
            role='AI Implementation Resource Specialist',
            goal=f'Find practical AI implementation resources for {self.company}',
            backstory=f"""Expert in identifying practical AI implementation resources and use cases.
            Deep knowledge of {self.industry} industry and technical requirements.
            Specializes in finding real-world examples, implementations, and relevant datasets.""",
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True
        )

        return [resource_specialist]

    def create_tasks(self, agents):
        resource_specialist = agents[0]

        resources = Task(
            description=f"""Create a comprehensive AI implementation resource guide for {self.company}.

YOUR TASK:
Generate 4 practical AI use cases with implementation resources and datasets specifically tailored for {self.company}.

FORMAT YOUR RESPONSE IN A MARKDOWN TABLE EXACTLY LIKE THIS:

| Use Case | Description | Implementation Resources | Datasets & Code |
|----------|-------------|-------------------------|-----------------|
| [Use Case Name] | [2-3 sentences describing what problem this solves and its concrete benefits] | • [Resource Name](URL) - Brief description<br>• [Resource Name](URL) - Brief description | • [Dataset Name](Kaggle/GitHub URL) - Dataset description<br>• [Code Repository](GitHub URL) - Implementation details |

REQUIRED USE CASES:
1. One focused on {self.company}'s core business operations
2. One focused on customer experience enhancement
3. One focused on operational efficiency
4. One focused on innovation/R&D

EXAMPLE FORMAT:
| Use Case | Description | Implementation Resources | Datasets & Code |
|----------|-------------|-------------------------|-----------------|
| Predictive Maintenance | Enables early detection of potential equipment failures through real-time sensor data analysis. This proactive approach reduces downtime, extends equipment life, and optimizes maintenance schedules. | • [NVIDIA AI-Powered Maintenance](https://developer.nvidia.com/blog/example) - Implementation guide<br>• [AWS Implementation](https://aws.com/example) - Cloud deployment guide | • [Industrial Maintenance Dataset](https://www.kaggle.com/datasets/example) - 10GB of sensor data<br>• [Maintenance ML Models](https://github.com/example/maintenance) - Python implementation |

REQUIREMENTS:
1. Make each use case highly specific to {self.company}'s industry and needs
2. Focus on practical, implementable solutions
3. Provide real, accessible resources (Kaggle/GitHub/HuggingFace)
4. Include both implementation resources and datasets/code
5. Keep descriptions natural and benefits concrete
6. Ensure URLs are valid and resources are relevant

GENERATE FOUR USE CASES NOW IN THE EXACT TABLE FORMAT SPECIFIED ABOVE.""",
            agent=resource_specialist,
            expected_output="AI implementation resources table with four specific use cases, implementation guides, and datasets"
        )

        return [resources]

    def run(self):
        try:
            print(f"\nAnalyzing {self.company} in {self.industry}...")
            
            agents = self.create_agents()
            tasks = self.create_tasks(agents)
            
            crew = Crew(
                agents=agents,
                tasks=tasks,
                process=Process.sequential,
                verbose=2
            )
            
            results = crew.kickoff()
            
            if not results or not str(results).strip():
                raise Exception("No results generated")
            
            report = f"""# AI Implementation Analysis for {self.company}
Generated on: {datetime.now().strftime("%Y-%m-%d")}

## Overview
This analysis provides implementation resources for {self.company}'s AI initiatives across different use cases, along with relevant datasets and implementation resources.

{str(results)}"""
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/{self.company.lower()}_{timestamp}"
            os.makedirs("reports", exist_ok=True)
            
            md_file = f"{filename}.md"
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(report)
            
            html_content = markdown.markdown(
                report,
                extensions=['tables', 'nl2br']
            )
            
            html_file = f"{filename}.html"
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <style>
                        body {{ 
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            max-width: 1200px;
                            margin: 0 auto;
                            padding: 20px;
                        }}
                        table {{ 
                            border-collapse: collapse;
                            width: 100%;
                            margin: 20px 0;
                        }}
                        th, td {{
                            border: 1px solid #ddd;
                            padding: 12px;
                            text-align: left;
                        }}
                        th {{
                            background-color: #f5f5f5;
                        }}
                        tr:nth-child(even) {{
                            background-color: #f9f9f9;
                        }}
                    </style>
                </head>
                <body>
                {html_content}
                </body>
                </html>
                """)
            
            return report, md_file, html_file

        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            return None, None, None
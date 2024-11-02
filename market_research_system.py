from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search.tool import TavilySearchResults
import os
import markdown
from datetime import datetime

# Core class that manages the market research system using multiple agents
class MarketResearchSystem:
    def __init__(self, company: str, industry: str, openai_api_key: str, tavily_api_key: str):
        # Initialize environment variables for API access
        os.environ["OPENAI_API_KEY"] = openai_api_key
        os.environ["TAVILY_API_KEY"] = tavily_api_key
        
        self.company = company
        self.industry = industry
        
        # Initialize GPT-4 as the base LLM for agents
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7,
            max_tokens=4000
        )
        
        # Initialize Tavily search tool for web research
        self.search_tool = TavilySearchResults(
            tavily_api_key=tavily_api_key,
            max_results=8,
            search_depth="advanced"
        )

    # Create four specialized agents for different aspects of research
    def create_agents(self):
        # Agent 1: Research Analyst - Identifies AI use cases
        research_analyst = Agent(
            role='Research Analyst',
            goal=f'Identify optimal AI use cases for {self.company}',
            backstory=f"""Senior industry analyst specializing in {self.industry}...""",
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True
        )

        # Agent 2: Technical Architect - Finds implementation resources
        tech_architect = Agent(
            role='Technical Architect',
            goal=f'Find official {self.company} implementation resources',
            backstory=f"""Senior technical architect...""",
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True
        )

        # Agent 3: Data Specialist - Finds relevant datasets and code
        data_specialist = Agent(
            role='Data & Training Specialist',
            goal=f'Find relevant datasets and code for {self.company} use cases',
            backstory="""Data scientist specializing...""",
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True
        )

        # Agent 4: Integration Specialist - Creates final documentation
        integration_specialist = Agent(
            role='Integration Specialist',
            goal='Create comprehensive implementation table with all use cases',
            backstory="""Technical documentation expert...""",
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True
        )

        return [research_analyst, tech_architect, data_specialist, integration_specialist]

    # Create sequential tasks for each agent
    def create_tasks(self, agents):
        research_analyst, tech_architect, data_specialist, integration_specialist = agents

        # Task 1: Identify use cases (Research Analyst)
        identify_use_cases = Task(
            description="""Identify EXACTLY 4 high-impact AI use cases...""",
            agent=research_analyst
        )

        # Task 2: Find implementation resources (Technical Architect)
        define_implementation = Task(
            description="""Find OFFICIAL company RESOURCES...""",
            agent=tech_architect
        )

        # Task 3: Find datasets and code (Data Specialist)
        find_datasets = Task(
            description="""Find REAL DATASETS AND CODE...""",
            agent=data_specialist
        )

        # Task 4: Create final output table (Integration Specialist)
        create_final_output = Task(
            description="""Create ONE TABLE combining ALL FINDINGS...""",
            agent=integration_specialist
        )

        return [identify_use_cases, define_implementation, find_datasets, create_final_output]

    # Main execution method
    def run(self):
        try:
            # Create agents and tasks
            agents = self.create_agents()
            tasks = self.create_tasks(agents)
            
            # Initialize crew with sequential process
            crew = Crew(
                agents=agents,
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            # Execute tasks and generate reports
            results = crew.kickoff()
            
            # Generate formatted reports in MD and HTML
            # [Report generation code...]
            
        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            return None, None, None
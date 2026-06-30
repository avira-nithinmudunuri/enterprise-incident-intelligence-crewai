import os


from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	FileReadTool,
	JSONSearchTool,
	TXTSearchTool,
	CSVSearchTool,
	ExaSearchTool,
	ContextualAIQueryTool,
	PDFSearchTool,
	WebsiteSearchTool
)

EMBEDDING_CONFIG = {
	"embedding_model": {
		"provider": "google-generativeai",
		"config": {
			"model_name": "gemini-embedding-001",
		},
	},
}

DEFAULT_MODEL = os.getenv("MODEL", "google/gemini-2.5-flash")


def _default_llm() -> LLM:
	return LLM(model=DEFAULT_MODEL)


def _contextual_ai_tool() -> ContextualAIQueryTool | None:
	api_key = os.getenv("CONTEXTUAL_AI_API_KEY")
	if not api_key:
		return None
	return ContextualAIQueryTool(api_key=api_key)


def _exa_tool() -> ExaSearchTool | None:
	if not os.getenv("EXA_API_KEY"):
		return None
	return ExaSearchTool()


DATA_DIR = "data"


@CrewBase
class EnterpriseIncidentIntelligenceResolutionSystemCrew:
    """EnterpriseIncidentIntelligenceResolutionSystem crew"""

    
    @agent
    def senior_it_incident_triage_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["senior_it_incident_triage_specialist"],
            
            
            tools=[				FileReadTool(),
				JSONSearchTool(
					json_path=f"{DATA_DIR}/incident_snapshot.json",
					config=EMBEDDING_CONFIG,
				)],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=_default_llm(),
            
        )
        
    
    @agent
    def enterprise_log_analysis_and_anomaly_detection_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["enterprise_log_analysis_and_anomaly_detection_engineer"],
            
            
            tools=[				FileReadTool(),
				TXTSearchTool(txt=f"{DATA_DIR}/application_logs.txt", config=EMBEDDING_CONFIG),
				CSVSearchTool(csv=f"{DATA_DIR}/error_metrics.csv", config=EMBEDDING_CONFIG),
				JSONSearchTool(
					json_path=f"{DATA_DIR}/incident_snapshot.json",
					config=EMBEDDING_CONFIG,
				)],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=_default_llm(),
            
        )
        
    
    @agent
    def enterprise_knowledge_base_and_runbook_retrieval_specialist(self) -> Agent:
        tools = [
				PDFSearchTool(config=EMBEDDING_CONFIG),
				WebsiteSearchTool(config=EMBEDDING_CONFIG)]
        exa_tool = _exa_tool()
        if exa_tool:
            tools.insert(0, exa_tool)
        contextual_tool = _contextual_ai_tool()
        if contextual_tool:
            tools.insert(1, contextual_tool)

        return Agent(
            config=self.agents_config["enterprise_knowledge_base_and_runbook_retrieval_specialist"],
            
            
            tools=tools,
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=_default_llm(),
            
        )
        
    
    @agent
    def principal_root_cause_analysis_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["principal_root_cause_analysis_engineer"],
            
            
            tools=[				JSONSearchTool(
					json_path=f"{DATA_DIR}/incident_snapshot.json",
					config=EMBEDDING_CONFIG,
				)],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=_default_llm(),
            
        )
        
    
    @agent
    def enterprise_remediation_and_resilience_architect(self) -> Agent:
        tools = [WebsiteSearchTool(config=EMBEDDING_CONFIG)]
        exa_tool = _exa_tool()
        if exa_tool:
            tools.insert(0, exa_tool)

        return Agent(
            config=self.agents_config["enterprise_remediation_and_resilience_architect"],
            
            
            tools=tools,
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=_default_llm(),
            
        )
        
    
    @agent
    def enterprise_incident_communications_and_reporting_director(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["enterprise_incident_communications_and_reporting_director"],
            
            
            tools=[				FileReadTool()],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=_default_llm(),
            
        )
        
    

    
    @task
    def incident_triage(self) -> Task:
        return Task(
            config=self.tasks_config["incident_triage"],
            markdown=False,
            
            
        )
    
    @task
    def log_analysis_and_anomaly_detection(self) -> Task:
        return Task(
            config=self.tasks_config["log_analysis_and_anomaly_detection"],
            markdown=False,
            
            
        )
    
    @task
    def knowledge_retrieval_and_runbook_search(self) -> Task:
        return Task(
            config=self.tasks_config["knowledge_retrieval_and_runbook_search"],
            markdown=False,
            
            
        )
    
    @task
    def root_cause_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["root_cause_analysis"],
            markdown=False,
            
            
        )
    
    @task
    def solution_recommendation_and_remediation_plan(self) -> Task:
        return Task(
            config=self.tasks_config["solution_recommendation_and_remediation_plan"],
            markdown=False,
            
            
        )
    
    @task
    def executive_incident_report(self) -> Task:
        return Task(
            config=self.tasks_config["executive_incident_report"],
            markdown=True,
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the EnterpriseIncidentIntelligenceResolutionSystem crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,

            chat_llm=_default_llm(),
        )


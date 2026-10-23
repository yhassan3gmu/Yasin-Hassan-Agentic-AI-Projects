# agentic_workflow.py

# TODO: 1 - Import the following agents: ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent from the workflow_agents.base_agents module
from workflow_agents.base_agents import ActionPlanningAgent
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent
from workflow_agents.base_agents import EvaluationAgent
from workflow_agents.base_agents import RoutingAgent

import os
print(f"current directory: {os.getcwd()}")
from dotenv import load_dotenv
load_dotenv()

# TODO: 2 - Load the OpenAI key into a variable called openai_api_key
openai_api_key = os.getenv("OPENAI_API_KEY")

# load the product spec
# TODO: 3 - Load the product spec document Product-Spec-Email-Router.txt into a variable called product_spec
with open('starter/phase_2/'+ 'Product-Spec-Email-Router.txt', 'r') as file:
    product_spec = file.read()

# Instantiate all the agents


# Action Planning Agent
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)
# TODO: 4 - Instantiate an action_planning_agent using the 'knowledge_action_planning'
action_planning_agent = ActionPlanningAgent(openai_api_key, knowledge_action_planning)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    # TODO: 5 - Complete this knowledge string by appending the product_spec loaded in TODO 3
    f"{product_spec}"
)
# TODO: 6 - Instantiate a product_manager_knowledge_agent using 'persona_product_manager' and the completed 'knowledge_product_manager'
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_product_manager, knowledge_product_manager)

# Product Manager - Evaluation Agent
# TODO: 7 - Define the persona and evaluation criteria for a Product Manager evaluation agent and instantiate it as product_manager_evaluation_agent. This agent will evaluate the product_manager_knowledge_agent.
# The evaluation_criteria should specify the expected structure for user stories (e.g., "As a [type of user], I want [an action or feature] so that [benefit/value].").
persona_product_manager_evaluation_agent = "You are a product manager evaluation agent that evaluates the user stories of each product manager knowledge agents" #"You are an evaluation agent that checks the answers of other worker agents"
product_manager_evaluation_criteria = "The answer should be stories that follow the following structure: As a [type of user], I want [an action or feature] so that [benefit/value]."
max_interactions = 1
product_manager_evaluation_agent = EvaluationAgent(openai_api_key, persona_product_manager_evaluation_agent, product_manager_evaluation_criteria, product_manager_knowledge_agent, max_interactions)
# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining product features derived from user stories" #"You are a Program Manager, you are responsible for defining the features for a product." 
#knowledge_program_manager = ("Features of a product are defined by organizing similar user stories into cohesive groups."
#                            f"{product_spec}") #added product_spec
knowledge_program_manager = f'''
Create Email Router product features using this exact format for every feature:
Feature Name:
Description:
Key Functionality:
User Benefit:

Use only the Email Router product specification below:
{product_spec}
'''
# Instantiate a program_manager_knowledge_agent using 'persona_program_manager' and 'knowledge_program_manager'
# (This is a necessary step before TODO 8. Students should add the instantiation code here.)
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_program_manager, knowledge_program_manager)

# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are a program manager evaluation agent that checks the features of related user stories."

# TODO: 8 - Instantiate a program_manager_evaluation_agent using 'persona_program_manager_eval' and the evaluation criteria below.
#                      "The answer should be product features that follow the following structure: " \
#                      "Feature Name: A clear, concise title that identifies the capability\n" \
#                      "Description: A brief explanation of what the feature does and its purpose\n" \
#                      "Key Functionality: The specific capabilities or actions the feature provides\n" \
#                      "User Benefit: How this feature creates value for the user"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
persona_evaluation_criteria = ("The answer should be product features that follow the following structure: " \
                      "Feature Name: A clear, concise title that identifies the capability\n" \
                      "Description: A brief explanation of what the feature does and its purpose\n" \
                      "Key Functionality: The specific capabilities or actions the feature provides\n" \
                      "User Benefit: How this feature creates value for the user\n"   
                      f"{product_spec}") 
program_manager_evaluation_agent = EvaluationAgent(openai_api_key, persona_program_manager_eval, persona_evaluation_criteria, program_manager_knowledge_agent, max_interactions)

# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
#knowledge_dev_engineer = "Development tasks are defined by identifying what needs to be built to implement each user story."  
knowledge_dev_engineer = f'''
Development tasks must be based only on the Email Router product spec below.
Create implementation tasks for email ingestion, message classification,
RAG-based response generation, SME routing, monitoring dashboards,
manual override, privacy controls, and system configuration.

Product spec:
{product_spec}
'''
# Instantiate a development_engineer_knowledge_agent using 'persona_dev_engineer' and 'knowledge_dev_engineer'
# (This is a necessary step before TODO 9. Students should add the instantiation code here.)
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_dev_engineer, knowledge_dev_engineer)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are a persona development evaluation agent that checks the answers of each development engineer knowledge agent." #"You are an evaluation agent that checks the answers of other worker agents."
# TODO: 9 - Instantiate a development_engineer_evaluation_agent using 'persona_dev_engineer_eval' and the evaluation criteria below.
'''
persona_dev_engineer_evaluation_criteria = (
                      "The answer should be tasks following this exact structure: " \
                      "Task ID: A unique identifier for tracking purposes\n" \
                      "Task Title: Brief description of the specific development work\n" \
                      "Related User Story: Reference to the parent user story\n" \
                      "Description: Detailed explanation of the technical work required\n" \
                      "Acceptance Criteria: Specific requirements that must be met for completion\n" \
                      "Estimated Effort: Time or complexity estimation\n" \
                      "Dependencies: Any tasks that must be completed first")
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
'''

#persona_dev_engineer_evaluation_criteria = f'''
#Each engineering task must use this exact structure:
#Task ID:
#Task Title:
#Related User Story:
#Description:
#Acceptance Criteria:
#Estimated Effort:
#Dependencies:
#The tasks must be specifically about the Email Router product, not generic ecommerce, shopping cart, account creation, or search-platform features.
#'''
#development_engineer_evaluation_agent = EvaluationAgent(openai_api_key, persona_dev_engineer_eval, persona_dev_engineer_evaluation_criteria, development_engineer_knowledge_agent, max_interactions) 
# In phase_2/agentic_workflow.py, use a separate interaction count for the Dev Engineer evaluator
dev_engineer_max_interactions = 2

persona_dev_engineer_evaluation_criteria = '''
Every engineering task must use this exact structure, with no grouped component bullets:
Task ID: <unique ID such as ER-001>
Task Title: <brief engineering work item>
Related User Story: <copy or reference the Email Router user story>
Description: <technical implementation details>
Acceptance Criteria: <testable completion requirements>
Estimated Effort: <time or complexity estimate>
Dependencies: <required prior task or None>
All tasks must be specifically about the Email Router product.
'''

development_engineer_evaluation_agent = EvaluationAgent(
    openai_api_key,
    persona_dev_engineer_eval,
    persona_dev_engineer_evaluation_criteria,
    development_engineer_knowledge_agent,
    dev_engineer_max_interactions
)

# Routing Agent
# TODO: 10 - Instantiate a routing_agent. You will need to define a list of agent dictionaries (routes) for Product Manager, Program Manager, and Development Engineer. Each dictionary should contain 'name', 'description', and 'func' (linking to a support function). Assign this list to the routing_agent's 'agents' attribute.
routing_agent = RoutingAgent(openai_api_key, {})  

# Job function persona support functions
# TODO: 11 - Define the support functions for the routes of the routing agent (e.g., product_manager_support_function, program_manager_support_function, development_engineer_support_function).
# Each support function should:
#   1. Take the input query (e.g., a step from the action plan).
#   2. Get a response from the respective Knowledge Augmented Prompt Agent.
#   3. Have the response evaluated by the corresponding Evaluation Agent.
#   4. Return the final validated response.

def product_manager_support_function(input_query):
    #product_manager_response = product_manager_knowledge_agent.respond(input_query)
    product_evaluation = product_manager_evaluation_agent.evaluate(input_query)
    return product_evaluation["final response"]

def program_manager_support_function(input_query):
    #program_manager_response = program_manager_knowledge_agent.respond(input_query)
    program_evaluation = program_manager_evaluation_agent.evaluate(input_query)
    return program_evaluation["final response"]

def development_engineer_support_function(input_query):
    #development_engineer_response = development_engineer_knowledge_agent.respond(input_query)
    development_evaluation = development_engineer_evaluation_agent.evaluate(input_query)
    return development_evaluation["final response"]
    
    
agents = [
    {
        "name": "product manager evaluation agent", 
        "description": "Define the user stories for a product.",
        "func": lambda x: product_manager_support_function(x) 
    },
    {
        "name": "program manager evaluation agent",
        "description": "Convert approved user stories into product features by grouping related stories and defining each feature's name, description, key functionality, and user benefit. Use this only for feature definition, not for creating user stories and not for defining engineering tasks.",
        "func": lambda x: program_manager_support_function(x)  
    },
    {
        "name": "development engineer evaluation agent",
        "description": "Convert approved product features or user stories into engineering tasks, technical work items, and implementation deliverables. Use this only for development-task planning, not for user stories or feature definition.",     #"Define the development tasks for a product.",
        "func": lambda x: development_engineer_support_function(x)
    }
]
routing_agent.agents = agents

# Run the workflow

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
# ****
workflow_prompt = "Create a development plan for this product by first identifying user stories, then grouping them into product features, and finally defining engineering tasks."
#"What would the development tasks for this product be?"
# ****
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")
# TODO: 12 - Implement the workflow.
#   1. Use the 'action_planning_agent' to extract steps from the 'workflow_prompt'.
#   2. Initialize an empty list to store 'completed_steps'.
#   3. Loop through the extracted workflow steps:
#      a. For each step, use the 'routing_agent' to route the step to the appropriate support function.
#      b. Append the result to 'completed_steps'.
#      c. Print information about the step being executed and its result.
#   4. After the loop, print the final output of the workflow (the last completed step).
uncompleted_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
completed_steps = []
for step in uncompleted_steps:
    #print(f"Step: {step}")
    step_result = routing_agent.routing(step)
    completed_steps.append(step_result)
    print(f"Executed Step Result: {step_result}")
#print(f"Final Output of the workflow: {completed_steps[-1]}")
print(
    f"Final Output of the workflow:\n\n"
    f"User Stories:\n{completed_steps[0]}\n\n"
    f"Product Features:\n{completed_steps[1]}\n\n"
    f"Engineering Tasks:\n{completed_steps[2]}"
)


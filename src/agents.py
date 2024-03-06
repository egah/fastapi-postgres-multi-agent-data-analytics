from typing import Callable
import autogen

from . import orchestrator
from . import agents_config
from . import agents_instrument


# ------------ PROMPTS ------------


# create our terminate msg function
def is_termination_msg(content):
    have_content = content.get("content", None) is not None
    if have_content and "APPROVED" in content["content"]:
        return True
    return False


COMPLETION_PROMPT = "If everything looks good, respond with APPROVED"


# ------------ AGENTS ------------
def build_data_engineering_teem(
    instruments: agents_instrument.PostgresAgentInstruments,
):
    # create a set of agents with specific roles
    # admin user proxy agent - takes in the prompt and manages the group chat
    USER_PROXY_PROMPT = "A human admin. Interact with the Product Manager \
        to discuss the plan. Plan execution needs to be approved by this admin."
    user_proxy = autogen.UserProxyAgent(
        name="Admin",
        system_message=USER_PROXY_PROMPT,
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    # data engineer agent - generates the sql query
    DATA_ENGINEER_PROMPT = "A Data Engineer. Generate the initial SQL based on \
          the requirements provided. Send it to \
    the Sr Data Analyst to be executed. "
    data_engineer = autogen.AssistantAgent(
        name="Engineer",
        llm_config=agents_config.base_config,
        system_message=DATA_ENGINEER_PROMPT,
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    SR_DATA_ANALYST_PROMPT = (
        "Sr Data Analyst. You run the SQL query "
        "using the run_sql function, send the raw response to product manager."
        "You use the run_sql function exclusively."
    )

    sr_data_analyst = autogen.AssistantAgent(
        name="Sr_Data_Analyst",
        llm_config=agents_config.sr_data_analyst_config,
        system_message=SR_DATA_ANALYST_PROMPT,
        code_execution_config=False,
        human_input_mode="NEVER",
        function_map={
            "run_sql": instruments.run_sql,
        },
    )

    PRODUCT_MANAGER_PROMPT = (
        "Product Manager. Validate the response to make sure it's correct"
        + COMPLETION_PROMPT
    )
    # product manager - validate the response to make sure it's correct
    product_manager = autogen.AssistantAgent(
        name="Product_Manager",
        llm_config=agents_config.base_config,
        system_message=PRODUCT_MANAGER_PROMPT,
        code_execution_config=False,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    return [user_proxy, data_engineer, sr_data_analyst, product_manager]


# ------------ ORCHESTRATION ------------

# j'ai mon objet orchestrator qui permet de combiner notres team avec avec notre onjet instrument
# l'objet instrument contient les ?????
def combine_team_instruments_in_orchestrator(
    team: str,
    agent_instruments: agents_instrument.PostgresAgentInstruments,
    validate_results: Callable,
) -> orchestrator.Orchestrator:
    if team == "data_engineering_team":
        return orchestrator.Orchestrator(
            name="Postgres Data Analytics Multi-Agent ::: Data Engineering Team",
            agents=build_data_engineering_teem(agent_instruments),
            instruments=agent_instruments,
            validate_results_func=validate_results,
        )
    else:
        raise ValueError(f"Team {team} not found")

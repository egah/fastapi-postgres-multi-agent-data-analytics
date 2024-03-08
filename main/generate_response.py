import os
import sys
from pathlib import Path
import dotenv
import json
from src import llm
from src import agents

from src.utils import (
    ConversationResult,
    generate_session_id,
    DatabaseEmbedder
)
from src.agents_instrument import PostgresAgentInstruments


BASE_DIR = "/" + "/".join((Path(__file__).resolve().parent.parent.parts)[1:])
sys.path.append(BASE_DIR)

PROMPT_TABLES_DEFINITIONS = "TABLE_DEFINITIONS"


def generate_response(
    raw_prompt: str, 
    db_url: str,
    openai_api_key: str
):

    prompt = f"Fulfill this database query: {raw_prompt}. "
 
    # generer une session id pour chaque prompt
    session_id = generate_session_id(raw_prompt)

    """
    je mobilise avec le context manager l'objet datatabse(gere les requete sql) 
    et l'objet instrument (gère les attributs et des agents)
    """
    with PostgresAgentInstruments(
        db_url, session_id) as (agent_instruments, db):
        map_table_name_to_table_def = \
            db.get_table_definitions_for_embeddings()
        
        # la ligne 47 a 56 permet de garder uniquement les tables qui ont des 
        # definitions les splus similaire avec la requete sql en lanaguage naturel
        database_embedder = DatabaseEmbedder()

        for name, table_def in map_table_name_to_table_def.items():
            database_embedder.add_table(name, table_def)

        similar_tables = database_embedder.get_similar_tables(raw_prompt, n=2)
        print(similar_tables)
   
        table_definitions = database_embedder.get_table_definitions_from_names(
            similar_tables
        )
        
        # on format le prompt en combinant la question vaac la requete de 
        # l'utilisateur  et en ajoutant la definition des tables dans 
        # notre base de données
        prompt = llm.add_cap_ref(
            prompt,
            f"Use these {PROMPT_TABLES_DEFINITIONS} to satisfy the database query.",
            PROMPT_TABLES_DEFINITIONS,
            table_definitions,
        )
         
         # retourne l'orchestrateur qui permet de combiner les agants, leur instruments
        data_eng_orchestrator = agents.combine_team_instruments_in_orchestrator(
            "data_engineering_team",
            agent_instruments,
            validate_results=agent_instruments.validate_run_sql,
        )

        data_eng_conversation_result: ConversationResult = (
            data_eng_orchestrator.sequential_conversation(prompt)
        )

        with open(agent_instruments.run_sql_results_file, "r") as f:
            result = json.loads(f.read())

        match data_eng_conversation_result:
            case ConversationResult(
                success=True, cost=data_eng_cost, tokens=data_eng_tokens
            ):
                return {
                    "orchestration_status": "success",
                    "request_cost": data_eng_cost,
                    "number_of_tokens": data_eng_tokens,
                    "query": data_eng_orchestrator.engineer_query,
                    "query_result": result,
                    "orchestrator_name": data_eng_orchestrator.name,
                }
                "✅💰📊🤖"
            case _:
                raise ValueError("❌ Orchestrator failed. Team: {data_eng_orchestrator.name} Failed")
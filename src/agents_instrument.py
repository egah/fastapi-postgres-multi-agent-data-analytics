import os

from .db import PostgresManager

BASE_DIR = os.environ.get("BASE_DIR", "./agent_results")


class AgentInstruments:
    """
    !Base class for multli-agent instruments that are tools, state, and functions that an agent can use across the lifecycle of conversations
    """

    def __init__(self) -> None:
        self.session_id = None
        self.messages = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def sync_messages(self, messages: list):
        """
        Syncs messages with the orchestrator
        """
        raise NotImplementedError

    @property
    def root_dir(self):
        return os.path.join(BASE_DIR, self.session_id)

    @property
    def agent_chat_file(self):
        return os.path.join(self.root_dir, "agent_chats.json")


class PostgresAgentInstruments(AgentInstruments):
    """
    Unified Toolset for the Postgres Data Analytics Multi-Agent System

    Advantages:
        - All agents have access to the same state and functions
        - Gives agent functions awareness of changing context
        - Clear and concise capabilities for agents
        - Clean database connection management

    Guidelines:
        - Agent Functions should not call other agent functions directly
            - Instead Agent Functions should call external lower level modules
        - Prefer 1 to 1 mapping of agents and their functions (controverisal)
        - The state lifecycle lives between all agent orchestrations
    """

    def __init__(self, db_url: str, session_id: str) -> None:
        super().__init__()

        self.db_url = db_url
        self.db = None
        self.session_id = session_id
        self.messages = []
        self.complete_keyword = "APPROVED"

        self.innovation_index = 0

        if len(os.listdir(os.path.dirname(os.path.abspath(self.root_dir)))) > 10:
            self.reset_files()

    def __enter__(self):
        self.reset_files()
        self.db = PostgresManager()
        self.db.connect_with_url(self.db_url)
        return self, self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def sync_messages(self, messages: list):
        self.messages = messages

    def reset_files(self):
        """
        Clear everything in the root_dir
        """

        # if it does not exist create it
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)

        for fname in os.listdir(self.root_dir):
            os.remove(os.path.join(self.root_dir, fname))

    # -------------------------- Agent Properties -------------------------- #

    @property
    def run_sql_results_file(self):
        return os.path.join(self.root_dir, "run_sql_results.json")

    # -------------------------- Agent Functions -------------------------- #

    def run_sql(self, sql: str) -> str:
        """
        Run a SQL query against the postgres database
        """
        # execute la requête sql
        results_as_json = self.db.run_sql(sql)

        # nom du fichier dans lequel le fichier est stocké
        fname = self.run_sql_results_file

        # dump these results to a file
        with open(fname, "w") as f:
            f.write(results_as_json)

        return "Successfully delivered results to json file"

    def validate_run_sql(self):
        """
        validate that the run_sql results file exists and has content
        """
        fname = self.run_sql_results_file
        try:
            doc = open(fname, "r")
        except FileNotFoundError:
            return False
        else:
            content = doc.read()
            if not content:
                doc.close()
                return False
            else:
                doc.close()
                return True

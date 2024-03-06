from dataclasses import dataclass
from typing import List
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
from fuzzywuzzy import process

# sentence_transformers


@dataclass
class Chat:
    from_name: str
    to_name: str
    message: str


@dataclass
class ConversationResult:
    success: bool
    messages: List[Chat]
    cost: float
    tokens: int
    last_message_str: str


def generate_session_id(raw_prompt: str):
    """
    "get jobs with 'Completed' or 'Started' status"

    ->

    "get_jobs_with_Completed_or_Started_status__12_22_22"
    """

    now = datetime.now()
    hours = now.hour
    minutes = now.minute
    seconds = now.second

    short_time_mm_ss = f"{hours:02}_{minutes:02}_{seconds:02}"

    lower_case = raw_prompt.lower()
    no_spaces = lower_case.replace(" ", "_")
    no_quotes = no_spaces.replace("'", "")
    shorter = no_quotes[:30]
    with_uuid = shorter + "__" + short_time_mm_ss
    return with_uuid


class DatabaseEmbedder:
    def __init__(self) -> None:
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.model = BertModel.from_pretrained("bert-base-uncased")
        # map table_name with table definition embeddings
        self.map_name_to_embeddings = {}
        # map  table_name with table definition
        self.map_name_to_table_def = {}

    def add_table(self, table_name: str, text_representation: str):
        self.map_name_to_embeddings[table_name] = self.compute_embeddings(
            text_representation
        )
        self.map_name_to_table_def[table_name] = text_representation

    # compute embeddings with BertModel and BertTokenizer
    def compute_embeddings(self, text):
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True, max_length=512
        )
        outputs = self.model(**inputs)
        return outputs["pooler_output"].detach().numpy()

    # compute similarity netween natural query and a table definition
    def compute_similarity(self, query, table_def):
        return cosine_similarity(
            self.compute_embeddings(query), self.compute_embeddings(table_def)
        )[0][0]

    # given a natural query, find the top 'n' tables that are most similar
    def get_similar_tables_via_embeddings(self, query, n=1):
        most_similar = process.extract(
            query,
            self.map_name_to_table_def.values(),
            limit=len(self.map_name_to_table_def),
            scorer=self.compute_similarity,
        )
        result = [elem[0] for elem in most_similar]
        result.sort()
        result.reverse()
        result = result[:n]
        table_def_to_table_name = {v: k for k, v in self.map_name_to_table_def.items()}
        return [table_def_to_table_name.get(tab_def) for tab_def in result]

    # if the table name is in the natural query keep the table
    def get_similar_tables_via_word_match(self, query: str):
        tables = []

        for table_name in self.map_name_to_table_def.keys():
            if table_name.lower() in query.lower():
                tables.append(table_name)

        return tables

    # combine les resultats de get_similar_tables_via_embeddings et get_similar_tables_via_word_match
    def get_similar_tables(self, query: str, n=1):
        similar_tables_via_embeddings = self.get_similar_tables_via_embeddings(query, n)
        similar_tables_via_match = self.get_similar_tables_via_word_match(query)

        return similar_tables_via_embeddings + similar_tables_via_match

    def get_table_definitions_from_names(self, table_names: list) -> str:
        table_defs = [
            self.map_name_to_table_def[table_name] for table_name in table_names
        ]
        return "\n\n".join(table_defs)

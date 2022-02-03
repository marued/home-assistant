from dependency_injector.wiring import inject
from sentence_transformers import SentenceTransformer, util
from typing import List


class MatchingTransformerModel:
    @inject
    def __init__(self) -> None:
        self.sentence_interpreter = SentenceTransformer(
            "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
        )

    def get_embeddings(self, str_list: List[str]) -> List:
        return self.sentence_interpreter.encode(str_list)

    def match(self, commands, commands_emb, query) -> List:
        query_emb = self.get_embeddings(query)
        scores = util.dot_score(query_emb, commands_emb)[0].cpu().tolist()

        # Combine docs & scores
        command_score_pairs = list(zip(commands, scores))

        # Sort by decreasing score
        command_score_pairs = sorted(
            command_score_pairs, key=lambda x: x[1], reverse=True
        )

        # Output passages & scores
        for command, score in command_score_pairs:
            print(score, command)

        return command_score_pairs

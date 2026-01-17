
"""
YBIS COUNCIL CORE
Implements the 'Mixture of Experts' consensus logic.
Inspired by karpathy/llm-council.
"""

import json
from src.agentic.core.utils.logging_utils import log_event
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class Vote(BaseModel):
    agent_id: str
    decision: str  # "APPROVE", "REJECT", "ABSTAIN"
    score: float = Field(..., ge=0.0, le=10.0)
    reason: str

class CouncilResult(BaseModel):
    topic: str
    status: str  # "APPROVED", "REJECTED", "PENDING"
    average_score: float
    votes: List[Vote]
    consensus_summary: str

class TheCouncil:
    """The governing body of YBIS agents."""

    def __init__(self):
        self.debate_path = Path("Knowledge/Messages/debates")

    def _parse_votes(self, debate_id: str) -> List[Vote]:
        """Parse a debate file to extract structured votes from agents."""
        file_path = self.debate_path / f"{debate_id}.json"
        if not file_path.exists():
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        votes = []
        # Simple heuristic: Look for explicit "VOTE:" or JSON blocks in messages
        # In V2, we will force agents to send structured JSON.
        for msg in data.get("messages", []):
            content = msg.get("content", "")

            # Simple keyword parsing (Frankenstein style)
            if "VOTE: APPROVE" in content:
                votes.append(Vote(agent_id=msg["from"], decision="APPROVE", score=10.0, reason="Text analysis"))
            elif "VOTE: REJECT" in content:
                votes.append(Vote(agent_id=msg["from"], decision="REJECT", score=0.0, reason="Text analysis"))
            # TODO: Add regex for "Score: 8.5" extraction

        return votes

    def evaluate_debate(self, debate_id: str, threshold: float = 7.0) -> CouncilResult:
        """
        Analyze a debate and return the Council's decision.
        """
        file_path = self.debate_path / f"{debate_id}.json"
        if not file_path.exists():
            return CouncilResult(topic="Unknown", status="ERROR", average_score=0, votes=[], consensus_summary="Debate not found")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        votes = self._parse_votes(debate_id)

        if not votes:
            return CouncilResult(
                topic=data.get("topic", ""),
                status="PENDING",
                average_score=0.0,
                votes=[],
                consensus_summary="No votes cast yet."
            )

        avg_score = sum(v.score for v in votes) / len(votes)
        status = "APPROVED" if avg_score >= threshold else "REJECTED"

        return CouncilResult(
            topic=data.get("topic", ""),
            status=status,
            average_score=avg_score,
            votes=votes,
            consensus_summary=f"Council has spoken. {len(votes)} votes cast. Average: {avg_score:.1f}"
        )

# Example Usage
if __name__ == "__main__":
    council = TheCouncil()
    # Mocking a check (replace with real ID in prod)
    log_event("Council Module Loaded.", component="council")

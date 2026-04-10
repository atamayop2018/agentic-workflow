"""
Responsible Academic Planning Agent
---------------------------------
A small agentic workflow that helps students plan study work, locate local
learning resources, and refuse requests that conflict with academic integrity.
"""

from __future__ import annotations

from collections import deque
from dataclasses import asdict, dataclass
from datetime import datetime
import re
from typing import Deque, Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


RESOURCE_DB = pd.DataFrame(
    [
        {"topic": "python", "resource": "Review loops, functions, and list comprehensions", "type": "practice", "minutes": 45},
        {"topic": "python", "resource": "Complete 5 short debugging exercises", "type": "practice", "minutes": 30},
        {"topic": "data analysis", "resource": "Read a short guide on pandas filtering and grouping", "type": "reading", "minutes": 35},
        {"topic": "data analysis", "resource": "Practice with one small CSV cleaning task", "type": "practice", "minutes": 40},
        {"topic": "statistics", "resource": "Review mean, variance, and probability notes", "type": "review", "minutes": 40},
        {"topic": "statistics", "resource": "Solve 8 mixed probability practice questions", "type": "practice", "minutes": 50},
        {"topic": "time management", "resource": "Use a Pomodoro block and checkpoint reflection", "type": "routine", "minutes": 25},
        {"topic": "general study skills", "resource": "Build a checklist with one milestone per hour", "type": "planning", "minutes": 20},
    ]
)

POLICY_DB = {
    "integrity": "I can support your learning, but I will not complete graded work or fabricate answers for you.",
    "transparency": "This agent always reports its intent classification, tools used, and memory updates.",
    "fallback": "When confidence is low, the agent falls back to a generic study checklist instead of pretending certainty.",
}

TOPIC_KEYWORDS = {
    "python": ["python", "loop", "function", "debug", "code"],
    "data analysis": ["data", "pandas", "csv", "analysis", "plot"],
    "statistics": ["statistics", "probability", "mean", "variance", "distribution"],
    "time management": ["schedule", "time", "deadline", "plan", "organize"],
}

RISK_TERMS = [
    "write my",
    "do my homework",
    "complete my assignment",
    "cheat",
    "bypass",
    "answer the quiz for me",
]


@dataclass
class MemoryEntry:
    timestamp: str
    request: str
    intent: str
    risk: str
    topic: str
    outcome: str


class AcademicPlanningAgent:
    def __init__(self, max_memory: int = 6) -> None:
        self.persona = "Responsible Academic Planning Agent"
        self.memory: Deque[MemoryEntry] = deque(maxlen=max_memory)
        self.logs: List[str] = []

    def _log(self, message: str) -> None:
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append(f"[{stamp}] {message}")

    def classify_request(self, request: str) -> tuple[str, str]:
        lower = request.lower()
        if any(term in lower for term in RISK_TERMS):
            return "integrity_risk", "high"
        if any(term in lower for term in ["plan", "schedule", "organize", "deadline"]):
            return "planning", "low"
        if any(term in lower for term in ["explain", "review", "practice", "resource", "understand"]):
            return "concept_help", "low"
        return "general_support", "medium"

    def detect_topic(self, request: str) -> str:
        lower = request.lower()
        scores = {
            topic: sum(1 for keyword in keywords if keyword in lower)
            for topic, keywords in TOPIC_KEYWORDS.items()
        }
        best_topic = max(scores, key=scores.get)
        return best_topic if scores[best_topic] > 0 else "general study skills"

    def extract_constraints(self, request: str) -> tuple[int, int]:
        lower = request.lower()
        hour_match = re.search(r"(\d+)\s*(hour|hours|hr|hrs)", lower)
        day_match = re.search(r"(\d+)\s*(day|days)", lower)

        hours = int(hour_match.group(1)) if hour_match else 4
        if "tomorrow" in lower:
            days = 1
        elif "tonight" in lower:
            days = 0
        else:
            days = int(day_match.group(1)) if day_match else 3

        return max(hours, 1), max(days, 0)

    def policy_lookup(self, key: str) -> str:
        return POLICY_DB.get(key, POLICY_DB["fallback"])

    def resource_lookup(self, topic: str) -> pd.DataFrame:
        matches = RESOURCE_DB[RESOURCE_DB["topic"] == topic]
        if matches.empty:
            matches = RESOURCE_DB[RESOURCE_DB["topic"] == "general study skills"]
        return matches.head(3)

    def build_schedule(self, hours: int, days: int) -> List[str]:
        allocations = np.array([0.4, 0.4, 0.2]) * hours * 60
        rounded = (np.round(allocations / 5) * 5).astype(int)
        return [
            f"Concept review: {rounded[0]} minutes",
            f"Targeted practice: {rounded[1]} minutes",
            f"Reflection and recap: {rounded[2]} minutes",
            f"Deadline horizon: {days} day(s)",
        ]

    def respond(self, request: str) -> Dict[str, object]:
        self._log(f"Received request: {request}")
        intent, risk = self.classify_request(request)
        topic = self.detect_topic(request)
        hours, days = self.extract_constraints(request)

        reasoning_trace = [
            f"Intent classified as '{intent}' with risk '{risk}'.",
            f"Topic detected as '{topic}'.",
            f"Extracted constraints: {hours} hour(s), {days} day(s).",
        ]

        if intent == "integrity_risk":
            tools_used = ["policy_lookup", "memory_write"]
            response = (
                f"I can't do the graded work for you. {self.policy_lookup('integrity')}\n\n"
                "Safer next steps:\n"
                "1. Share the prompt and I can help you break it into smaller parts.\n"
                "2. I can create a study checklist or outline.\n"
                "3. I can quiz you with practice questions so you can write the final response yourself."
            )
            status = "redirected"
        elif intent == "planning":
            tools_used = ["resource_lookup", "schedule_builder", "memory_write"]
            resources = self.resource_lookup(topic)
            schedule = self.build_schedule(hours, days)
            resource_lines = "\n".join(
                f"- {row.resource} ({row.type}, ~{row.minutes} min)"
                for row in resources.itertuples()
            )
            response = (
                f"Here is a focused study plan for **{topic}**:\n"
                + "\n".join(f"- {step}" for step in schedule)
                + "\nRecommended resources:\n"
                + resource_lines
                + "\nTransparency note: this answer used local planning rules rather than hidden reasoning."
            )
            status = "supported"
        elif intent == "concept_help":
            tools_used = ["resource_lookup", "memory_write"]
            resources = self.resource_lookup(topic)
            resource_lines = "\n".join(
                f"- {row.resource} ({row.type}, ~{row.minutes} min)"
                for row in resources.itertuples()
            )
            response = (
                f"You seem to need concept support in **{topic}**. Start with:\n"
                + resource_lines
                + "\nIf you want, I can also turn this into a 30-minute review routine or a self-test checklist."
            )
            status = "supported"
        else:
            tools_used = ["policy_lookup", "memory_write"]
            response = (
                "I am not fully confident about the exact intent, so I am using a safe fallback. "
                + self.policy_lookup("fallback")
                + "\nTry sharing the topic, the time available, and the due date for a more precise plan."
            )
            status = "fallback"

        reasoning_trace.append(f"Selected tools: {', '.join(tools_used)}.")
        reasoning_trace.append(f"Final status: {status}.")

        self.memory.append(
            MemoryEntry(
                timestamp=datetime.now().isoformat(timespec="seconds"),
                request=request,
                intent=intent,
                risk=risk,
                topic=topic,
                outcome=status,
            )
        )
        self._log(f"Completed request with status '{status}'.")

        return {
            "request": request,
            "intent": intent,
            "risk": risk,
            "topic": topic,
            "status": status,
            "tools_used": tools_used,
            "reasoning_trace": reasoning_trace,
            "response": response,
        }

    def memory_frame(self) -> pd.DataFrame:
        return pd.DataFrame([asdict(item) for item in self.memory])


def print_result(result: Dict[str, object]) -> None:
    print("\n" + "=" * 88)
    print(f"REQUEST: {result['request']}")
    print(f"INTENT: {result['intent']} | RISK: {result['risk']} | STATUS: {result['status']}")
    print(f"TOOLS USED: {', '.join(result['tools_used'])}")
    print("REASONING TRACE:")
    for step in result["reasoning_trace"]:
        print(f"  - {step}")
    print("RESPONSE:")
    print(result["response"])


def main() -> None:
    agent = AcademicPlanningAgent()

    demo_requests = [
        "I have 5 hours over the next 2 days to prepare for a statistics quiz. Please make me a study plan.",
        "Can you write my discussion post for me so I can submit it tonight?",
        "I need resources to review Python loops and debugging before class tomorrow.",
        "Help me organize my workload for a data analysis lab due in 3 days.",
    ]

    results = [agent.respond(request) for request in demo_requests]
    for result in results:
        print_result(result)

    evaluation_df = pd.DataFrame(
        [
            {
                "intent": item["intent"],
                "risk": item["risk"],
                "status": item["status"],
                "topic": item["topic"],
                "tool_count": len(item["tools_used"]),
            }
            for item in results
        ]
    )

    print("\nEvaluation table:")
    print(evaluation_df.to_string(index=False))

    risk_map = {"low": 1, "medium": 2, "high": 3}
    avg_risk = np.mean([risk_map[item["risk"]] for item in results])
    print(f"\nAverage risk score across representative runs: {avg_risk:.2f} / 3.00")

    status_counts = evaluation_df["status"].value_counts().sort_index()
    plt.figure(figsize=(6, 4))
    status_counts.plot(kind="bar", color=["#4C78A8", "#F58518", "#54A24B"])
    plt.title("Agent outcomes across representative prompts")
    plt.xlabel("Outcome")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("agent_outcomes.png", dpi=150)
    print("Saved visualization to 'agent_outcomes.png'.")

    print("\nShort-term memory:")
    print(agent.memory_frame().to_string(index=False))

    print(
        "\nSummary: This single-agent workflow classifies student requests, uses local tools to "
        "build plans or resource suggestions, stores a short memory of prior interactions, and "
        "refuses integrity-risk requests. Its main limitation is that the reasoning is rule-based, "
        "so unusual prompts can fall back to generic support rather than nuanced personalization."
    )


if __name__ == "__main__":
    main()

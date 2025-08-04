"""
VERN Agent Registry & Orchestration

Manages agent registration, dynamic loading, and role-based orchestration (planner/executor/critic).
"""

from typing import Dict, Callable, Any

import asyncio

class AgentRegistry:
    def __init__(self):
        self.agents: Dict[str, Callable] = {}

    def register(self, name: str, agent_fn: Callable):
        self.agents[name] = agent_fn

    def get(self, name: str) -> Callable:
        return self.agents.get(name)

    def list_agents(self):
        return list(self.agents.keys())

    async def acall(self, name: str, *args, **kwargs) -> Any:
        agent = self.get(name)
        if agent:
            if asyncio.iscoroutinefunction(agent):
                return await agent(*args, **kwargs)
            else:
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, agent, *args, **kwargs)
        else:
            return f"Agent '{name}' not found."

    def call(self, name: str, *args, **kwargs) -> Any:
        agent = self.get(name)
        if agent:
            return agent(*args, **kwargs)
        else:
            return f"Agent '{name}' not found."

# Example agent roles
def planner_agent(task: str, context: dict):
    # Decompose task into steps (stub)
    return [f"Step for: {task}"]

def executor_agent(step: str, context: dict):
    # Execute step (stub)
    return f"Executed: {step}"

def critic_agent(result: str, context: dict):
    # Review result (stub)
    return f"Critique: {result}"

# Registry usage
registry = AgentRegistry()
registry.register("planner", planner_agent)
registry.register("executor", executor_agent)
registry.register("critic", critic_agent)

# Example orchestration
async def orchestrate_async(task: str, context: dict):
    steps = await registry.acall("planner", task, context)
    results = []
    for step in steps:
        result = await registry.acall("executor", step, context)
        results.append(result)
    critiques = []
    for result in results:
        critique = await registry.acall("critic", result, context)
        critiques.append(critique)
    return {"steps": steps, "results": results, "critiques": critiques}

def orchestrate(task: str, context: dict):
    steps = registry.call("planner", task, context)
    results = [registry.call("executor", step, context) for step in steps]
    critiques = [registry.call("critic", result, context) for result in results]
    return {"steps": steps, "results": results, "critiques": critiques}

# Example:
# output = orchestrate("Plan a trip", {})
# print(output)

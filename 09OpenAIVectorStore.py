from agents import Agent, FileSearchTool, Runner, WebSearchTool
import asyncio
from agents import set_default_openai_key

set_default_openai_key("sk-proj-...")
agent = Agent(
    name="Assistant",
    tools=[
        FileSearchTool(
            max_num_results=3,
            vector_store_ids=["vs_..."],
        ),
    ],

)

async def main():
    result = await Runner.run(agent, "How to add user to administrators?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

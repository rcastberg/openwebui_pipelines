from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage
import subprocess
from pydantic import BaseModel


class Pipeline:
    class Valves(BaseModel):
        # List target pipeline ids (models) that this filter will be connected to.
        # If you want to connect this filter to all pipelines, you can set pipelines to ["*"]
        # e.g. ["llama3:latest", "gpt-3.5-turbo"]
        pipelines: List[str] = []

        # Assign a priority level to the filter pipeline.
        # The priority level determines the order in which the filter pipelines are executed.
        # The lower the number, the higher the priority.
        priority: int = 0

    def __init__(self):
        self.type = "filter"
        self.id = "info_pipeline"
        self.name = "Info Pipeline"
        self.valves = self.Valves(
            **{
                "pipelines": ["*"],  # Connect to all pipelines
            }
        )
        self.model = None
        pass

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        # This filter is applied to the form data before it is sent to the OpenAI API.
        print(f"inlet:{__name__}")

        print(messages)
        print(user_message)
        print(body)
        user_message = body["messages"][-1]["content"]

        # Filter out toxic messages
        toxicity = self.model.predict(user_message)
        print(toxicity)

        if toxicity["toxicity"] > 0.5:
            raise Exception("Toxic message detected")

        return body

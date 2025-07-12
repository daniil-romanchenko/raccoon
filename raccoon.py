import abc
import asyncio
import json
import typing as t
from dataclasses import dataclass, field

import click
import httpx
from loguru import logger
from pydantic import StringConstraints

import rigging as rg
from rigging import logging

# Constants

MAX_PINS = 10
MAX_HISTORY = 5

SYSTEM_PROMPT = """
You are a persistent application reconnaissance agent. Your job is to explore a modern JavaScript web app by issuing HTTP requests that simulate user behavior. Look for forms, authentication, API endpoints, and any signs of sensitive logic. Maximize surface discovery.
"""

# Models

str_strip = t.Annotated[str, StringConstraints(strip_whitespace=True)]
str_upper = t.Annotated[str, StringConstraints(to_upper=True)]


class Action(rg.Model, abc.ABC):
    @abc.abstractmethod
    async def run(self, state: "State") -> str:
        ...


class Header(rg.Model):
    name: str = rg.attr()
    value: str_strip


class Parameter(rg.Model):
    name: str = rg.attr()
    value: str_strip


class Request(Action):
    method: str_upper = rg.attr()
    path: str = rg.attr()
    headers: list[Header] = rg.wrapped("headers", rg.element(default=[]))
    url_params: list[Parameter] = rg.wrapped("url_params", rg.element(default=[]))
    body: str_strip = rg.element(default="")

    @classmethod
    def xml_example(cls) -> str:
        return Request(
            method="GET",
            path="/$path",
            headers=[Header(name="X-Header", value="my-value")],
            url_params=[Parameter(name="name", value="test-param")],
            body="$body",
        ).to_pretty_xml()

    async def run(self, state: "State") -> str:
        response = await send_request(state.client, self)
        logger.success(f"{self.method} '{self.path}' -> {response.status_code}")
        state.traffic.append((self, response))
        return response.to_pretty_xml()


class Response(rg.Model):
    status_code: int = rg.attr()
    headers: list[Header] = rg.element(default=[])
    body: str_strip = rg.element(default="")


@dataclass
class State:
    client: httpx.AsyncClient
    max_actions: int
    base_chat: rg.ChatPipeline
    goals: list[str] = field(default_factory=list)
    next_actions: list[Request] = field(default_factory=list)
    traffic: list[tuple[Request, Response]] = field(default_factory=list)

    async def step(self) -> None:
        logger.info(f"Running {len(self.next_actions)} action(s)")
        for action in self.next_actions:
            await action.run(self)
        self.next_actions.clear()

    def get_prompt(self) -> str:
        traffic = "\n".join(f"{r.method} {r.path} -> {res.status_code}" for r, res in self.traffic)
        return f"""
# Traffic
{traffic or 'No traffic yet'}

# Goal
{self.goals[-1] if self.goals else 'Explore the app'}

# Actions
Use the format below to send new HTTP requests.

{Request.xml_example()}
"""


async def send_request(client: httpx.AsyncClient, request: Request) -> Response:
    try:
        json_body = json.loads(request.body)
    except json.JSONDecodeError:
        json_body = None

    httpx_request = client.build_request(
        method=request.method,
        url=request.path,
        headers={h.name: h.value for h in request.headers},
        content=request.body if not json_body else None,
        json=json_body,
    )

    response = await client.send(httpx_request)
    return Response(
        status_code=response.status_code,
        headers=[Header(name=k, value=v) for k, v in response.headers.items()],
        body=response.text,
    )


@click.command()
@click.option("--goal", default="Explore all endpoints in the app.", help="Initial goal")
@click.option("--generator-id", default="ollama/llama3.1,api_base=http://localhost:11434", help="LLM backend")
# @click.option("--generator-id", default="ollama/deepseek-r1:8b,api_base=http://localhost:11434", help="LLM backend")
@click.option("--base-url", default="http://localhost:3000", help="Target URL")
@click.option("--iterations", default=20, help="Max interaction rounds")
@click.option("--max-actions", default=2, help="Max actions per round")
@click.option("--log-level", default="info")
@click.option("--proxy", type=str, help="HTTP proxy to use for requests")
def cli(goal, generator_id, base_url, iterations, max_actions, log_level, proxy: t.Optional[str]):
    logging.configure_logging(log_level)
    generator = rg.get_generator(generator_id)
    client = httpx.AsyncClient(
        base_url=base_url,
        verify=False,
        proxy=proxy if proxy else None
    )

    chat = generator.chat([
        {"role": "system", "content": SYSTEM_PROMPT},
    ], rg.GenerateParams(max_tokens=2048))

    state = State(client=client, max_actions=max_actions, base_chat=chat, goals=[goal])

    async def agent_loop():
        for i in range(iterations):
            logger.info(f"Iteration {i + 1}/{iterations}")

            async def parse(chat: rg.Chat) -> None:
                parsed = chat.last.try_parse_many(Request)
                actions = parsed if parsed else []
                state.next_actions = actions[:max_actions]

            await chat.fork(state.get_prompt()).then(parse).run()
            await state.step()

    asyncio.run(agent_loop())


if __name__ == "__main__":
    cli()

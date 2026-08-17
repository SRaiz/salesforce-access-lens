# MCP Learning Journey

This directory documents the MCP knowledge and architectural
decisions developed while building the MCP interface for
Salesforce Access Lens.

The objective is not only to build a working MCP server, but also
to understand the protocol well enough to explain, design, debug,
and operate an MCP integration confidently.

## Learning Method

Each lesson follows this process:

1. Understand the underlying problem.
2. Learn the MCP concept that addresses it.
3. Map the concept to Salesforce Access Lens.
4. Explain the concept back in our own words.
5. Make an architectural decision.
6. Implement the smallest useful part.
7. Verify the behavior.
8. Record what was learned.

## Lessons

| Lesson | Topic | Status |
|---|---|---|
| 01 | Why MCP Exists | Completed |
| 02 | Host, Client, Server, and Transport | Completed |
| 03 | Tools, Resources, and Prompts | Not Started |
| 04 | MCP Protocol Lifecycle | Not Started |
| 05 | Streamable HTTP | Not Started |
| 06 | Salesforce Access Lens MCP Foundation | Not Started |
| 07 | MCP Inspector and Debugging | Not Started |
| 08 | Salesforce Permission Tools | Not Started |
| 09 | Security and Production Concerns | Not Started |
| 10 | n8n Integration | Not Started |

## Project Principle

MCP is an adapter around the Salesforce Access Lens application
layer. Salesforce permission-resolution logic must remain
independent of MCP so that it can also be reused by a CLI, REST
API, tests, or other integrations.
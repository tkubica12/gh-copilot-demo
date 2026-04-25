"""MCP servers for token-efficiency wide-tool versus discovery-tool tests."""

from __future__ import annotations

import argparse

from mcp.server.fastmcp import FastMCP


def action_payload(index: int) -> dict[str, str]:
    """Return deterministic fake action metadata."""

    marker = "TARGET-SUNSET" if index == 42 else f"TARGET-CODE-{index:03d}"
    return {
        "id": marker,
        "owner": f"team-{index % 7}",
        "payload": f"route-add-on-{index:03d}",
    }


def build_wide_server() -> FastMCP:
    """Expose 100 direct action tools so tool-list context is intentionally large."""

    mcp = FastMCP("token-lab-wide")

    for index in range(100):

        def lookup(index: int = index) -> dict[str, str]:
            """Return action metadata for one fixed action."""

            return action_payload(index)

        lookup.__name__ = f"action_lookup_{index:03d}"
        description = (
            f"Return metadata for catalog action {action_payload(index)['id']}. "
            "The full action description includes eligibility conditions, owner, "
            "payload routing notes, rollback guidance, validation expectations, "
            "audit handling, customer-notification constraints, operational "
            "escalation notes, and idempotency requirements. Use this direct tool "
            "only when the requested target id matches this description exactly."
        )
        mcp.tool(name=f"action_lookup_{index:03d}", description=description)(lookup)

    return mcp


def build_discovery_server() -> FastMCP:
    """Expose search and fetch tools so the model can progressively reveal detail."""

    mcp = FastMCP("token-lab-discovery")

    @mcp.tool()
    def search_actions(query: str) -> list[dict[str, str]]:
        """Search action ids and return compact candidates."""

        results = []
        for index in range(100):
            payload = action_payload(index)
            if query in payload["id"]:
                results.append({"id": payload["id"], "owner": payload["owner"]})
        return results[:5]

    @mcp.tool()
    def get_action(action_id: str) -> dict[str, str]:
        """Fetch full metadata for one action id returned by search_actions."""

        for index in range(100):
            payload = action_payload(index)
            if payload["id"] == action_id:
                return payload
        raise ValueError(f"Unknown action id: {action_id}")

    return mcp


def main() -> int:
    """Run the selected MCP server over stdio."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["wide", "discovery"])
    args = parser.parse_args()
    server = build_wide_server() if args.mode == "wide" else build_discovery_server()
    server.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

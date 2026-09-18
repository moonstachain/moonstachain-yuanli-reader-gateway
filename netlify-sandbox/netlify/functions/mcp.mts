import type { Config, Context } from "@netlify/functions";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { WebStandardStreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/webStandardStreamableHttp.js";
import { z } from "zod";

function buildServer() {
  const server = new McpServer({ name: "yuanli-readonly", version: "0.1.0" });

  server.tool(
    "get_yuanli_context",
    "Return a non-sensitive, read-only Yuanli OS capability-plane proof.",
    { topic: z.string().optional().describe("Optional context label") },
    async ({ topic }) => ({
      content: [{
        type: "text",
        text: JSON.stringify({
          protocol: "YOS-NET0",
          mode: "READ_ONLY",
          authority: "NONE",
          canon_write: false,
          action_write: false,
          topic: topic ?? "default",
          source: "moonstachain/moonstachain-yuanli-reader-gateway",
          status: "G3_REMOTE_MCP_OK"
        })
      }]
    })
  );

  return server;
}

export default async (req: Request, _context: Context) => {
  if (req.method !== "POST") return new Response("Method not allowed", { status: 405 });
  const server = buildServer();
  const transport = new WebStandardStreamableHTTPServerTransport({
    sessionIdGenerator: undefined,
    enableJsonResponse: true
  });
  await server.connect(transport);
  return transport.handleRequest(req);
};

export const config: Config = {
  path: "/mcp",
  rateLimit: {
    windowSize: 60,
    windowLimit: 10,
    aggregateBy: ["ip", "domain"]
  }
};

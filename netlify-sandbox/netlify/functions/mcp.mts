import type { Config, Context } from "@netlify/functions";
import { createHash, timingSafeEqual } from "node:crypto";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { WebStandardStreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/webStandardStreamableHttp.js";
import { z } from "zod";

const CLIENTS = {
  "ray-primary": {
    tokenSha256: "d74949fe78dfb3ce4c8acdbc2668d89adcdb41a12f271f5ae4b73b9aa3cec5ea",
    scopes: ["mcp:read"]
  }
} as const;

function audit(event: string, data: Record<string, unknown>) {
  console.log(JSON.stringify({
    schema: "yos.net1.auth.audit.v1",
    event,
    at: new Date().toISOString(),
    ...data
  }));
}

function authorize(req: Request) {
  const clientId = req.headers.get("x-yuanli-client") ?? "";
  const auth = req.headers.get("authorization") ?? "";
  const client = CLIENTS[clientId as keyof typeof CLIENTS];

  if (!client) {
    audit("AUTH_DENY", { client_id: clientId || "missing", reason: "unknown_client" });
    return { ok: false as const, status: 403, reason: "unknown_client" };
  }

  if (!auth.startsWith("Bearer ")) {
    audit("AUTH_DENY", { client_id: clientId, reason: "missing_bearer" });
    return { ok: false as const, status: 401, reason: "missing_bearer" };
  }

  const token = auth.slice(7);
  const presented = createHash("sha256").update(token).digest();
  const expected = Buffer.from(client.tokenSha256, "hex");
  const matched = presented.length === expected.length && timingSafeEqual(presented, expected);

  if (!matched) {
    audit("AUTH_DENY", { client_id: clientId, reason: "invalid_bearer" });
    return { ok: false as const, status: 401, reason: "invalid_bearer" };
  }

  audit("AUTH_ADMIT", { client_id: clientId, scopes: client.scopes });
  return { ok: true as const, clientId, scopes: client.scopes };
}

function buildServer(clientId: string, scopes: readonly string[]) {
  const server = new McpServer({ name: "yuanli-readonly", version: "0.2.0" });

  server.tool(
    "get_yuanli_context",
    "Return a non-sensitive, governed read-only Yuanli OS capability-plane proof.",
    { topic: z.string().optional().describe("Optional context label") },
    async ({ topic }) => ({
      content: [{
        type: "text",
        text: JSON.stringify({
          protocol: "YOS-NET1",
          mode: "READ_ONLY",
          authority: "NONE",
          canon_write: false,
          action_write: false,
          client_id: clientId,
          scopes,
          topic: topic ?? "default",
          source: "moonstachain/moonstachain-yuanli-reader-gateway",
          status: "NET1_GOVERNED_MCP_OK"
        })
      }]
    })
  );

  return server;
}

export default async (req: Request, _context: Context) => {
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405, headers: { Allow: "POST" } });
  }

  const admission = authorize(req);
  if (!admission.ok) {
    const headers = new Headers({ "Content-Type": "application/json" });
    if (admission.status === 401) {
      headers.set("WWW-Authenticate", 'Bearer realm="yuanli-mcp", scope="mcp:read"');
    }
    return new Response(JSON.stringify({
      error: "unauthorized",
      reason: admission.reason,
      protocol: "YOS-NET1"
    }), { status: admission.status, headers });
  }

  const server = buildServer(admission.clientId, admission.scopes);
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

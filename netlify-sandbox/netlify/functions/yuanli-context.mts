import type { Config, Context } from "@netlify/functions";

export default async (_req: Request, _context: Context) => {
  const body = {
    protocol: "YOS-NET0",
    mode: "READ_ONLY",
    authority: "NONE",
    canon_write: false,
    action_write: false,
    message: "Yuanli Remote Capability Plane reality proof",
    source: "moonstachain/moonstachain-yuanli-reader-gateway",
    status: "G2_READ_ONLY_ENDPOINT_OK"
  };
  return Response.json(body);
};

export const config: Config = {
  path: "/yuanli-context"
};

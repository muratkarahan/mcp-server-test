#!/usr/bin/env node
import readline from "readline";
import { spawn } from "child_process";

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

function send(obj) {
  process.stdout.write(JSON.stringify(obj) + "\n");
}

const tools = [
  {
    name: "run_python",
    title: "Run Python",
    description: "Execute Python code and return stdout/stderr. Use for small scripts.",
    inputSchema: {
      type: "object",
      properties: {
        code: { type: "string", description: "Python code to execute" }
      },
      required: ["code"]
    }
  }
];

rl.on("line", async (line) => {
  let msg;
  try { msg = JSON.parse(line); } catch { return; }

  if (msg.method === "initialize") {
    return send({
      jsonrpc: "2.0",
      id: msg.id,
      result: {
        protocolVersion: "2024-11-05",
        capabilities: {},
        serverInfo: {
          name: "mcp-python",
          version: "1.0.0"
        }
      }
    });
  }

  if (msg.method === "tools/list") {
    return send({ jsonrpc: "2.0", id: msg.id, result: { tools } });
  }

  if (msg.method === "tools/call" && msg.params?.name === "run_python") {
    const code = msg.params?.arguments?.code ?? "";
    const py = spawn("python", ["-c", code], { stdio: ["ignore", "pipe", "pipe"] });

    let out = "", err = "";
    py.stdout.on("data", (d) => (out += d.toString("utf-8")));
    py.stderr.on("data", (d) => (err += d.toString("utf-8")));

    py.on("error", (error) => {
      send({
        jsonrpc: "2.0",
        id: msg.id,
        error: {
          code: -1,
          message: `Python spawn error: ${error.message}`
        }
      });
    });

    py.on("close", (exitCode) => {
      send({
        jsonrpc: "2.0",
        id: msg.id,
        result: {
          exitCode,
          stdout: out,
          stderr: err
        }
      });
    });

    return;
  }
});

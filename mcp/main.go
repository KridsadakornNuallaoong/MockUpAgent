package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

type Request struct {
	Jsonrpc string          `json:"jsonrpc"`
	ID      any             `json:"id"`
	Method  string          `json:"method"`
	Params  json.RawMessage `json:"params,omitempty"`
}

type Response struct {
	Jsonrpc string `json:"jsonrpc"`
	ID      any    `json:"id"`
	Result  any    `json:"result,omitempty"`
	Error   any    `json:"error,omitempty"`
}

func main() {
	http.HandleFunc("/mcp", handleMCP)

	log.Println("🚀 MCP HTTP server running on http://localhost:8001/mcp")
	log.Fatal(http.ListenAndServe(":8001", nil))
}

func handleMCP(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "POST only", http.StatusMethodNotAllowed)
		return
	}

	var req Request
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	resp := Response{
		Jsonrpc: "2.0",
		ID:      req.ID,
	}

	switch req.Method {

	// ----------------------
	// REQUIRED
	// ----------------------
	case "initialize":
		resp.Result = map[string]any{
			"protocolVersion": "2024-11-05",
			"serverInfo": map[string]any{
				"name":    "go-mcp-http",
				"version": "1.0.0",
			},
			"capabilities": map[string]any{
				"tools":     map[string]any{},
				"prompts":   map[string]any{},
				"resources": map[string]any{},
			},
		}

	// ----------------------
	// TOOLS
	// ----------------------
	case "tools/list":
		resp.Result = map[string]any{
			"tools": []any{
				map[string]any{
					"name":        "hello",
					"description": "Say hello",
					"inputSchema": map[string]any{
						"type": "object",
						"properties": map[string]any{
							"name": map[string]any{
								"type": "string",
							},
						},
						"required": []string{"name"},
					},
				},
				map[string]any{
					"name":        "add",
					"description": "Add two numbers",
					"inputSchema": map[string]any{
						"type": "object",
						"properties": map[string]any{
							"a": map[string]any{
								"type": "number",
							},
							"b": map[string]any{
								"type": "number",
							},
						},
						"required": []string{"a", "b"},
					},
				},
			},
		}

	case "tools/call":
		var p struct {
			Name      string         `json:"name"`
			Arguments map[string]any `json:"arguments"`
		}
		json.Unmarshal(req.Params, &p)

		switch p.Name {
		case "hello":
			resp.Result = map[string]any{
				"content": []any{
					map[string]any{
						"type": "text",
						"text": fmt.Sprintf("Hello %s 👋 from MCP HTTP server", p.Arguments["name"]),
					},
				},
			}
		case "add":
			a := p.Arguments["a"].(float64)
			b := p.Arguments["b"].(float64)
			sum := a + b
			resp.Result = map[string]any{
				"content": []any{
					map[string]any{
						"type": "text",
						"text": fmt.Sprintf("The sum of %.2f and %.2f is %.2f", a, b, sum),
					},
				},
			}
		}

	// ----------------------
	// PROMPTS
	// ----------------------
	case "prompts/list":
		resp.Result = map[string]any{
			"prompts": []any{
				map[string]any{
					"name":        "explain_code",
					"description": "Explain Go code step by step",
					"arguments": []any{
						map[string]any{
							"name":     "code",
							"required": true,
						},
					},
				},
			},
		}

	case "prompts/get":
		var p struct {
			Name string `json:"name"`
		}
		json.Unmarshal(req.Params, &p)

		if p.Name == "explain_code" {
			resp.Result = map[string]any{
				"messages": []any{
					map[string]any{
						"role": "system",
						"content": map[string]any{
							"type": "text",
							"text": "You are a senior Go engineer. Explain the following code step by step.",
						},
					},
				},
			}
		}

	// ----------------------
	// RESOURCES
	// ----------------------
	case "resources/list":
		resp.Result = map[string]any{
			"resources": []any{
				map[string]any{
					"uri":      "resource://config/app",
					"name":     "App Config",
					"mimeType": "application/json",
				},
			},
		}

	case "resources/read":
		var p struct {
			URI string `json:"uri"`
		}
		json.Unmarshal(req.Params, &p)

		if p.URI == "resource://config/app" {
			resp.Result = map[string]any{
				"contents": []any{
					map[string]any{
						"uri":      p.URI,
						"mimeType": "application/json",
						"text":     `{"app":"MCP HTTP","version":"1.0.0"}`,
					},
				},
			}
		}

	default:
		resp.Error = map[string]any{
			"code":    -32601,
			"message": "Method not found",
		}
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

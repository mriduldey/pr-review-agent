TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read one sample file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string"}
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "post_review_comment",
            "description": "Save a simulated PR review comment",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string"},
                    "comment": {"type": "string"}
                },
                "required": ["filename", "comment"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_pr_status",
            "description": "Set simulated PR review status",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["PASS", "BLOCKED"]
                    }
                },
                "required": ["status"]
            }
        }
    }
]
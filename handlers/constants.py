Simple = {
  "title": "A registration form",
  "description": "A simple form example.",
  "type": "object",
  "required": [
    "firstName",
    "lastName"
  ],
  "properties": {
    "firstName": {
      "type": "string",
      "title": "First name",
      "default": "Chuck"
    },
    "lastName": {
      "type": "string",
      "title": "Last name"
    },
    "telephone": {
      "type": "string",
      "title": "Telephone",
      "minLength": 10
    }
  }
}

Nested = {
  "title": "A list of tasks",
  "type": "object",
  "required": [
    "title"
  ],
  "properties": {
    "title": {
      "type": "string",
      "title": "Task list title"
    },
    "tasks": {
      "type": "array",
      "title": "Tasks",
      "items": {
        "type": "object",
        "required": [
          "title"
        ],
        "properties": {
          "title": {
            "type": "string",
            "title": "Title",
            "description": "A sample title"
          },
          "details": {
            "type": "string",
            "title": "Task details",
            "description": "Enter the task details"
          },
          "done": {
            "type": "boolean",
            "title": "Done?",
            "default": False
          }
        }
      }
    }
  }
}

DEFAULT_SCHEME = Nested

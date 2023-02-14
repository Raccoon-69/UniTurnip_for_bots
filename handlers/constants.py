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

Arrays = {
    "definitions": {
        "Thing": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "default": "Default name"
                }
            }
        }
    },
    "type": "object",
    "properties": {
        "listOfStrings": {
            "type": "array",
            "title": "A list of strings",
            "items": {
                "type": "string",
                "default": "bazinga"
            }
        },
        "multipleChoicesList": {
            "type": "array",
            "title": "A multiple choices list",
            "items": {
                "type": "string",
                "enum": [
                    "foo",
                    "bar",
                    "fuzz",
                    "qux"
                ]
            },
            "uniqueItems": True
        },
        "fixedItemsList": {
            "type": "array",
            "title": "A list of fixed items",
            "items": [
                {
                    "title": "A string value",
                    "type": "string",
                    "default": "lorem ipsum"
                },
                {
                    "title": "a boolean value",
                    "type": "boolean"
                }
            ],
            "additionalItems": {
                "title": "Additional item",
                "type": "number"
            }
        },
        "minItemsList": {
            "type": "array",
            "title": "A list with a minimal number of items",
            "minItems": 3,
            "items": {
                "$ref": "#/definitions/Thing"
            }
        },
        "defaultsAndMinItems": {
            "type": "array",
            "title": "List and item level defaults",
            "minItems": 5,
            "default": [
                "carp",
                "trout",
                "bream"
            ],
            "items": {
                "type": "string",
                "default": "unidentified"
            }
        },
        "nestedList": {
            "type": "array",
            "title": "Nested list",
            "items": {
                "type": "array",
                "title": "Inner list",
                "items": {
                    "type": "string",
                    "default": "lorem ipsum"
                }
            }
        },
        "unorderable": {
            "title": "Unorderable items",
            "type": "array",
            "items": {
                "type": "string",
                "default": "lorem ipsum"
            }
        },
        "unremovable": {
            "title": "Unremovable items",
            "type": "array",
            "items": {
                "type": "string",
                "default": "lorem ipsum"
            }
        },
        "noToolbar": {
            "title": "No add, remove and order buttons",
            "type": "array",
            "items": {
                "type": "string",
                "default": "lorem ipsum"
            }
        },
        "fixedNoToolbar": {
            "title": "Fixed array without buttons",
            "type": "array",
            "items": [
                {
                    "title": "A number",
                    "type": "number",
                    "default": 42
                },
                {
                    "title": "A boolean",
                    "type": "boolean",
                    "default": False
                }
            ],
            "additionalItems": {
                "title": "A string",
                "type": "string",
                "default": "lorem ipsum"
            }
        }
    }
}

dependencies = {
    "title": "Schema dependencies",
    "description": "These samples are best viewed without live validation.",
    "type": "object",
    "properties": {
        "conditional": {
            "title": "Conditional",
            "$ref": "#/definitions/person"
        }
    },
    "definitions": {
        "person": {
            "title": "Person",
            "type": "object",
            "properties": {
                "Do you have any pets?": {
                    "type": "string",
                    "enum": [
                        "No",
                        "Yes: One",
                        "Yes: More than one"
                    ],
                    "default": "No"
                }
            },
            "required": [
                "Do you have any pets?"
            ],
            "dependencies": {
                "Do you have any pets?": {
                    "oneOf": [
                        {
                            "properties": {
                                "Do you have any pets?": {
                                    "enum": [
                                        "No"
                                    ]
                                }
                            }
                        },
                        {
                            "properties": {
                                "Do you have any pets?": {
                                    "enum": [
                                        "Yes: One"
                                    ]
                                },
                                "How old is your pet?": {
                                    "type": "number"
                                }
                            },
                            "required": [
                                "How old is your pet?"
                            ]
                        },
                        {
                            "properties": {
                                "Do you have any pets?": {
                                    "enum": [
                                        "Yes: More than one"
                                    ]
                                },
                                "Do you want to get rid of any?": {
                                    "type": "boolean"
                                }
                            },
                            "required": [
                                "Do you want to get rid of any?"
                            ]
                        }
                    ]
                }
            }
        }
    }
}

DEFAULT_SCHEME = Simple

post_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "isbn": {"type": "string"},
        "authors": {"type": "array",
                    "contains": {"type": "string"}},
        "number_of_pages": {"type": "number", "minimum": 1},
        "publisher": {"type": "string"},
        "country": {"type": "string"},
        "release_date": {"format": "date",
                         "type": "string"
                         }
    },
    "required": ["name"]
}

get_schema = ["name", "country", "publisher", "release date"]

patch_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "isbn": {"type": "string"},
        "authors": {"type": "array",
                    "contains": {"type": "string"}},
        "number_of_pages": {"type": "number", "minimum": 1},
        "publisher": {"type": "string"},
        "country": {"type": "string"},
        "release_date": {"format": "date",
                         "type": "string"
                         }
    }
}
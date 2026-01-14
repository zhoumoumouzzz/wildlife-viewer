def load_schema(path="db/schema.sql"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "未找到 schema.sql"

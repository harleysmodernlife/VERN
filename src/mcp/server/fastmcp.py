class FastMCP:
    def __init__(self, name):
        self.name = name
        self.tools = {}

    def tool(self):
        def decorator(f):
            self.tools[f.__name__] = f
            return f
        return decorator

    async def list_tools(self):
        return list(self.tools.keys())

    async def run_stdio(self):
        pass
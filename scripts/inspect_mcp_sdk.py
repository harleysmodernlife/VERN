import mcp
import sys

print("mcp module attributes:")
print(dir(mcp))

try:
    import mcp.client
    print("\nmcp.client module attributes:")
    print(dir(mcp.client))
except ImportError as e:
    print("\nCould not import mcp.client:", e)
    sys.exit(1)

try:
    from agents import Thread, Runner
    print("Imports successful.")
except ImportError as e:
    print(f"ImportError: {e}")

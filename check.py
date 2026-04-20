print("Testing imports...")

try:
    from agents.Donna import Donna
    print("✅ Donna imported")
except Exception as e:
    print(f"❌ Donna failed: {e}")

try:
    from agents.mike import Mike
    print("✅ Mike imported")
except Exception as e:
    print(f"❌ Mike failed: {e}")

try:
    from agents.harvey import Harvey
    print("✅ Harvey imported")
except Exception as e:
    print(f"❌ Harvey failed: {e}")

try:
    from agents.louis import Louis
    print("✅ Louis imported")
except Exception as e:
    print(f"❌ Louis failed: {e}")

try:
    from agents.Jessica import Jessica
    print("✅ Jessica imported")
except Exception as e:
    print(f"❌ Jessica failed: {e}")
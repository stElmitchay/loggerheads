"""
Test script for user context functionality.
"""

from loggerheads.user_context import UserContext
import json
import os

def test_user_context():
    """Test user context creation and usage."""

    # Use a test config file
    test_config = "/tmp/test_daily_tracker_context.json"

    # Clean up any existing test config
    if os.path.exists(test_config):
        os.remove(test_config)

    print("🧪 Testing User Context Functionality\n")
    print("=" * 60)

    # Test 1: Create new context with defaults
    print("\n1️⃣ Creating new user context with defaults...")
    context = UserContext(config_path=test_config)
    print(f"✅ Config created at: {test_config}")
    print(f"   Role: {context.config['user_role']}")
    print(f"   Industry: {context.config['industry']}")

    # Test 2: Modify and save configuration
    print("\n2️⃣ Modifying configuration...")
    context.config['user_role'] = "Social Media Manager"
    context.config['industry'] = "Marketing"
    context.config['custom_rules']['WhatsApp'] = "work"
    context.config['custom_rules']['Instagram'] = "work"
    context.save_config()
    print("✅ Configuration updated:")
    print(f"   New Role: {context.config['user_role']}")
    print(f"   New Industry: {context.config['industry']}")
    print(f"   WhatsApp: {context.config['custom_rules']['WhatsApp']}")
    print(f"   Instagram: {context.config['custom_rules']['Instagram']}")

    # Test 3: Load existing configuration
    print("\n3️⃣ Loading configuration from file...")
    context2 = UserContext(config_path=test_config)
    print(f"✅ Config loaded successfully")
    print(f"   Role: {context2.config['user_role']}")
    print(f"   Industry: {context2.config['industry']}")

    # Test 4: Generate AI prompt context
    print("\n4️⃣ Generating AI context prompt...")
    prompt = context2.get_user_context_prompt()
    print("✅ AI Prompt generated:")
    print("-" * 60)
    print(prompt)
    print("-" * 60)

    # Test 5: Test work categorization
    print("\n5️⃣ Testing work categorization logic...")
    test_cases = [
        ("WhatsApp", "Client meeting notes"),
        ("Instagram", "Posting campaign updates"),
        ("VSCode", "Writing Python code"),
        ("Netflix", "Watching a show"),
        ("Chrome", "github.com/myproject"),
        ("Chrome", "reddit.com/r/funny")
    ]

    for app, window_title in test_cases:
        result = context2.is_work_activity(app, window_title)
        print(f"   {app} - '{window_title}': {result}")

    # Test 6: Show final config
    print("\n6️⃣ Final configuration:")
    print(json.dumps(context2.config, indent=2))

    # Cleanup
    print(f"\n🧹 Cleaning up test file: {test_config}")
    os.remove(test_config)

    print("\n" + "=" * 60)
    print("✅ All tests passed!")

if __name__ == "__main__":
    test_user_context()

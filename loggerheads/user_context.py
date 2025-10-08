"""
User context configuration for intelligent work categorization.
Allows users to define what counts as work based on their role and industry.
"""

import json
import os
from pathlib import Path


class UserContext:
    """Manages user's work context and categorization preferences."""

    def __init__(self, config_path=None):
        """
        Initialize user context.

        Args:
            config_path (str): Path to user context config file
        """
        if config_path is None:
            config_path = os.path.join(os.path.expanduser("~"), ".loggerheads_context.json")

        self.config_path = config_path
        self.config = self._load_or_create_config()

    def _load_or_create_config(self):
        """Load existing config or create default one."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error loading config: {e}, creating new one")

        # Default configuration
        return {
            "user_role": "Software Developer",
            "industry": "Technology",
            "work_apps": {
                "VSCode": "always_work",
                "PyCharm": "always_work",
                "IntelliJ": "always_work",
                "Terminal": "always_work",
                "iTerm": "always_work",
                "Slack": "work_hours_only",
                "Discord": "check_content",
                "Chrome": "check_content",
                "Safari": "check_content",
                "Firefox": "check_content"
            },
            "work_keywords": [
                "github.com",
                "stackoverflow",
                "documentation",
                "api",
                "localhost",
                "development",
                "pull request",
                "commit",
                "merge",
                "deploy"
            ],
            "personal_keywords": [
                "facebook.com",
                "instagram.com",
                "reddit.com/r/funny",
                "youtube.com/watch",
                "netflix.com",
                "twitter.com/home"
            ],
            "work_hours": {
                "start": "09:00",
                "end": "18:00",
                "timezone": "local"
            },
            "custom_rules": {
                "WhatsApp": "personal",
                "Messages": "personal",
                "Signal": "personal"
            }
        }

    def save_config(self):
        """Save current configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, indent=2, fp=f)
            print(f"✅ Configuration saved to {self.config_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving config: {e}")
            return False

    def get_user_context_prompt(self):
        """
        Generate a context string for the AI to understand user's work.

        Returns:
            str: Context description for AI prompt
        """
        role = self.config.get("user_role", "Professional")
        industry = self.config.get("industry", "Technology")

        work_apps = [app for app, rule in self.config.get("work_apps", {}).items()
                     if rule == "always_work"]

        custom_work = [app for app, rule in self.config.get("custom_rules", {}).items()
                      if rule == "work"]

        context = f"""
USER CONTEXT:
- Role: {role}
- Industry: {industry}
- Primary work applications: {', '.join(work_apps) if work_apps else 'Not specified'}
- Custom work apps: {', '.join(custom_work) if custom_work else 'None'}

WORK CATEGORIZATION RULES:
- Focus ONLY on work-related activities relevant to a {role} in {industry}
- Ignore personal messaging apps, social media browsing, entertainment
- For browsers, only consider work-related content (documentation, development tools, professional research)
"""

        work_keywords = self.config.get("work_keywords", [])
        if work_keywords:
            context += f"\n- Work-related keywords to look for: {', '.join(work_keywords[:10])}"

        personal_keywords = self.config.get("personal_keywords", [])
        if personal_keywords:
            context += f"\n- Personal/non-work keywords to IGNORE: {', '.join(personal_keywords[:10])}"

        return context

    def is_work_activity(self, app_name, window_title=None, timestamp=None):
        """
        Determine if an activity should be categorized as work.

        Args:
            app_name (str): Name of the application
            window_title (str): Window title/content
            timestamp (datetime): When the activity occurred

        Returns:
            str: "work", "personal", or "check_ai" (let AI decide)
        """
        # Check custom rules first
        custom_rules = self.config.get("custom_rules", {})
        if app_name in custom_rules:
            rule = custom_rules[app_name]
            if rule in ["work", "personal"]:
                return rule

        # Check work apps configuration
        work_apps = self.config.get("work_apps", {})
        if app_name in work_apps:
            rule = work_apps[app_name]

            if rule == "always_work":
                return "work"
            elif rule == "never_work":
                return "personal"
            elif rule == "check_content":
                # Check against keywords if window title provided
                if window_title:
                    return self._check_keywords(window_title)
                return "check_ai"
            elif rule == "work_hours_only":
                # TODO: Implement time-based checking
                return "check_ai"

        # Default: let AI decide
        return "check_ai"

    def _check_keywords(self, text):
        """
        Check text against work and personal keywords.

        Args:
            text (str): Text to check

        Returns:
            str: "work", "personal", or "check_ai"
        """
        text_lower = text.lower()

        # Check work keywords
        work_keywords = self.config.get("work_keywords", [])
        work_matches = sum(1 for keyword in work_keywords if keyword.lower() in text_lower)

        # Check personal keywords
        personal_keywords = self.config.get("personal_keywords", [])
        personal_matches = sum(1 for keyword in personal_keywords if keyword.lower() in text_lower)

        if work_matches > personal_matches:
            return "work"
        elif personal_matches > work_matches:
            return "personal"
        else:
            return "check_ai"

    def setup_interactive(self):
        """Interactive setup wizard for user context."""
        print("\n🎯 Loggerheads - User Context Setup")
        print("=" * 50)
        print("This helps the AI understand what counts as 'work' for you.\n")

        # Get user role
        current_role = self.config.get("user_role", "Software Developer")
        role = input(f"What is your role? [{current_role}]: ").strip()
        if role:
            self.config["user_role"] = role

        # Get industry
        current_industry = self.config.get("industry", "Technology")
        industry = input(f"What industry do you work in? [{current_industry}]: ").strip()
        if industry:
            self.config["industry"] = industry

        # Custom app rules
        print("\n📱 Custom App Rules")
        print("Define which apps should always/never be counted as work.")
        print("Examples: WhatsApp, Discord, Telegram, etc.\n")

        add_custom = input("Add custom app rules? [y/N]: ").strip().lower()
        if add_custom == 'y':
            while True:
                app = input("\nApp name (or press Enter to finish): ").strip()
                if not app:
                    break

                print(f"How should '{app}' be categorized?")
                print("  1. Always work")
                print("  2. Always personal")
                print("  3. Check content (context-dependent)")

                choice = input("Choice [1-3]: ").strip()

                if choice == "1":
                    self.config["custom_rules"][app] = "work"
                elif choice == "2":
                    self.config["custom_rules"][app] = "personal"
                elif choice == "3":
                    self.config["work_apps"][app] = "check_content"
                else:
                    print("Invalid choice, skipping...")

        # Work keywords
        print("\n🔑 Work-related Keywords")
        print("Add keywords that indicate work activity (e.g., 'gitlab', 'jira', 'confluence')")

        add_keywords = input("Add work keywords? [y/N]: ").strip().lower()
        if add_keywords == 'y':
            keywords = input("Enter keywords (comma-separated): ").strip()
            if keywords:
                new_keywords = [k.strip() for k in keywords.split(',')]
                self.config["work_keywords"].extend(new_keywords)

        # Save configuration
        print("\n💾 Saving configuration...")
        if self.save_config():
            print(f"\n✅ Setup complete! Configuration saved to: {self.config_path}")
            print("\nYou can edit this file directly or re-run setup anytime.")
        else:
            print("\n❌ Failed to save configuration")

        return self.config


def get_user_context():
    """
    Get or create user context configuration.

    Returns:
        UserContext: User context instance
    """
    return UserContext()


if __name__ == "__main__":
    # Run interactive setup if executed directly
    context = UserContext()
    context.setup_interactive()

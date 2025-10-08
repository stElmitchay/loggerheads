"""
Auto-start configuration for loggerheads on macOS.
Creates a LaunchAgent to run the tracker automatically on system boot.
"""

import os
import sys
import subprocess
from pathlib import Path


def get_plist_path():
    """Get the LaunchAgent plist file path."""
    home = Path.home()
    launch_agents_dir = home / "Library" / "LaunchAgents"
    launch_agents_dir.mkdir(parents=True, exist_ok=True)
    return launch_agents_dir / "com.loggerheads.autostart.plist"


def get_executable_path():
    """Get the path to the loggerheads executable."""
    try:
        result = subprocess.run(['which', 'loggerheads'],
                              capture_output=True,
                              text=True,
                              check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        # Fallback: try to find it in common locations
        python_bin = os.path.dirname(sys.executable)
        possible_path = os.path.join(python_bin, 'loggerheads')
        if os.path.exists(possible_path):
            return possible_path
        return None


def create_plist_content(executable_path):
    """
    Create the LaunchAgent plist content.

    Args:
        executable_path (str): Path to loggerheads executable

    Returns:
        str: plist XML content
    """
    log_dir = Path.home() / ".loggerheads_logs"
    log_dir.mkdir(exist_ok=True)

    stdout_log = log_dir / "loggerheads.log"
    stderr_log = log_dir / "loggerheads_error.log"

    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.loggerheads.autostart</string>

    <key>ProgramArguments</key>
    <array>
        <string>{executable_path}</string>
        <string>start</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>{stdout_log}</string>

    <key>StandardErrorPath</key>
    <string>{stderr_log}</string>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:{os.path.dirname(executable_path)}</string>
    </dict>

    <key>WorkingDirectory</key>
    <string>{Path.home()}</string>
</dict>
</plist>
"""
    return plist_content


def install_autostart():
    """Install the LaunchAgent for auto-start on boot."""
    print("🔧 Installing loggerheads auto-start...")

    # Get executable path
    executable_path = get_executable_path()
    if not executable_path:
        print("❌ Error: Could not find loggerheads executable")
        print("   Make sure loggerheads is installed: pip3 install -e .")
        return False

    print(f"✅ Found executable: {executable_path}")

    # Create plist content
    plist_content = create_plist_content(executable_path)
    plist_path = get_plist_path()

    # Write plist file
    try:
        with open(plist_path, 'w') as f:
            f.write(plist_content)
        print(f"✅ Created LaunchAgent: {plist_path}")
    except Exception as e:
        print(f"❌ Error writing plist file: {e}")
        return False

    # Load the LaunchAgent
    try:
        subprocess.run(['launchctl', 'unload', str(plist_path)],
                      capture_output=True,
                      check=False)  # Ignore errors if not already loaded

        subprocess.run(['launchctl', 'load', str(plist_path)],
                      capture_output=True,
                      check=True)

        print("✅ LaunchAgent loaded successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error loading LaunchAgent: {e}")
        print(f"   stderr: {e.stderr.decode() if e.stderr else 'none'}")
        return False

    # Show log locations
    log_dir = Path.home() / ".loggerheads_logs"
    print(f"\n📋 Logs will be written to:")
    print(f"   Output: {log_dir / 'loggerheads.log'}")
    print(f"   Errors: {log_dir / 'loggerheads_error.log'}")

    print("\n✅ Auto-start installed! Loggerheads will now start automatically on boot.")
    print("\nTo check if it's running:")
    print("   launchctl list | grep loggerheads")
    print("\nTo view logs:")
    print(f"   tail -f {log_dir / 'loggerheads.log'}")

    return True


def uninstall_autostart():
    """Uninstall the LaunchAgent."""
    print("🗑️  Uninstalling loggerheads auto-start...")

    plist_path = get_plist_path()

    if not plist_path.exists():
        print("⚠️  Auto-start is not installed")
        return True

    # Unload the LaunchAgent
    try:
        subprocess.run(['launchctl', 'unload', str(plist_path)],
                      capture_output=True,
                      check=True)
        print("✅ LaunchAgent unloaded")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Could not unload LaunchAgent: {e}")

    # Delete the plist file
    try:
        plist_path.unlink()
        print(f"✅ Deleted: {plist_path}")
    except Exception as e:
        print(f"❌ Error deleting plist file: {e}")
        return False

    print("\n✅ Auto-start uninstalled successfully")
    return True


def check_autostart_status():
    """Check if auto-start is currently installed and running."""
    plist_path = get_plist_path()

    print("📊 Auto-start Status:")
    print("-" * 50)

    # Check if plist exists
    if plist_path.exists():
        print(f"✅ LaunchAgent installed: {plist_path}")
    else:
        print("❌ LaunchAgent not installed")
        print("\nTo install: loggerheads install")
        return

    # Check if loaded
    try:
        result = subprocess.run(['launchctl', 'list'],
                              capture_output=True,
                              text=True,
                              check=True)

        if 'com.loggerheads.autostart' in result.stdout:
            print("✅ LaunchAgent is loaded and running")

            # Get detailed status
            status_result = subprocess.run(
                ['launchctl', 'list', 'com.loggerheads.autostart'],
                capture_output=True,
                text=True,
                check=False
            )

            if status_result.returncode == 0:
                print("\nDetails:")
                for line in status_result.stdout.split('\n'):
                    if line.strip():
                        print(f"  {line}")
        else:
            print("⚠️  LaunchAgent installed but not loaded")
            print("\nTo load: launchctl load ~/Library/LaunchAgents/com.loggerheads.autostart.plist")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error checking status: {e}")

    # Show log locations
    log_dir = Path.home() / ".loggerheads_logs"
    if log_dir.exists():
        print(f"\n📋 Log files:")
        print(f"   {log_dir / 'loggerheads.log'}")
        print(f"   {log_dir / 'loggerheads_error.log'}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "install":
            install_autostart()
        elif command == "uninstall":
            uninstall_autostart()
        elif command == "status":
            check_autostart_status()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python -m loggerheads.autostart [install|uninstall|status]")
    else:
        print("Usage: python -m loggerheads.autostart [install|uninstall|status]")

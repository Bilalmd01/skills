"""Interactive setup wizard for NIMA."""
import sys
import argparse
from pathlib import Path
from ..config.auto import detect_openclaw, get_nima_config, setup_paths


def run_setup():
    """Run interactive setup wizard."""
    print("🧠 NIMA Setup Wizard")
    print("=" * 50)
    
    # Detect environment
    openclaw = detect_openclaw()
    
    if openclaw:
        print(f"✅ OpenClaw detected!")
        print(f"   Workspace: {openclaw['workspace']}")
        print(f"   Version: {openclaw.get('version', 'unknown')}")
        print()
        print("NIMA will integrate automatically with your OpenClaw installation.")
    else:
        print("ℹ️  OpenClaw not detected - running in standalone mode")
        print()
    
    # Get config
    config = get_nima_config()
    
    print(f"📁 Data directory: {config['data_dir']}")
    print(f"📁 Models directory: {config['models_dir']}")
    print()
    
    # Confirm
    response = input("Proceed with setup? [Y/n]: ").strip().lower()
    if response not in ('', 'y', 'yes'):
        print("Setup cancelled.")
        sys.exit(0)
    
    # Create paths
    print("\n🔧 Creating directories...")
    setup_paths(config)
    print("✅ Directories created")
    
    # Save config (atomic write)
    config_path = Path(config['data_dir']) / "config.json"
    from ..utils import atomic_json_save
    try:
        atomic_json_save(config, config_path)
        print(f"✅ Config saved to {config_path}")
    except OSError as e:
        print(f"Error: Failed to write config file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # OpenClaw integration
    if openclaw:
        print("\n📝 OpenClaw Integration:")
        print("   To complete setup, add to your OpenClaw agent:")
        print()
        print("   1. Message capture hook:")
        print("      python3 -m nima_core.capture_message")
        print()
        print("   2. Recall hook:")
        print("      python3 -m nima_core.recall_query")
        print()
        print("   3. Dream consolidation (cron):")
        print("      python3 -m nima_core.dream")
        print()
        print("   See README.md for detailed integration guide.")
    
    print("\n✨ Setup complete!")
    print(f"   Mode: {config['mode']}")
    print(f"   Ready to use NIMA 🧠")


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(description="NIMA - Noosphere Integrated Memory Architecture")
    parser.add_argument('command', nargs='?', default='init', choices=['init'], 
                       help='Command to run (default: init)')
    
    args = parser.parse_args()
    
    if args.command == 'init':
        run_setup()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Robbie OS Command Line Interface

Direct interface to Robbie OS - no obfuscation, just clarity.
"""

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Optional

from robbie_os import RobbieOS


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def print_banner():
    """Print Robbie OS banner."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                 ROBBIE OS                                    ║
║                          Sovereign Operating System                         ║
║                             Founded by Robbie George                        ║
║                                                                              ║
║  Principles: Clarity • Sovereignty • Direct Execution • No Obfuscation      ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")


def handle_status_command(os_instance: RobbieOS, args) -> None:
    """Handle status command."""
    status = os_instance.get_status()
    print(json.dumps(status, indent=2))


def handle_health_command(os_instance: RobbieOS, args) -> None:
    """Handle health check command."""
    health = os_instance.run_health_check()
    print(json.dumps(health, indent=2))
    
    if not health['overall'] == 'healthy':
        print(f"\n⚠️  System Health: {health['overall'].upper()}")
        if health['issues']:
            print("Issues:")
            for issue in health['issues']:
                print(f"  • {issue}")
        sys.exit(1)
    else:
        print("\n✅ System is healthy")


def handle_execute_command(os_instance: RobbieOS, args) -> None:
    """Handle execute command."""
    command = ' '.join(args.command)
    
    print(f"Executing: {command}")
    result = os_instance.execute_command(command)
    
    if result['status'] == 'success':
        print(f"✅ Result: {result['result']}")
        print(f"Execution time: {result['execution_time']:.3f}s")
    elif result['status'] == 'blocked':
        print(f"🚫 Command blocked: {result['error']}")
        sys.exit(1)
    else:
        print(f"❌ Error: {result['error']}")
        print(f"Execution time: {result['execution_time']:.3f}s")
        sys.exit(1)


def handle_memory_command(os_instance: RobbieOS, args) -> None:
    """Handle memory commands."""
    if args.memory_action == 'status':
        status = os_instance.memory.get_status()
        print(json.dumps(status, indent=2))
    
    elif args.memory_action == 'stats':
        stats = os_instance.memory.get_stats()
        print(json.dumps(stats, indent=2))
    
    elif args.memory_action == 'history':
        limit = getattr(args, 'limit', 10)
        history = os_instance.memory.get_execution_history(limit)
        print(json.dumps(history, indent=2))
    
    elif args.memory_action == 'patterns':
        patterns = os_instance.memory.get_learned_patterns()
        print(json.dumps(patterns, indent=2))


def handle_seedgrid_command(os_instance: RobbieOS, args) -> None:
    """Handle seedgrid commands."""
    if args.seedgrid_action == 'status':
        status = os_instance.seedgrid.get_status()
        print(json.dumps(status, indent=2))
    
    elif args.seedgrid_action == 'nodes':
        nodes = os_instance.seedgrid.list_nodes()
        print(json.dumps(nodes, indent=2))
        
        # Summary
        print(f"\nTotal nodes: {len(nodes)}")
        if nodes:
            by_status = {}
            by_type = {}
            for node in nodes:
                status = node['status']
                node_type = node['node_type']
                by_status[status] = by_status.get(status, 0) + 1
                by_type[node_type] = by_type.get(node_type, 0) + 1
            
            print(f"By status: {dict(by_status)}")
            print(f"By type: {dict(by_type)}")


def handle_sentinel_command(os_instance: RobbieOS, args) -> None:
    """Handle sentinel commands."""
    if args.sentinel_action == 'status':
        status = os_instance.sentinel.get_status()
        print(json.dumps(status, indent=2))
    
    elif args.sentinel_action == 'rules':
        rules = os_instance.sentinel.get_rules()
        print(json.dumps(rules, indent=2))
        print(f"\nTotal rules: {len(rules)}")
    
    elif args.sentinel_action == 'violations':
        limit = getattr(args, 'limit', 10)
        violations = os_instance.sentinel.get_violation_log(limit)
        print(json.dumps(violations, indent=2))
    
    elif args.sentinel_action == 'integrity':
        report = os_instance.sentinel.validate_system_integrity()
        print(json.dumps(report, indent=2))
        
        if report['overall_status'] != 'healthy':
            print(f"\n⚠️  Integrity Status: {report['overall_status'].upper()}")
            if report['issues']:
                print("Issues:")
                for issue in report['issues']:
                    print(f"  • {issue}")


def handle_failures_command(os_instance: RobbieOS, args) -> None:
    """Handle failure detector commands."""
    if args.failures_action == 'status':
        status = os_instance.failure_detector.get_status()
        print(json.dumps(status, indent=2))
    
    elif args.failures_action == 'patterns':
        min_severity = getattr(args, 'min_severity', 0.0)
        limit = getattr(args, 'limit', 10)
        patterns = os_instance.failure_detector.get_anomaly_patterns(min_severity, limit)
        print(json.dumps(patterns, indent=2))
        print(f"\nShowing {len(patterns)} anomaly patterns (min severity: {min_severity})")
    
    elif args.failures_action == 'insights':
        insights = os_instance.failure_detector.get_failure_insights()
        print(json.dumps(insights, indent=2))
        
        # Print summary
        summary = insights['summary']
        print(f"\n📊 Failure Summary:")
        print(f"Total failures: {summary['total_failures']}")
        print(f"Average failure rate: {summary['avg_failure_rate']:.2f}/hour")
        print(f"Detected patterns: {summary['total_patterns']}")
        
        if insights['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in insights['recommendations']:
                print(f"  • {rec}")


def handle_interactive_mode(os_instance: RobbieOS) -> None:
    """Handle interactive mode."""
    print("Robbie OS Interactive Mode")
    print("Type 'help' for commands, 'exit' to quit")
    print()
    
    while True:
        try:
            command = input("robbie> ").strip()
            
            if not command:
                continue
            
            if command.lower() in ['exit', 'quit']:
                break
            
            if command.lower() == 'help':
                print("""
Available commands:
  status                 - Show system status
  health                 - Run health check
  memory status          - Show memory status
  seedgrid nodes         - Show nodes
  sentinel rules         - Show ethical rules
  failures insights      - Show failure insights
  <any command>          - Execute directly
  exit                   - Quit interactive mode
""")
                continue
            
            # Execute command
            result = os_instance.execute_command(command)
            
            if result['status'] == 'success':
                print(f"✅ {result['result']}")
            elif result['status'] == 'blocked':
                print(f"🚫 {result['error']}")
            else:
                print(f"❌ {result['error']}")
        
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Robbie OS - Sovereign Operating System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-c', '--config', 
                       help='Configuration file path')
    parser.add_argument('-v', '--verbose', 
                       action='store_true', 
                       help='Enable verbose logging')
    parser.add_argument('--no-banner', 
                       action='store_true', 
                       help='Skip banner display')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    subparsers.add_parser('status', help='Show system status')
    
    # Health command
    subparsers.add_parser('health', help='Run health check')
    
    # Execute command
    exec_parser = subparsers.add_parser('exec', help='Execute a command')
    exec_parser.add_argument('command', nargs='+', help='Command to execute')
    
    # Memory commands
    memory_parser = subparsers.add_parser('memory', help='Memory operations')
    memory_parser.add_argument('memory_action', 
                              choices=['status', 'stats', 'history', 'patterns'],
                              help='Memory action')
    memory_parser.add_argument('--limit', type=int, default=10,
                              help='Limit results (for history)')
    
    # SeedGrid commands
    seedgrid_parser = subparsers.add_parser('seedgrid', help='SeedGrid operations')
    seedgrid_parser.add_argument('seedgrid_action', 
                                choices=['status', 'nodes'],
                                help='SeedGrid action')
    
    # Sentinel commands
    sentinel_parser = subparsers.add_parser('sentinel', help='Sentinel operations')
    sentinel_parser.add_argument('sentinel_action',
                               choices=['status', 'rules', 'violations', 'integrity'],
                               help='Sentinel action')
    sentinel_parser.add_argument('--limit', type=int, default=10,
                               help='Limit results (for violations)')
    
    # Failure detector commands
    failures_parser = subparsers.add_parser('failures', help='Failure detection operations')
    failures_parser.add_argument('failures_action',
                                choices=['status', 'patterns', 'insights'],
                                help='Failure detector action')
    failures_parser.add_argument('--min-severity', type=float, default=0.0,
                                help='Minimum severity for patterns')
    failures_parser.add_argument('--limit', type=int, default=10,
                                help='Limit results')
    
    # Interactive mode
    subparsers.add_parser('interactive', help='Enter interactive mode')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Show banner
    if not args.no_banner:
        print_banner()
    
    # Initialize Robbie OS
    try:
        print("Initializing Robbie OS...")
        with RobbieOS(args.config) as os_instance:
            print("✅ Robbie OS initialized successfully")
            
            # Handle commands
            if args.command == 'status':
                handle_status_command(os_instance, args)
            
            elif args.command == 'health':
                handle_health_command(os_instance, args)
            
            elif args.command == 'exec':
                handle_execute_command(os_instance, args)
            
            elif args.command == 'memory':
                handle_memory_command(os_instance, args)
            
            elif args.command == 'seedgrid':
                handle_seedgrid_command(os_instance, args)
            
            elif args.command == 'sentinel':
                handle_sentinel_command(os_instance, args)
            
            elif args.command == 'failures':
                handle_failures_command(os_instance, args)
            
            elif args.command == 'interactive':
                handle_interactive_mode(os_instance)
            
            else:
                parser.print_help()
    
    except KeyboardInterrupt:
        print("\nShutdown requested")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    print("Robbie OS shutdown complete")


if __name__ == '__main__':
    main()
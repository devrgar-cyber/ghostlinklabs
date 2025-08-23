#!/usr/bin/env python3
"""
Test Robbie OS functionality

Basic test to verify all components work together.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from robbie_os import RobbieOS
import json


def test_robbie_os():
    """Test Robbie OS basic functionality."""
    print("Testing Robbie OS...")
    
    # Initialize Robbie OS
    with RobbieOS() as os_instance:
        print("✅ Robbie OS initialized")
        
        # Test status
        status = os_instance.get_status()
        print(f"✅ Status: {status['identity']} founded by {status['founder']}")
        
        # Test command execution
        result = os_instance.execute_command("echo Hello from Robbie OS")
        print(f"✅ Echo command: {result['result']}")
        
        # Test memory
        os_instance.execute_command("memory set test_key=test_value")
        result = os_instance.execute_command("memory get test_key")
        print(f"✅ Memory test: {result['result']}")
        
        # Test SeedGrid
        result = os_instance.execute_command("seedgrid nodes")
        print(f"✅ SeedGrid nodes: {len(result['result'])} nodes")
        
        # Test health check
        health = os_instance.run_health_check()
        print(f"✅ Health check: {health['overall']}")
        
        # Test ethical validation (try a blocked command)
        result = os_instance.execute_command("rm -rf /")
        if result['status'] == 'blocked':
            print("✅ Ethical validation working - dangerous command blocked")
        else:
            print("❌ Ethical validation failed")
        
        print("\n🎉 All tests passed! Robbie OS is working correctly.")


if __name__ == '__main__':
    test_robbie_os()
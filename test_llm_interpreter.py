#!/usr/bin/env python3

"""
Test script for LLMunix LLM Interpreter

This script validates the LLM interpreter functionality with environment
detection and autonomous execution capabilities.
"""

import os
import sys
import time
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def test_environment_setup():
    """Test environment setup and dependencies"""
    print("🧪 Testing Environment Setup")
    print("-" * 40)
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"✅ Python version: {python_version}")
    
    # Check if API key is available
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OpenAI API key required.")
        print("💡 Set OPENAI_API_KEY in .env file")
        return False
    else:
        print("✅ OpenAI API key found in environment")
    
    # Test required imports
    try:
        from llm_interpreter import LLMunixInterpreter
        print("✅ LLMunix interpreter module imported")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Test OpenAI client
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized")
    except Exception as e:
        print(f"❌ OpenAI client failed: {e}")
        return False
    
    return True

def test_interpreter_initialization():
    """Test interpreter initialization"""
    print("\\n🤖 Testing Interpreter Initialization")
    print("-" * 40)
    
    try:
        from llm_interpreter import LLMunixInterpreter
        
        # Test initialization
        interpreter = LLMunixInterpreter(model="gpt-4o")
        print("✅ Interpreter initialized successfully")
        
        # Check properties
        print(f"✅ Model: {interpreter.model}")
        print(f"✅ Workspace: {interpreter.workspace_dir}")
        print(f"✅ State dir: {interpreter.state_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False

def test_docker_availability():
    """Test Docker availability for tool execution"""
    print("\\n🐳 Testing Docker Availability")
    print("-" * 40)
    
    import subprocess
    
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Docker available: {result.stdout.strip()}")
            
            # Test container creation capability
            try:
                test_result = subprocess.run([
                    'docker', 'run', '--rm', 'alpine:latest', 'echo', 'test'
                ], capture_output=True, text=True, timeout=30)
                
                if test_result.returncode == 0:
                    print("✅ Docker container execution works")
                    return True
                else:
                    print(f"⚠️  Docker available but container test failed: {test_result.stderr}")
                    return False
                    
            except Exception as e:
                print(f"⚠️  Docker available but test failed: {e}")
                return False
                
        else:
            print("⚠️  Docker not available - will run in simulation mode")
            return False
            
    except FileNotFoundError:
        print("⚠️  Docker not found - will run in simulation mode")
        return False
    except Exception as e:
        print(f"⚠️  Docker test failed: {e}")
        return False

def test_simple_execution():
    """Test simple goal execution"""
    print("\\n🎯 Testing Simple Execution")
    print("-" * 40)
    
    try:
        from llm_interpreter import LLMunixInterpreter
        
        interpreter = LLMunixInterpreter(model="gpt-4o")
        
        # Test simple goal
        test_goal = "Create a simple text file called hello.txt with the content 'Hello LLMunix!'"
        
        print(f"🎯 Test goal: {test_goal}")
        print("⏳ Starting execution (this may take a moment)...")
        
        # Execute goal
        interpreter.execute(test_goal)
        
        # Check if workspace was created
        if interpreter.workspace_dir.exists():
            print("✅ Workspace created")
            
            # Check state files
            state_files = ['plan.md', 'history.md', 'context.md', 'constraints.md', 'variables.json']
            for state_file in state_files:
                file_path = interpreter.state_dir / state_file
                if file_path.exists():
                    print(f"✅ State file created: {state_file}")
                else:
                    print(f"⚠️  State file missing: {state_file}")
            
            # Check for execution artifacts
            hello_file = interpreter.workspace_dir / "hello.txt"
            if hello_file.exists():
                content = hello_file.read_text()
                print(f"✅ Output file created: hello.txt")
                print(f"📄 Content: {content}")
            else:
                print("⚠️  Expected output file not found")
            
            return True
        else:
            print("❌ Workspace not created")
            return False
            
    except Exception as e:
        print(f"❌ Execution test failed: {e}")
        return False

def test_environment_detection():
    """Test environment detection capabilities"""
    print("\\n🔍 Testing Environment Detection")
    print("-" * 40)
    
    # This test only works if Docker is available
    if not test_docker_availability():
        print("⚠️  Skipping environment detection test (Docker not available)")
        return True
    
    try:
        from llm_interpreter import LLMunixInterpreter
        
        interpreter = LLMunixInterpreter(model="gpt-4o")
        
        # Setup Docker environment
        interpreter._setup_docker()
        
        if hasattr(interpreter, 'container_name') and interpreter.container_name:
            print(f"✅ Container created: {interpreter.container_name}")
            
            # Test environment detection
            interpreter._detect_container_environment()
            
            # Check environment info
            if hasattr(interpreter, 'context') and interpreter.context and interpreter.context.environment_info:
                env_info = interpreter.context.environment_info
                print(f"✅ Tools detected: {len(env_info.get('available_tools', []))}")
                print(f"✅ Package managers: {env_info.get('package_managers', [])}")
                print(f"✅ OS detected: {env_info.get('distro', 'Unknown')}")
                
                # Cleanup
                interpreter._cleanup_execution()
                return True
            else:
                print("❌ Environment detection failed")
                return False
        else:
            print("❌ Container creation failed")
            return False
            
    except Exception as e:
        print(f"❌ Environment detection test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 LLMunix LLM Interpreter Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Interpreter Initialization", test_interpreter_initialization),
        ("Docker Availability", test_docker_availability),
        ("Environment Detection", test_environment_detection),
        ("Simple Execution", test_simple_execution),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\\n🎯 Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! LLM interpreter is ready.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
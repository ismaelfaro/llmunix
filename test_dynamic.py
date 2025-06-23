#!/usr/bin/env python3

"""
Test Script for Dynamic Component Creation

This script tests whether the LLM interpreter can dynamically create 
markdown components during execution based on user goals.
"""

import os
import sys
from pathlib import Path
from llm_interpreter import LLMunixInterpreter

def test_dynamic_component_creation():
    """Test if the interpreter creates components dynamically"""
    
    print("="*60)
    print("🧪 Testing Dynamic Component Creation")
    print("="*60)
    
    # Initialize interpreter
    interpreter = LLMunixInterpreter()
    
    # Clean workspace for fresh test
    interpreter._clean_workspace()
    
    # Check initial state - no sentiment analysis components
    components_dir = Path("components")
    initial_files = list(components_dir.rglob("*.md"))
    print(f"📁 Initial component files: {len(initial_files)}")
    
    # Check SmartLibrary for sentiment capabilities
    smart_lib = Path("system/SmartLibrary.md")
    initial_lib_content = smart_lib.read_text()
    has_sentiment = "sentiment" in initial_lib_content.lower()
    print(f"🔍 Sentiment analysis in SmartLibrary: {has_sentiment}")
    
    if has_sentiment:
        print("⚠️  Warning: Sentiment analysis already exists - test may not show dynamic creation")
    
    # Define the test goal that requires missing capabilities
    test_goal = """Analyze the sentiment and key topics from TechCrunch AI news, then create a report showing whether the coverage is positive or negative about AI developments. I need to understand the emotional tone of the articles."""
    
    print(f"\n🎯 Test Goal: {test_goal}")
    print("\n🚀 Starting execution...")
    
    try:
        # Execute the goal - this should trigger dynamic component creation
        interpreter.execute(test_goal, cleanup_after=False)
        
        print("\n✅ Execution completed!")
        
        # Check what was created
        final_files = list(components_dir.rglob("*.md"))
        new_files = set(final_files) - set(initial_files)
        
        print(f"\n📊 Results:")
        print(f"   Initial files: {len(initial_files)}")
        print(f"   Final files: {len(final_files)}")
        print(f"   New files created: {len(new_files)}")
        
        if new_files:
            print(f"\n📝 New components created:")
            for file in new_files:
                print(f"   ✨ {file}")
                
        # Check SmartLibrary updates
        final_lib_content = smart_lib.read_text()
        lib_changed = len(final_lib_content) != len(initial_lib_content)
        print(f"\n📚 SmartLibrary updated: {lib_changed}")
        
        # Check workspace outputs
        workspace_files = list(Path("workspace").rglob("*"))
        workspace_count = len([f for f in workspace_files if f.is_file()])
        print(f"📂 Workspace files created: {workspace_count}")
        
        # Analyze what was created
        if new_files:
            print(f"\n🔍 Component Analysis:")
            for file in new_files:
                content = file.read_text()
                if "sentiment" in content.lower():
                    print(f"   📊 {file.name}: Contains sentiment analysis logic")
                if "comparative" in content.lower() or "comparison" in content.lower():
                    print(f"   📈 {file.name}: Contains comparative analysis logic")
                if "TOOL" in content:
                    print(f"   🔧 {file.name}: Tool component")
                if "AGENT" in content:
                    print(f"   🤖 {file.name}: Agent component")
        
        return len(new_files) > 0
        
    except Exception as e:
        print(f"\n❌ Execution failed: {e}")
        return False

def check_execution_details():
    """Check the execution details in workspace"""
    print(f"\n🔍 Checking execution details...")
    
    workspace = Path("workspace")
    if not workspace.exists():
        print("   ⚠️  No workspace found")
        return
    
    # Check state files
    state_dir = workspace / "state"
    if state_dir.exists():
        print(f"   📁 State directory: {state_dir}")
        state_files = list(state_dir.glob("*.md")) + list(state_dir.glob("*.json"))
        for state_file in state_files:
            print(f"      📄 {state_file.name}")
    
    # Check if any components were actually created and used
    history_file = state_dir / "history.md" if state_dir.exists() else None
    if history_file and history_file.exists():
        history = history_file.read_text()
        if "SentimentAnalysis" in history or "sentiment" in history.lower():
            print("   ✅ Evidence of sentiment analysis in execution history")
        if "component" in history.lower() and "create" in history.lower():
            print("   ✅ Evidence of component creation in execution history")

if __name__ == "__main__":
    try:
        success = test_dynamic_component_creation()
        check_execution_details()
        
        print(f"\n" + "="*60)
        if success:
            print("🎉 SUCCESS: Dynamic component creation working!")
            print("The LLM interpreter successfully created new markdown components during execution.")
        else:
            print("⚠️  INCONCLUSIVE: No new components detected.")
            print("This could mean:")
            print("   1. The goal was solved with existing components")
            print("   2. Components were created but not detected")
            print("   3. Dynamic creation needs debugging")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)
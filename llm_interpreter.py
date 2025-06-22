#!/usr/bin/env python3

"""
LLMunix LLM Interpreter - Lightweight Runtime for Pure Markdown OS

This is a minimal runtime that delegates all logic to markdown-defined agents
and tools. The interpreter serves as a bridge between the command line and
the LLMunix markdown specifications.

Key Features:
- No hardcoded logic - everything delegated to markdown agents/tools
- Docker/CLI tool detection and mapping
- SystemAgent.md orchestrates all execution
- Pure markdown-driven decision making
- Lightweight bridge to host system tools

The runtime reads markdown specifications and lets the SystemAgent make all decisions.
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# Environment setup
from dotenv import load_dotenv
load_dotenv()

# OpenAI client
from openai import OpenAI

@dataclass
class ExecutionContext:
    """Maintains execution state and configuration"""
    goal: str
    workspace_dir: Path
    state_dir: Path
    container_name: Optional[str] = None
    environment_info: Dict[str, Any] = None
    execution_history: List[Dict] = None
    
    def __post_init__(self):
        if self.execution_history is None:
            self.execution_history = []
        if self.environment_info is None:
            self.environment_info = {}

class LLMunixInterpreter:
    """
    LLMunix LLM Interpreter - Lightweight Runtime
    
    Minimal runtime that delegates all logic to markdown-defined SystemAgent.
    This class only handles basic setup and environment detection.
    """
    
    def __init__(self, model: str = "gpt-4o"):
        """Initialize the LLM interpreter"""
        
        # Validate OpenAI API key
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        
        # Setup paths
        self.llmunix_root = Path(__file__).parent
        self.workspace_dir = self.llmunix_root / "workspace"
        self.state_dir = self.workspace_dir / "state"
        
        # Execution context
        self.context: Optional[ExecutionContext] = None
        
        print(f"🤖 LLMunix LLM Interpreter initialized")
        print(f"📁 LLMunix root: {self.llmunix_root}")
        print(f"🏗️  Workspace: {self.workspace_dir}")
        print(f"🧠 Model: {self.model}")
    
    def boot(self):
        """Boot LLMunix operating system"""
        print("\n" + "="*60)
        print("██╗     ██╗     ███╗   ███╗██╗   ██╗███╗   ██╗██╗██╗  ██╗")
        print("██║     ██║     ████╗ ████║██║   ██║████╗  ██║██║╚██╗██╔╝")
        print("██║     ██║     ██╔████╔██║██║   ██║██╔██╗ ██║██║ ╚███╔╝ ")
        print("██║     ██║     ██║╚██╔╝██║██║   ██║██║╚██╗██║██║ ██╔██╗ ")
        print("███████╗███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║██╔╝ ██╗")
        print("╚══════╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝")
        print("                Pure Markdown Operating System v1.0")
        print("                    LLM Interpreter Runtime")
        print("="*60)
        
        # Clean workspace
        self._clean_workspace()
        
        # Setup Docker environment if available
        self._setup_docker()
        
        print("\n🎯 LLMunix is ready for autonomous execution!")
        print("\nExample commands:")
        print('  ./llmunix-llm execute: "Create a Python calculator"')
        print('  ./llmunix-llm execute: "Research AI trends and create summary"')
        print('  ./llmunix-llm execute: "Fetch data from URL and analyze"')
        print("\n" + "="*60 + "\n")
    
    def execute(self, goal: str):
        """Execute a goal by delegating to SystemAgent.md"""
        
        print(f"🎯 Executing goal: {goal}")
        print("="*60)
        
        # Initialize execution context
        self.context = ExecutionContext(
            goal=goal,
            workspace_dir=self.workspace_dir,
            state_dir=self.state_dir,
            container_name=getattr(self, 'container_name', None)
        )
        
        # Setup workspace and state
        self._setup_workspace()
        
        # Detect environment if Docker is available
        if self.context.container_name:
            self._detect_container_environment()
        
        # Delegate execution to SystemAgent
        try:
            self._delegate_to_system_agent()
        except Exception as e:
            print(f"❌ Execution failed: {e}")
            self._log_error(str(e))
        finally:
            self._cleanup_execution()
    
    def _setup_workspace(self):
        """Setup modular workspace structure"""
        print("🏗️  Setting up modular workspace...")
        
        # Create directories
        self.workspace_dir.mkdir(exist_ok=True)
        self.state_dir.mkdir(exist_ok=True)
        
        # Initialize state files
        state_files = {
            'plan.md': f"# Execution Plan\n\n**Goal:** {self.context.goal}\n\n## Status\nInitializing...\n",
            'context.md': "# Execution Context\n\n## Knowledge Accumulation\n\n",
            'history.md': f"# Execution History\n\n**Started:** {datetime.now().isoformat()}\n\n",
            'constraints.md': "# Behavioral Constraints\n\n## Initial Settings\n- priority: balanced\n- error_tolerance: moderate\n",
            'variables.json': json.dumps({"goal": self.context.goal, "start_time": datetime.now().isoformat()}, indent=2)
        }
        
        for filename, content in state_files.items():
            file_path = self.state_dir / filename
            file_path.write_text(content, encoding='utf-8')
        
        print(f"✅ Workspace setup complete: {self.workspace_dir}")
    
    def _setup_docker(self):
        """Setup Docker environment for tool execution"""
        try:
            # Check if Docker is available
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                print("⚠️  Docker not available - running in simulation mode")
                return
            
            print("🐳 Docker detected - setting up execution environment...")
            
            # Create and start container
            container_name = f"llmunix-{int(time.time())}"
            
            # Mount workspace directory for file access from outside container
            workspace_mount = f"{self.workspace_dir}:/workspace"
            
            # Use Alpine Linux for lightweight container with package manager detection
            run_command = [
                'docker', 'run', '-d', '--name', container_name,
                '-v', workspace_mount,
                '-w', '/workspace',
                'alpine:latest',
                'sh', '-c', 'apk add --no-cache python3 py3-pip curl bash && pip install requests beautifulsoup4 && sleep 3600'
            ]
            
            result = subprocess.run(run_command, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                self.container_name = container_name
                print(f"✅ Container '{container_name}' created and running")
                time.sleep(5)  # Allow time for package installation
            else:
                print(f"⚠️  Failed to create container: {result.stderr}")
                
        except Exception as e:
            print(f"⚠️  Docker setup failed: {e}")
    
    def _detect_container_environment(self):
        """Detect available tools and environment in the container"""
        if not hasattr(self, 'container_name') or not self.container_name:
            return
            
        print("🔍 Detecting container environment...")
        
        # Common tools to check
        tools_to_check = [
            'python3', 'python', 'pip', 'pip3', 'curl', 'wget', 'bash', 'sh',
            'git', 'nano', 'vim', 'cat', 'grep', 'sed', 'awk', 'jq'
        ]
        
        # Package managers to check
        package_managers = ['apt-get', 'yum', 'apk', 'dnf', 'zypper']
        
        available_tools = []
        available_package_managers = []
        
        # Check tools
        for tool in tools_to_check:
            try:
                result = subprocess.run([
                    'docker', 'exec', self.container_name, 'which', tool
                ], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    available_tools.append(tool)
            except:
                pass
        
        # Check package managers
        for pm in package_managers:
            try:
                result = subprocess.run([
                    'docker', 'exec', self.container_name, 'which', pm
                ], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    available_package_managers.append(pm)
            except:
                pass
        
        # Get OS information
        os_info = self._get_os_info()
        distro_info = self._detect_distro()
        
        # Store environment information
        self.context.environment_info = {
            'available_tools': available_tools,
            'package_managers': available_package_managers,
            'os_info': os_info,
            'distro': distro_info,
            'container_name': self.container_name
        }
        
        # Create environment documentation
        self._create_environment_doc()
        
        print(f"✅ Environment detected: {len(available_tools)} tools, {len(available_package_managers)} package managers")
        print(f"🐧 OS: {distro_info}")
    
    def _get_os_info(self):
        """Get OS information from container"""
        try:
            result = subprocess.run([
                'docker', 'exec', self.container_name, 'uname', '-a'
            ], capture_output=True, text=True, timeout=5)
            return result.stdout.strip() if result.returncode == 0 else "Unknown"
        except:
            return "Unknown"
    
    def _detect_distro(self):
        """Detect Linux distribution"""
        distro_files = [
            ('/etc/alpine-release', 'Alpine Linux'),
            ('/etc/os-release', 'os-release'),
            ('/etc/redhat-release', 'Red Hat based'),
            ('/etc/debian_version', 'Debian based')
        ]
        
        for file_path, distro_type in distro_files:
            try:
                result = subprocess.run([
                    'docker', 'exec', self.container_name, 'cat', file_path
                ], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    if file_path == '/etc/alpine-release':
                        return f"Alpine Linux v{result.stdout.strip()}"
                    elif file_path == '/etc/os-release':
                        # Parse os-release for detailed info
                        for line in result.stdout.split('\n'):
                            if line.startswith('PRETTY_NAME='):
                                return line.split('=')[1].strip('\"')
                    else:
                        return f"{distro_type}: {result.stdout.strip()}"
            except:
                pass
        
        return "Unknown Linux distribution"
    
    def _create_environment_doc(self):
        """Create environment documentation for LLM reference"""
        env_info = self.context.environment_info
        
        doc_content = f"""# Container Environment Detection

## Available Tools
{', '.join(env_info.get('available_tools', []))}

## Package Managers  
{', '.join(env_info.get('package_managers', []))}

## OS Information
{env_info.get('os_info', 'Unknown')}

## Distribution
{env_info.get('distro', 'Unknown')}

## Recommendations for SystemAgent
- Use these available tools: {', '.join(env_info.get('available_tools', [])[:10])}
- For package installation, use: {env_info.get('package_managers', ['unknown'])[0] if env_info.get('package_managers') else 'unknown'}
- This is a {env_info.get('distro', 'unknown')} system

## Notes
- Always check tool availability before using
- Use appropriate package manager for this system
- Consider OS-specific command variations
"""
        
        env_file = self.state_dir / "container_environment.md"
        env_file.write_text(doc_content, encoding='utf-8')
        print(f"📋 Environment documentation created: {env_file}")
    
    def _delegate_to_system_agent(self):
        """Delegate execution to SystemAgent.md"""
        print("🧠 Delegating to SystemAgent.md...")
        
        # Read SystemAgent specification
        system_agent_path = self.llmunix_root / "system" / "SystemAgent.md"
        if not system_agent_path.exists():
            raise FileNotFoundError(f"SystemAgent.md not found at {system_agent_path}")
        
        system_agent_spec = system_agent_path.read_text(encoding='utf-8')
        
        # Build execution context for SystemAgent
        environment_context = self._build_environment_context()
        available_tools = self._get_available_cli_tools()
        
        # Create execution prompt that delegates to SystemAgent
        prompt = f"""You are acting as the SystemAgent from this specification:

{system_agent_spec}

EXECUTION CONTEXT:
- Goal: {self.context.goal}
- Workspace: {self.workspace_dir}
- State directory: {self.state_dir}
- Container: {self.context.container_name if self.context.container_name else "None (host system)"}

ENVIRONMENT:
{environment_context}

AVAILABLE CLI TOOLS:
{available_tools}

WORKSPACE STATE FILES:
{self._list_workspace_files()}

Execute the goal by following the SystemAgent specification. You have access to:
1. All CLI tools available in the environment
2. File operations in the workspace
3. Container commands if available
4. The modular state management system

Begin execution according to the SystemAgent specification."""

        # Execute via SystemAgent
        response = self._call_llm(prompt, max_tokens=3000)
        
        # Log the SystemAgent response
        self._log_execution_step("SystemAgent Execution", response)
        
        print("✅ Execution delegated to SystemAgent")
    
    def _get_available_cli_tools(self) -> str:
        """Get list of available CLI tools"""
        if self.context.environment_info:
            tools = self.context.environment_info.get('available_tools', [])
            return f"Container tools: {', '.join(tools)}"
        else:
            # Host system tools
            common_tools = ['python3', 'curl', 'cat', 'echo', 'mkdir', 'ls', 'grep', 'sed']
            return f"Host system tools: {', '.join(common_tools)} (detection needed)"
    
    def _list_workspace_files(self) -> str:
        """List current workspace files"""
        files = []
        for file_path in self.workspace_dir.rglob('*'):
            if file_path.is_file():
                rel_path = file_path.relative_to(self.workspace_dir)
                files.append(str(rel_path))
        return "\n".join(files) if files else "No files in workspace"
    
    # Utility methods
    
    def _build_system_context(self) -> str:
        """Build system context for LLM"""
        return f"""
        - LLMunix Pure Markdown Operating System
        - Runtime: LLM Interpreter (lightweight)
        - Workspace: {self.workspace_dir}
        - State management: {self.state_dir}
        - Docker available: {hasattr(self, 'container_name')}
        """
    
    def _build_environment_context(self) -> str:
        """Build environment context for LLM"""
        if not self.context.environment_info:
            return "Environment: Not detected (simulation mode)"
        
        env = self.context.environment_info
        return f"""
        Available tools: {', '.join(env.get('available_tools', [])[:10])}
        Package managers: {', '.join(env.get('package_managers', []))}
        OS: {env.get('distro', 'Unknown')}
        Container: {env.get('container_name', 'None')}
        """
    
    def _call_llm(self, prompt: str, max_tokens: int = 1000) -> str:
        """Call OpenAI LLM with prompt"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            error_msg = f"LLM call failed: {e}"
            print(f"❌ {error_msg}")
            return f"ERROR: {error_msg}"
    
    def _update_state_file(self, filename: str, content: str):
        """Update a state file"""
        file_path = self.state_dir / filename
        file_path.write_text(content, encoding='utf-8')
    
    def _read_state_file(self, filename: str) -> str:
        """Read a state file"""
        file_path = self.state_dir / filename
        return file_path.read_text(encoding='utf-8') if file_path.exists() else ""
    
    def _log_execution_step(self, step: str, content: str):
        """Log an execution step"""
        timestamp = datetime.now().isoformat()
        log_entry = f"\n## {step} - {timestamp}\n\n{content}\n"
        
        history_file = self.state_dir / "history.md"
        current_history = history_file.read_text(encoding='utf-8') if history_file.exists() else ""
        updated_history = current_history + log_entry
        
        history_file.write_text(updated_history, encoding='utf-8')
    
    def _update_context(self, content: str):
        """Update execution context"""
        timestamp = datetime.now().isoformat()
        context_entry = f"\n**{timestamp}:** {content}\n"
        
        context_file = self.state_dir / "context.md"
        current_context = context_file.read_text(encoding='utf-8') if context_file.exists() else ""
        updated_context = current_context + context_entry
        
        context_file.write_text(updated_context, encoding='utf-8')
    
    def _log_error(self, error: str):
        """Log an error"""
        self._log_execution_step("ERROR", error)
    
    def _clean_workspace(self):
        """Clean workspace for fresh execution"""
        import shutil
        
        if self.workspace_dir.exists():
            shutil.rmtree(self.workspace_dir)
        
        self.workspace_dir.mkdir(exist_ok=True)
        print("🧹 Workspace cleaned")
    
    def _cleanup_execution(self):
        """Cleanup after execution"""
        if hasattr(self, 'container_name') and self.container_name:
            try:
                subprocess.run(['docker', 'stop', self.container_name], 
                             capture_output=True, timeout=30)
                subprocess.run(['docker', 'rm', self.container_name], 
                             capture_output=True, timeout=30)
                print(f"🧹 Container {self.container_name} cleaned up")
            except:
                pass

def main():
    """Main entry point for the LLM interpreter"""
    import argparse
    
    parser = argparse.ArgumentParser(description='LLMunix LLM Interpreter - Lightweight Runtime')
    parser.add_argument('command', choices=['boot', 'execute'], help='Command to run')
    parser.add_argument('goal', nargs='?', help='Goal to execute (for execute command)')
    parser.add_argument('--model', default='gpt-4o', help='OpenAI model to use')
    
    args = parser.parse_args()
    
    try:
        interpreter = LLMunixInterpreter(model=args.model)
        
        if args.command == 'boot':
            interpreter.boot()
        elif args.command == 'execute':
            if not args.goal:
                print("❌ Goal required for execute command")
                sys.exit(1)
            interpreter.execute(args.goal)
            
    except Exception as e:
        print(f"❌ Interpreter failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
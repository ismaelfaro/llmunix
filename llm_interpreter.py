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
        """Delegate execution to SystemAgent.md with real tool execution loop"""
        print("🧠 Delegating to SystemAgent.md...")
        
        # Read SystemAgent specification
        system_agent_path = self.llmunix_root / "system" / "SystemAgent.md"
        if not system_agent_path.exists():
            raise FileNotFoundError(f"SystemAgent.md not found at {system_agent_path}")
        
        system_agent_spec = system_agent_path.read_text(encoding='utf-8')
        
        # Initialize execution context
        execution_context = self._build_full_execution_context()
        
        # Start agentic execution loop
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            print(f"🔄 Execution iteration {iteration}")
            
            # Build current prompt with context
            prompt = self._build_iteration_prompt(system_agent_spec, execution_context, iteration)
            
            # Get LLM response
            response = self._call_llm(prompt, max_tokens=2000)
            
            # Log the response
            self._log_execution_step(f"SystemAgent Iteration {iteration}", response)
            
            # Parse and execute any tool calls from the response
            tool_results = self._extract_and_execute_tools(response)
            
            # Update execution context with results
            execution_context = self._update_execution_context(execution_context, response, tool_results)
            
            # Check if execution is complete
            if self._is_execution_complete(response, tool_results):
                print("✅ Execution completed successfully")
                break
            
            # Update state files
            self._update_state_with_context(execution_context)
        
        if iteration >= max_iterations:
            print("⚠️ Maximum iterations reached")
        
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
    
    def _build_full_execution_context(self) -> Dict[str, Any]:
        """Build complete execution context for agentic loop"""
        return {
            'goal': self.context.goal,
            'workspace_dir': str(self.workspace_dir),
            'state_dir': str(self.state_dir),
            'container_name': self.context.container_name,
            'environment_info': self.context.environment_info or {},
            'execution_history': [],
            'tool_results': [],
            'current_state': 'initialized'
        }
    
    def _build_iteration_prompt(self, system_agent_spec: str, execution_context: Dict, iteration: int) -> str:
        """Build prompt for current iteration with full context"""
        
        # Get current workspace state
        workspace_files = self._list_workspace_files()
        available_tools = self._get_available_cli_tools()
        
        prompt = f"""You are acting as the SystemAgent from this specification:

{system_agent_spec}

EXECUTION CONTEXT (Iteration {iteration}):
- Goal: {execution_context['goal']}
- Workspace: {execution_context['workspace_dir']}
- State directory: {execution_context['state_dir']}
- Container: {execution_context['container_name'] or "None (host system)"}
- Current state: {execution_context['current_state']}

ENVIRONMENT:
{self._format_environment_info(execution_context['environment_info'])}

AVAILABLE CLI TOOLS:
{available_tools}

WORKSPACE STATE FILES:
{workspace_files}

EXECUTION HISTORY:
{self._format_execution_history(execution_context['execution_history'])}

TOOL RESULTS FROM PREVIOUS STEPS:
{self._format_tool_results(execution_context['tool_results'])}

INSTRUCTIONS:
You can execute real tools and commands. When you need to use a tool, format your response like this:

TOOL_CALL: command_name
PARAMETERS: parameter1=value1, parameter2=value2
REASONING: Why you need this tool

Available tool patterns:
- TOOL_CALL: curl
  PARAMETERS: url=https://example.com, output_file=/workspace/content.html
  REASONING: Fetch web content

- TOOL_CALL: python3
  PARAMETERS: script=/workspace/process.py, args=input.txt output.txt
  REASONING: Process downloaded content

- TOOL_CALL: cat
  PARAMETERS: file=/workspace/file.txt
  REASONING: Read file contents

Continue execution according to the SystemAgent specification. If you need to execute tools, use the TOOL_CALL format above."""

        return prompt
    
    def _extract_and_execute_tools(self, response: str) -> List[Dict[str, Any]]:
        """Extract and execute tool calls from LLM response"""
        tool_results = []
        
        # Parse tool calls from response
        lines = response.split('\n')
        i = 0
        
        while i < len(lines):
            if lines[i].startswith('TOOL_CALL:'):
                tool_call = self._parse_tool_call(lines, i)
                if tool_call:
                    print(f"🔧 Executing tool: {tool_call['command']}")
                    result = self._execute_tool_call(tool_call)
                    tool_results.append(result)
                    i += tool_call.get('lines_consumed', 1)
                else:
                    i += 1
            else:
                i += 1
        
        return tool_results
    
    def _parse_tool_call(self, lines: List[str], start_index: int) -> Dict[str, Any]:
        """Parse a tool call from response lines"""
        if start_index >= len(lines):
            return None
            
        tool_call = {
            'command': lines[start_index].replace('TOOL_CALL:', '').strip(),
            'parameters': {},
            'reasoning': '',
            'lines_consumed': 1
        }
        
        # Parse parameters and reasoning
        i = start_index + 1
        while i < len(lines) and i < start_index + 10:  # Look ahead max 10 lines
            line = lines[i].strip()
            if line.startswith('PARAMETERS:'):
                param_str = line.replace('PARAMETERS:', '').strip()
                tool_call['parameters'] = self._parse_parameters(param_str)
                tool_call['lines_consumed'] += 1
            elif line.startswith('REASONING:'):
                tool_call['reasoning'] = line.replace('REASONING:', '').strip()
                tool_call['lines_consumed'] += 1
            elif line == '' or not line.startswith(('PARAMETERS:', 'REASONING:')):
                break
            i += 1
        
        return tool_call
    
    def _parse_parameters(self, param_str: str) -> Dict[str, str]:
        """Parse parameters string into dictionary"""
        params = {}
        if not param_str:
            return params
            
        # Split by comma and parse key=value pairs
        for pair in param_str.split(','):
            if '=' in pair:
                key, value = pair.split('=', 1)
                params[key.strip()] = value.strip()
        
        return params
    
    def _execute_tool_call(self, tool_call: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call in the container or host system"""
        command = tool_call['command']
        params = tool_call['parameters']
        
        result = {
            'tool': command,
            'parameters': params,
            'reasoning': tool_call['reasoning'],
            'success': False,
            'output': '',
            'error': '',
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            if command == 'curl':
                result = self._execute_curl(params, result)
            elif command == 'python3':
                result = self._execute_python(params, result)
            elif command in ['cat', 'ls', 'grep', 'echo', 'mkdir']:
                result = self._execute_shell_command(command, params, result)
            else:
                result = self._execute_generic_command(command, params, result)
                
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            print(f"❌ Tool execution failed: {e}")
        
        return result
    
    def _execute_curl(self, params: Dict[str, str], result: Dict[str, Any]) -> Dict[str, Any]:
        """Execute curl command to fetch web content"""
        url = params.get('url', '')
        output_file = params.get('output_file', '/workspace/fetched_content.html')
        
        if not url:
            result['error'] = "URL parameter required for curl"
            return result
        
        if self.context.container_name:
            # Execute in container
            cmd = ['docker', 'exec', self.context.container_name, 'curl', '-s', '-L', url, '-o', output_file]
        else:
            # Execute on host
            cmd = ['curl', '-s', '-L', url, '-o', output_file]
        
        process_result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        result['success'] = process_result.returncode == 0
        result['output'] = process_result.stdout
        result['error'] = process_result.stderr
        
        if result['success']:
            print(f"✅ Successfully fetched {url} to {output_file}")
        
        return result
    
    def _execute_python(self, params: Dict[str, str], result: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Python script"""
        script = params.get('script', '')
        args = params.get('args', '')
        
        if not script:
            result['error'] = "Script parameter required for python3"
            return result
        
        if self.context.container_name:
            cmd = ['docker', 'exec', self.context.container_name, 'python3', script] + args.split() if args else ['docker', 'exec', self.context.container_name, 'python3', script]
        else:
            cmd = ['python3', script] + args.split() if args else ['python3', script]
        
        process_result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        result['success'] = process_result.returncode == 0
        result['output'] = process_result.stdout
        result['error'] = process_result.stderr
        
        return result
    
    def _execute_shell_command(self, command: str, params: Dict[str, str], result: Dict[str, Any]) -> Dict[str, Any]:
        """Execute basic shell commands"""
        args = []
        
        # Build command arguments from parameters
        if command == 'cat':
            file_path = params.get('file', '')
            if file_path:
                args = [file_path]
        elif command == 'ls':
            path = params.get('path', '/workspace')
            args = [path]
        elif command == 'mkdir':
            path = params.get('path', '')
            if path:
                args = ['-p', path]
        elif command == 'echo':
            text = params.get('text', '')
            if text:
                args = [text]
        
        if self.context.container_name:
            cmd = ['docker', 'exec', self.context.container_name, command] + args
        else:
            cmd = [command] + args
        
        process_result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        result['success'] = process_result.returncode == 0
        result['output'] = process_result.stdout
        result['error'] = process_result.stderr
        
        return result
    
    def _execute_generic_command(self, command: str, params: Dict[str, str], result: Dict[str, Any]) -> Dict[str, Any]:
        """Execute generic command with parameters"""
        args = []
        for key, value in params.items():
            if key != 'command':
                args.extend([f'--{key}', value])
        
        if self.context.container_name:
            cmd = ['docker', 'exec', self.context.container_name, command] + args
        else:
            cmd = [command] + args
        
        process_result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        result['success'] = process_result.returncode == 0
        result['output'] = process_result.stdout
        result['error'] = process_result.stderr
        
        return result
    
    def _update_execution_context(self, context: Dict[str, Any], response: str, tool_results: List[Dict]) -> Dict[str, Any]:
        """Update execution context with latest results"""
        context['execution_history'].append({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        context['tool_results'].extend(tool_results)
        
        # Update current state based on results
        if tool_results:
            if any(not r['success'] for r in tool_results):
                context['current_state'] = 'error_recovery'
            else:
                context['current_state'] = 'progressing'
        
        return context
    
    def _is_execution_complete(self, response: str, tool_results: List[Dict]) -> bool:
        """Check if execution is complete"""
        completion_indicators = [
            'task completed', 'execution complete', 'goal achieved',
            'summary saved', 'process finished', 'done'
        ]
        
        response_lower = response.lower()
        has_completion_text = any(indicator in response_lower for indicator in completion_indicators)
        
        # Also check if recent tool results indicate completion
        recent_success = len(tool_results) > 0 and all(r['success'] for r in tool_results[-3:])
        
        return has_completion_text or (recent_success and 'summary' in response_lower)
    
    def _update_state_with_context(self, context: Dict[str, Any]):
        """Update state files with current context"""
        # Update plan with current state
        plan_content = f"# Execution Plan\n\n**Goal:** {context['goal']}\n\n## Current State\n{context['current_state']}\n\n## Progress\n{len(context['execution_history'])} iterations completed\n"
        self._update_state_file('plan.md', plan_content)
        
        # Update variables with latest data
        variables = {
            'goal': context['goal'],
            'current_state': context['current_state'],
            'iterations': len(context['execution_history']),
            'tool_calls': len(context['tool_results'])
        }
        self._update_state_file('variables.json', json.dumps(variables, indent=2))
    
    def _format_environment_info(self, env_info: Dict) -> str:
        """Format environment info for prompt"""
        if not env_info:
            return "Environment: Not detected"
        
        return f"""
        Available tools: {', '.join(env_info.get('available_tools', [])[:10])}
        Package managers: {', '.join(env_info.get('package_managers', []))}
        OS: {env_info.get('distro', 'Unknown')}
        Container: {env_info.get('container_name', 'None')}
        """
    
    def _format_execution_history(self, history: List[Dict]) -> str:
        """Format execution history for prompt"""
        if not history:
            return "No previous execution steps"
        
        formatted = []
        for i, step in enumerate(history[-3:], 1):  # Show last 3 steps
            formatted.append(f"Step {i}: {step['response'][:200]}...")
        
        return '\n'.join(formatted)
    
    def _format_tool_results(self, results: List[Dict]) -> str:
        """Format tool results for prompt"""
        if not results:
            return "No tool executions yet"
        
        formatted = []
        for result in results[-5:]:  # Show last 5 results
            status = "✅" if result['success'] else "❌"
            formatted.append(f"{status} {result['tool']}: {result['output'][:100]}...")
        
        return '\n'.join(formatted)

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
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
    
    def __init__(self, model: str = None):
        """Initialize the LLM interpreter"""
        
        # Validate OpenAI API key
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        self.model = model or os.getenv('OPENAI_MODEL', 'gpt-4o')
        
        # Setup paths
        self.llmunix_root = Path(__file__).parent
        self.workspace_dir = self.llmunix_root / "workspace"
        self.state_dir = self.workspace_dir / "state"
        
        # Execution context
        self.context: Optional[ExecutionContext] = None
        
        # Load markdown components registry
        self.component_registry = self._load_component_registry()
        
        print(f"🤖 LLMunix LLM Interpreter initialized")
        print(f"📁 LLMunix root: {self.llmunix_root}")
        print(f"🏗️  Workspace: {self.workspace_dir}")
        print(f"🧠 Model: {self.model}")
        print(f"🔧 Components loaded: {len(self.component_registry)} tools/agents")
    
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
        print('  ./llmunix-llm interactive                      # Start interactive session')
        print('  ./llmunix-llm execute: "Create a Python calculator"')
        print('  ./llmunix-llm execute: "Research AI trends" -i   # Execute and enter interactive mode')
        print('  ./llmunix-llm execute: "Fetch data from URL and analyze"')
        print("\nInteractive session features:")
        print('  🔄 Goal refinement with "refine" command')
        print('  📊 Workspace status with "status" command') 
        print('  📜 Execution history with "history" command')
        print('  🧹 Workspace management with "clear" command')
        print("\n" + "="*60 + "\n")
    
    def execute(self, goal: str, cleanup_after=True):
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
            if cleanup_after:
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
        """Execute a tool call - either CLI command or markdown component"""
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
            # First, check if this is a markdown component
            if self._is_markdown_component(command):
                print(f"🔧 Executing markdown component: {command}")
                markdown_result = self._execute_markdown_component(command, params)
                
                # Convert markdown result to tool result format
                result['success'] = markdown_result.get('success', False)
                result['output'] = markdown_result.get('output', '')
                result['error'] = markdown_result.get('error', '')
                result['metadata'] = markdown_result.get('metadata', {})
                
                if result['success']:
                    print(f"✅ Markdown component '{command}' executed successfully")
                else:
                    print(f"❌ Markdown component '{command}' failed: {result['error']}")
                
                return result
            
            # Otherwise, execute as CLI command
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
    
    def _is_markdown_component(self, command: str) -> bool:
        """Check if a command refers to a markdown component"""
        # Check if command matches any component in registry
        for comp_data in self.component_registry.values():
            comp_name = comp_data.get('name', '').replace('[REAL]', '').replace('[SIMULATION]', '').strip()
            if (comp_name == command or 
                comp_data.get('id') == command or 
                command in comp_data.get('name', '') or
                command.lower().replace('tool', '').replace('agent', '') in comp_name.lower()):
                return True
        
        # Common markdown component name patterns
        markdown_patterns = [
            'QueryMemoryTool', 'RealWebFetchTool', 'RealFileSystemTool', 'RealSummarizationAgent',
            'MemoryAnalysisAgent', 'WebFetcherTool', 'SummarizationAgent', 'FileWriterTool'
        ]
        
        return command in markdown_patterns
    
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
            response = step.get('response', '')
            if isinstance(response, str):
                formatted.append(f"Step {i}: {response[:200]}...")
            else:
                formatted.append(f"Step {i}: {str(response)[:200]}...")
        
        return '\n'.join(formatted)
    
    def _format_tool_results(self, results: List[Dict]) -> str:
        """Format tool results for prompt"""
        if not results:
            return "No tool executions yet"
        
        formatted = []
        for result in results[-5:]:  # Show last 5 results
            status = "✅" if result.get('success') else "❌"
            tool_name = result.get('tool', 'unknown')
            output = result.get('output', '')
            if isinstance(output, str):
                output_preview = output[:100]
            else:
                output_preview = str(output)[:100]
            formatted.append(f"{status} {tool_name}: {output_preview}...")
        
        return '\n'.join(formatted)

    def _load_component_registry(self) -> Dict[str, Dict]:
        """Load all markdown components from the system"""
        registry = {}
        
        # Load SmartLibrary registry
        smart_library_path = self.llmunix_root / "system" / "SmartLibrary.md"
        if smart_library_path.exists():
            registry.update(self._parse_smart_library(smart_library_path))
        
        # Discover components in directories
        components_dir = self.llmunix_root / "components"
        if components_dir.exists():
            registry.update(self._discover_components(components_dir))
        
        return registry
    
    def _parse_smart_library(self, library_path: Path) -> Dict[str, Dict]:
        """Parse SmartLibrary.md to extract component metadata"""
        registry = {}
        
        try:
            content = library_path.read_text(encoding='utf-8')
            
            # Extract component entries (basic parsing)
            lines = content.split('\n')
            current_component = {}
            
            for line in lines:
                line = line.strip()
                if line.startswith('- **id**:'):
                    if current_component:
                        registry[current_component.get('id', '')] = current_component
                    current_component = {'id': line.split('`')[1] if '`' in line else ''}
                elif line.startswith('- **name**:'):
                    current_component['name'] = line.split(': ')[1] if ': ' in line else ''
                elif line.startswith('- **file_path**:'):
                    current_component['file_path'] = line.split('`')[1] if '`' in line else ''
                elif line.startswith('- **record_type**:'):
                    current_component['type'] = line.split(': ')[1] if ': ' in line else ''
                elif line.startswith('- **claude_tool**:'):
                    current_component['claude_tools'] = line.split(': ')[1] if ': ' in line else ''
                elif line.startswith('- **command_tool**:'):
                    current_component['command_tools'] = line.split(': ')[1] if ': ' in line else ''
                elif line.startswith('- **description**:'):
                    current_component['description'] = line.split(': ')[1] if ': ' in line else ''
            
            # Add last component
            if current_component and current_component.get('id'):
                registry[current_component['id']] = current_component
                
        except Exception as e:
            print(f"⚠️  Error parsing SmartLibrary: {e}")
        
        return registry
    
    def _discover_components(self, components_dir: Path) -> Dict[str, Dict]:
        """Discover markdown components in components directory"""
        registry = {}
        
        for md_file in components_dir.rglob('*.md'):
            try:
                relative_path = md_file.relative_to(self.llmunix_root)
                component_name = md_file.stem
                
                # Determine type from path
                component_type = 'UNKNOWN'
                if 'tools' in md_file.parts:
                    component_type = 'TOOL'
                elif 'agents' in md_file.parts:
                    component_type = 'AGENT'
                
                registry[component_name] = {
                    'id': component_name,
                    'name': component_name,
                    'file_path': str(relative_path),
                    'type': component_type,
                    'full_path': str(md_file)
                }
                
            except Exception as e:
                print(f"⚠️  Error discovering component {md_file}: {e}")
        
        return registry
    
    def _execute_markdown_component(self, component_name: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a markdown-defined component using LLM interpretation"""
        
        # Find component in registry
        component = None
        for comp_data in self.component_registry.values():
            if (comp_data.get('name', '').replace('[REAL]', '').replace('[SIMULATION]', '').strip() == component_name or
                comp_data.get('id') == component_name or
                component_name in comp_data.get('name', '')):
                component = comp_data
                break
        
        if not component:
            return {
                'success': False,
                'error': f"Component '{component_name}' not found in registry",
                'output': ''
            }
        
        # Load component specification
        try:
            if 'full_path' in component:
                component_path = Path(component['full_path'])
            else:
                component_path = self.llmunix_root / component.get('file_path', '')
            
            if not component_path.exists():
                return {
                    'success': False,
                    'error': f"Component file not found: {component_path}",
                    'output': ''
                }
            
            component_spec = component_path.read_text(encoding='utf-8')
            
            # Execute component using LLM interpretation
            return self._interpret_and_execute_component(component_spec, component, inputs)
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error loading component: {e}",
                'output': ''
            }
    
    def _interpret_and_execute_component(self, spec: str, component: Dict, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Use LLM to interpret markdown specification and execute with real tools"""
        
        # Build execution prompt
        prompt = f"""You are executing a LLMunix component. Your task is to interpret the markdown specification and execute it using real tools.

COMPONENT SPECIFICATION:
{spec}

COMPONENT METADATA:
- Name: {component.get('name', 'Unknown')}
- Type: {component.get('type', 'Unknown')}
- Claude Tools: {component.get('claude_tools', 'Unknown')}
- Command Tools: {component.get('command_tools', 'Unknown')}

INPUT PARAMETERS:
{json.dumps(inputs, indent=2)}

EXECUTION CONTEXT:
- Workspace: {self.workspace_dir}
- State Directory: {self.state_dir}
- Container: {self.context.container_name if self.context else 'None'}

AVAILABLE REAL TOOLS:
{self._get_available_cli_tools()}

INSTRUCTIONS:
1. Read and understand the component specification
2. Interpret the logic for the given inputs
3. Execute the required steps using real tools (TOOL_CALL format)
4. Return structured output matching the component's output specification

You can use these real tools:
- curl: For web requests
- python3: For data processing
- cat: For reading files
- echo: For creating simple content
- grep: For searching content
- mkdir: For creating directories

Use the TOOL_CALL format when you need to execute tools:

TOOL_CALL: command_name
PARAMETERS: param1=value1, param2=value2
REASONING: Why you need this tool

After all tool executions, provide a final JSON result in this format:
```json
{{
  "success": true,
  "output": "main result content",
  "metadata": {{"execution_time": "...", "tools_used": [...]}},
  "error": null
}}
```"""

        # Get LLM response for component execution
        response = self._call_llm(prompt, max_tokens=3000)
        
        # Extract and execute any tool calls
        tool_results = self._extract_and_execute_tools(response)
        
        # Parse final JSON result from response
        final_result = self._extract_final_result(response, tool_results)
        
        return final_result
    
    def _extract_final_result(self, response: str, tool_results: List[Dict]) -> Dict[str, Any]:
        """Extract the final JSON result from LLM response"""
        
        # Look for JSON block in response
        try:
            # Find JSON block
            json_start = response.find('```json')
            if json_start != -1:
                json_start += 7  # Skip ```json
                json_end = response.find('```', json_start)
                if json_end != -1:
                    json_str = response[json_start:json_end].strip()
                    result = json.loads(json_str)
                    
                    # Add tool execution metadata
                    if 'metadata' not in result:
                        result['metadata'] = {}
                    result['metadata']['tool_executions'] = len(tool_results)
                    result['metadata']['successful_tools'] = sum(1 for r in tool_results if r.get('success'))
                    
                    return result
        except Exception as e:
            print(f"⚠️  Error parsing JSON result: {e}")
        
        # Fallback result if JSON parsing fails
        success = len(tool_results) == 0 or any(r.get('success') for r in tool_results)
        output = response if not tool_results else tool_results[-1].get('output', response)
        
        return {
            'success': success,
            'output': output,
            'metadata': {
                'tool_executions': len(tool_results),
                'successful_tools': sum(1 for r in tool_results if r.get('success')),
                'fallback_parsing': True
            },
            'error': None if success else 'Component execution may have failed'
        }

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
    
    def interactive_session(self):
        """Start an interactive session for goal refinement and new tasks"""
        print("\n" + "="*60)
        print("🎯 LLMunix Interactive Session")
        print("="*60)
        print("Enter goals to execute, or type commands:")
        print("  'refine' - Refine the last goal")
        print("  'status' - Show current workspace status")
        print("  'history' - Show execution history")
        print("  'clear' - Clear workspace for fresh start")
        print("  'help' - Show this help")
        print("  'exit' or 'quit' - Exit interactive session")
        print("-"*60)
        
        try:
            while True:
                try:
                    # Get user input
                    user_input = input("\n🎯 llmunix> ").strip()
                    
                    if not user_input:
                        continue
                    
                    # Handle commands
                    if user_input.lower() in ['exit', 'quit', 'q']:
                        print("👋 Goodbye!")
                        break
                    elif user_input.lower() == 'help':
                        self._show_interactive_help()
                    elif user_input.lower() == 'status':
                        self._show_status()
                    elif user_input.lower() == 'history':
                        self._show_history()
                    elif user_input.lower() == 'clear':
                        self._interactive_clear_workspace()
                    elif user_input.lower() == 'refine':
                        self._refine_last_goal()
                    else:
                        # Treat as a new goal to execute
                        print(f"\n🚀 Executing: {user_input}")
                        self.execute(user_input, cleanup_after=False)
                        print(f"\n✅ Goal completed. Ready for next command.")
                        
                except KeyboardInterrupt:
                    print("\n\n👋 Session interrupted. Goodbye!")
                    break
                except EOFError:
                    print("\n\n👋 Session ended. Goodbye!")
                    break
                except Exception as e:
                    print(f"\n❌ Error: {e}")
                    print("Type 'help' for available commands or 'exit' to quit.")
        finally:
            # Cleanup when session ends
            self._cleanup_execution()
    
    def _show_interactive_help(self):
        """Show interactive session help"""
        print("\n📖 LLMunix Interactive Session Help")
        print("-"*40)
        print("Commands:")
        print("  refine       - Refine and re-execute the last goal")
        print("  status       - Show workspace and execution status")
        print("  history      - Show execution history")
        print("  clear        - Clear workspace for fresh start")
        print("  help         - Show this help")
        print("  exit/quit    - Exit interactive session")
        print("\nTo execute a goal, simply type it:")
        print("  Create a Python calculator")
        print("  Fetch content from https://example.com")
        print("  Analyze the data in my workspace")
        print("\nExamples:")
        print("  🎯 llmunix> Create a simple web scraper")
        print("  🎯 llmunix> refine")
        print("  🎯 llmunix> status")
        print("  🎯 llmunix> Build a REST API server")
    
    def _show_status(self):
        """Show current workspace status"""
        print("\n📊 Workspace Status")
        print("-"*30)
        
        if not self.workspace_dir.exists():
            print("⚠️  No workspace found. Execute a goal first.")
            return
        
        # Show workspace files
        files = list(self.workspace_dir.rglob('*'))
        file_count = len([f for f in files if f.is_file()])
        dir_count = len([f for f in files if f.is_dir()]) - 1  # Exclude workspace itself
        
        print(f"📁 Workspace: {self.workspace_dir}")
        print(f"📄 Files: {file_count}")
        print(f"📂 Directories: {dir_count}")
        
        # Show state files status
        if self.state_dir.exists():
            print(f"\n🧠 State Directory: {self.state_dir}")
            state_files = ['plan.md', 'history.md', 'context.md', 'constraints.md', 'variables.json']
            for state_file in state_files:
                file_path = self.state_dir / state_file
                status = "✅" if file_path.exists() else "❌"
                print(f"  {status} {state_file}")
        
        # Show recent files
        recent_files = sorted(
            [f for f in files if f.is_file()], 
            key=lambda f: f.stat().st_mtime, 
            reverse=True
        )[:5]
        
        if recent_files:
            print(f"\n📝 Recent files:")
            for f in recent_files:
                rel_path = f.relative_to(self.workspace_dir)
                size = f.stat().st_size
                print(f"  • {rel_path} ({size} bytes)")
    
    def _show_history(self):
        """Show execution history"""
        print("\n📜 Execution History")
        print("-"*30)
        
        history_file = self.state_dir / "history.md" if self.state_dir else None
        if not history_file or not history_file.exists():
            print("⚠️  No execution history found.")
            return
        
        try:
            history_content = history_file.read_text(encoding='utf-8')
            
            # Extract recent entries (last 1000 chars for readability)
            if len(history_content) > 1000:
                print("... (showing recent history)")
                history_content = "..." + history_content[-1000:]
            
            print(history_content)
            
        except Exception as e:
            print(f"❌ Error reading history: {e}")
    
    def _interactive_clear_workspace(self):
        """Clear workspace interactively with confirmation"""
        print("\n🧹 Clear Workspace")
        print("-"*20)
        
        if not self.workspace_dir.exists():
            print("⚠️  No workspace to clear.")
            return
        
        # Show what will be cleared
        files = list(self.workspace_dir.rglob('*'))
        file_count = len([f for f in files if f.is_file()])
        
        print(f"This will delete {file_count} files in {self.workspace_dir}")
        
        confirm = input("Are you sure? [y/N]: ").strip().lower()
        if confirm in ['y', 'yes']:
            self._clean_workspace()
            print("✅ Workspace cleared successfully.")
        else:
            print("❌ Clear cancelled.")
    
    def _refine_last_goal(self):
        """Refine and re-execute the last goal"""
        print("\n🔄 Refine Last Goal")
        print("-"*20)
        
        # Get last goal from context
        last_goal = None
        if self.context and hasattr(self.context, 'goal'):
            last_goal = self.context.goal
        else:
            # Try to read from variables.json
            try:
                variables_file = self.state_dir / "variables.json"
                if variables_file.exists():
                    variables = json.loads(variables_file.read_text())
                    last_goal = variables.get('goal')
            except:
                pass
        
        if not last_goal:
            print("⚠️  No previous goal found to refine.")
            print("💡 Execute a goal first, then use 'refine' to improve it.")
            return
        
        print(f"Previous goal: {last_goal}")
        print("\nHow would you like to refine this goal?")
        print("Enter your refinement instructions (or press Enter to re-execute as-is):")
        
        refinement = input("🔄 refinement> ").strip()
        
        if refinement:
            # Create refined goal
            refined_goal = f"Refine the previous goal '{last_goal}' with these improvements: {refinement}"
            print(f"\n🚀 Executing refined goal...")
            self.execute(refined_goal, cleanup_after=False)
        else:
            # Re-execute the same goal
            print(f"\n🚀 Re-executing previous goal...")
            self.execute(last_goal, cleanup_after=False)
        
        print(f"\n✅ Refinement completed. Ready for next command.")

def main():
    """Main entry point for the LLM interpreter"""
    import argparse
    
    parser = argparse.ArgumentParser(description='LLMunix LLM Interpreter - Lightweight Runtime')
    parser.add_argument('command', choices=['boot', 'execute', 'interactive'], help='Command to run')
    parser.add_argument('goal', nargs='?', help='Goal to execute (for execute command)')
    parser.add_argument('--model', default='gpt-4o', help='OpenAI model to use')
    parser.add_argument('--interactive', '-i', action='store_true', help='Start interactive session after execution')
    
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
            
            # Start interactive session if requested
            if args.interactive:
                interpreter.interactive_session()
        elif args.command == 'interactive':
            interpreter.boot()
            interpreter.interactive_session()
            
    except Exception as e:
        print(f"❌ Interpreter failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
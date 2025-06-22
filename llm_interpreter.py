#!/usr/bin/env python3

"""
LLMunix LLM Interpreter - Pure Markdown Operating System Runtime

This module implements an LLM-driven interpreter that replaces Claude Code
as the runtime engine for LLMunix. It provides autonomous execution of
markdown-defined agent/tool systems using OpenAI's GPT models.

Key Features:
- Zero hardcoded logic - all decisions made by LLM
- Docker sandbox for secure tool execution
- Environment detection and adaptation
- Modular state management
- Real tool integration with error recovery

Created as part of LLMunix's dual runtime architecture.
"""

import os
import sys
import json
import time
import yaml
import subprocess
import tempfile
import requests
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
    LLMunix LLM Interpreter - Autonomous markdown-driven execution
    
    This interpreter replaces Claude Code as the runtime engine, providing
    equivalent capabilities through LLM-driven decision making.
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
        print("\\n" + "="*60)
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
        
        print("\\n🎯 LLMunix is ready for autonomous execution!")
        print("\\nExample commands:")
        print('  ./llmunix-llm execute: "Create a Python calculator"')
        print('  ./llmunix-llm execute: "Research AI trends and create summary"')
        print('  ./llmunix-llm execute: "Fetch data from URL and analyze"')
        print("\\n" + "="*60 + "\\n")
    
    def execute(self, goal: str):
        """Execute a goal using LLM-driven autonomous planning and execution"""
        
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
        
        # LLM-driven execution loop
        try:
            self._llm_execution_loop()
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
            'plan.md': f"# Execution Plan\\n\\n**Goal:** {self.context.goal}\\n\\n## Status\\nInitializing...\\n",
            'context.md': "# Execution Context\\n\\n## Knowledge Accumulation\\n\\n",
            'history.md': f"# Execution History\\n\\n**Started:** {datetime.now().isoformat()}\\n\\n",
            'constraints.md': "# Behavioral Constraints\\n\\n## Initial Settings\\n- priority: balanced\\n- error_tolerance: moderate\\n",
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
            
            # Use Alpine Linux for lightweight container with package manager detection
            run_command = [
                'docker', 'run', '-d', '--name', container_name,
                '-w', '/workspace',
                'alpine:latest',
                'sh', '-c', 'apk add --no-cache python3 py3-pip curl bash && sleep 3600'
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
                        for line in result.stdout.split('\\n'):
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

## Recommendations for LLM
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
    
    def _llm_execution_loop(self):
        """Main LLM-driven execution loop"""
        print("🧠 Starting LLM-driven execution...")
        
        # Phase 1: Goal Analysis and Planning
        print("\\n📋 Phase 1: Goal Analysis and Planning")
        plan = self._llm_analyze_and_plan()
        self._update_state_file('plan.md', plan)
        
        # Phase 2: Step-by-step execution
        print("\\n🔄 Phase 2: Execution")
        self._llm_execute_plan()
        
        # Phase 3: Completion and summary
        print("\\n📝 Phase 3: Completion Summary")
        self._llm_generate_summary()
    
    def _llm_analyze_and_plan(self) -> str:
        """LLM analyzes the goal and creates execution plan"""
        
        # Build context for LLM
        system_context = self._build_system_context()
        environment_context = self._build_environment_context()
        
        prompt = f"""You are the LLMunix System Agent - an autonomous AI operating system that executes goals through markdown-defined tools and agents.

SYSTEM CONTEXT:
{system_context}

ENVIRONMENT CONTEXT:
{environment_context}

GOAL TO EXECUTE:
{self.context.goal}

Your task is to analyze this goal and create a detailed execution plan. Consider:

1. **Goal Analysis**: Break down what exactly needs to be accomplished
2. **Tool Selection**: What tools/capabilities will be needed
3. **Step Sequencing**: Logical order of operations
4. **Error Handling**: Potential failure points and recovery strategies
5. **Environment Adaptation**: Use detected tools and avoid unavailable ones

Respond with a structured markdown execution plan that will be saved to plan.md.
Focus on practical, achievable steps using available tools.

EXECUTION PLAN:"""

        response = self._call_llm(prompt, max_tokens=2000)
        
        print("✅ Execution plan generated")
        return response
    
    def _llm_execute_plan(self):
        """Execute the LLM-generated plan step by step"""
        
        # Read current plan
        plan_file = self.state_dir / "plan.md"
        current_plan = plan_file.read_text(encoding='utf-8') if plan_file.exists() else ""
        
        # Get current context
        context_file = self.state_dir / "context.md"
        current_context = context_file.read_text(encoding='utf-8') if context_file.exists() else ""
        
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            print(f"\\n🔄 Execution iteration {iteration}")
            
            # LLM decides next action
            action = self._llm_decide_next_action(current_plan, current_context, iteration)
            
            if "EXECUTION_COMPLETE" in action:
                print("✅ LLM determined execution is complete")
                break
            
            # Execute the action
            self._execute_action(action, iteration)
            
            # Update context
            current_context = self._read_state_file("context.md")
            
            # Brief pause between iterations
            time.sleep(1)
        
        if iteration >= max_iterations:
            print("⚠️  Maximum iterations reached")
    
    def _llm_decide_next_action(self, plan: str, context: str, iteration: int) -> str:
        """LLM decides the next action to take"""
        
        environment_context = self._build_environment_context()
        history = self._read_state_file("history.md")
        
        prompt = f"""You are executing step {iteration} of the LLMunix goal: "{self.context.goal}"

CURRENT EXECUTION PLAN:
{plan}

ACCUMULATED CONTEXT:
{context}

EXECUTION HISTORY:
{history}

ENVIRONMENT CONTEXT:
{environment_context}

Based on the plan, context, and history, decide the next action to take.

Available action types:
1. **TOOL_EXECUTION**: Execute a command/tool (specify exact command)
2. **FILE_OPERATION**: Create, read, or modify files
3. **WEB_REQUEST**: Fetch content from URLs
4. **ANALYSIS**: Analyze data or content
5. **EXECUTION_COMPLETE**: Mark execution as finished

Guidelines:
- Use only available tools from environment detection
- Be specific about commands and parameters
- If goal is achieved, respond with "EXECUTION_COMPLETE"
- Adapt to any errors from previous iterations
- Make real progress toward the goal

NEXT ACTION:"""
        
        response = self._call_llm(prompt, max_tokens=1500)
        return response
    
    def _execute_action(self, action: str, iteration: int):
        """Execute an LLM-determined action"""
        
        print(f"🎬 Executing action: {action[:100]}...")
        
        # Log the action
        self._log_execution_step(f"Iteration {iteration}", action)
        
        try:
            # Parse action type and execute accordingly
            if "TOOL_EXECUTION" in action or "docker exec" in action or any(cmd in action.lower() for cmd in ['python', 'curl', 'cat', 'echo', 'mkdir']):
                self._execute_tool_action(action)
            elif "FILE_OPERATION" in action or "file" in action.lower():
                self._execute_file_action(action)
            elif "WEB_REQUEST" in action or "http" in action:
                self._execute_web_action(action)
            elif "ANALYSIS" in action:
                self._execute_analysis_action(action)
            else:
                # Generic LLM processing
                self._execute_generic_action(action)
                
        except Exception as e:
            error_msg = f"Action execution failed: {e}"
            print(f"❌ {error_msg}")
            self._log_execution_step(f"ERROR in iteration {iteration}", error_msg)
    
    def _execute_tool_action(self, action: str):
        """Execute tool/command actions"""
        
        # Extract command from action
        command = self._extract_command_from_action(action)
        
        if not command:
            print("⚠️  No command found in action")
            return
        
        print(f"🔧 Executing command: {command}")
        
        if self.container_name:
            # Execute in Docker container
            result = self._execute_in_container(command)
        else:
            # Simulate execution
            result = f"SIMULATED: {command}\\nOutput would appear here in real execution"
        
        # Log result
        self._log_execution_step("Tool Execution Result", result)
        self._update_context(f"Executed: {command}\\nResult: {result}")
    
    def _execute_file_action(self, action: str):
        """Execute file operations"""
        print("📁 Executing file operation...")
        
        # Use LLM to interpret file action
        file_result = self._call_llm(f"""
        Interpret this file action and provide a summary:
        {action}
        
        If this involves creating/modifying files, provide the filename and content.
        If reading files, provide what should be read.
        
        File operation summary:""", max_tokens=500)
        
        self._log_execution_step("File Operation", file_result)
        self._update_context(f"File operation: {file_result}")
    
    def _execute_web_action(self, action: str):
        """Execute web requests"""
        print("🌐 Executing web request...")
        
        # Extract URL if present
        import re
        url_pattern = r'https?://[^\\s]+'
        urls = re.findall(url_pattern, action)
        
        if urls:
            url = urls[0]
            try:
                print(f"📡 Fetching: {url}")
                response = requests.get(url, timeout=10)
                content = response.text[:2000]  # Limit content
                
                result = f"Fetched {url}\\nStatus: {response.status_code}\\nContent preview: {content}..."
                self._log_execution_step("Web Request", result)
                self._update_context(f"Web content from {url}: {content[:500]}...")
                
            except Exception as e:
                error_msg = f"Web request failed: {e}"
                self._log_execution_step("Web Request Error", error_msg)
        else:
            self._log_execution_step("Web Action", "No URL found in action")
    
    def _execute_analysis_action(self, action: str):
        """Execute analysis actions"""
        print("🔍 Executing analysis...")
        
        # Use LLM for analysis
        analysis_result = self._call_llm(f"""
        Perform this analysis task:
        {action}
        
        Provide a structured analysis with key findings and insights.
        
        Analysis result:""", max_tokens=1000)
        
        self._log_execution_step("Analysis", analysis_result)
        self._update_context(f"Analysis completed: {analysis_result}")
    
    def _execute_generic_action(self, action: str):
        """Execute generic actions via LLM processing"""
        print("⚙️  Processing generic action...")
        
        result = self._call_llm(f"""
        Process this action and provide a result:
        {action}
        
        Action result:""", max_tokens=800)
        
        self._log_execution_step("Generic Action", result)
        self._update_context(f"Action processed: {result}")
    
    def _extract_command_from_action(self, action: str) -> Optional[str]:
        """Extract executable command from LLM action"""
        
        # Look for common command patterns
        import re
        
        # Direct command patterns
        patterns = [
            r'docker exec [^\\n]+',
            r'python3? [^\\n]+',
            r'curl [^\\n]+',
            r'echo [^\\n]+',
            r'cat [^\\n]+',
            r'mkdir [^\\n]+',
            r'ls [^\\n]+',
            r'pip3? [^\\n]+',
            r'apk [^\\n]+',
            r'apt-get [^\\n]+'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, action, re.IGNORECASE)
            if matches:
                return matches[0].strip()
        
        # Look for code blocks
        code_block_pattern = r'```(?:bash|shell)?\\n([^`]+)```'
        code_matches = re.findall(code_block_pattern, action, re.MULTILINE | re.DOTALL)
        if code_matches:
            return code_matches[0].strip()
        
        return None
    
    def _execute_in_container(self, command: str) -> str:
        """Execute command in Docker container"""
        try:
            # Handle multi-line commands
            if '\\n' in command:
                # Create temporary script
                script_content = command
                script_path = f"/tmp/llmunix_script_{int(time.time())}.sh"
                
                # Write script to container
                subprocess.run([
                    'docker', 'exec', self.container_name,
                    'sh', '-c', f'echo "{script_content}" > {script_path} && chmod +x {script_path}'
                ], timeout=30)
                
                # Execute script
                result = subprocess.run([
                    'docker', 'exec', self.container_name, 'sh', script_path
                ], capture_output=True, text=True, timeout=60)
                
                # Clean up
                subprocess.run([
                    'docker', 'exec', self.container_name, 'rm', script_path
                ], capture_output=True, timeout=10)
                
            else:
                # Simple command execution
                if command.startswith('docker exec'):
                    # Remove docker exec prefix if present
                    command = command.replace(f'docker exec {self.container_name}', '').strip()
                
                result = subprocess.run([
                    'docker', 'exec', self.container_name, 'sh', '-c', command
                ], capture_output=True, text=True, timeout=60)
            
            output = f"Exit code: {result.returncode}\\n"
            if result.stdout:
                output += f"STDOUT:\\n{result.stdout}\\n"
            if result.stderr:
                output += f"STDERR:\\n{result.stderr}\\n"
            
            return output
            
        except subprocess.TimeoutExpired:
            return "Command timed out"
        except Exception as e:
            return f"Execution error: {e}"
    
    def _llm_generate_summary(self):
        """Generate execution summary"""
        
        history = self._read_state_file("history.md")
        context = self._read_state_file("context.md")
        
        prompt = f"""Generate a completion summary for the LLMunix execution.

ORIGINAL GOAL: {self.context.goal}

EXECUTION HISTORY:
{history}

ACCUMULATED CONTEXT:
{context}

Provide a structured summary including:
1. **Goal Achievement**: Was the goal accomplished?
2. **Key Actions**: What major steps were taken?
3. **Results**: What was produced/accomplished?
4. **Challenges**: Any issues encountered and how they were resolved?
5. **Files/Outputs**: What files or outputs were created?

EXECUTION SUMMARY:"""
        
        summary = self._call_llm(prompt, max_tokens=1500)
        
        # Save summary
        summary_file = self.workspace_dir / "execution_summary.md"
        summary_file.write_text(summary, encoding='utf-8')
        
        print("\\n" + "="*60)
        print("📋 EXECUTION SUMMARY")
        print("="*60)
        print(summary)
        print("="*60)
    
    # Utility methods
    
    def _build_system_context(self) -> str:
        """Build system context for LLM"""
        return f"""
        - LLMunix Pure Markdown Operating System
        - Runtime: LLM Interpreter (autonomous)
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
        log_entry = f"\\n## {step} - {timestamp}\\n\\n{content}\\n"
        
        history_file = self.state_dir / "history.md"
        current_history = history_file.read_text(encoding='utf-8') if history_file.exists() else ""
        updated_history = current_history + log_entry
        
        history_file.write_text(updated_history, encoding='utf-8')
    
    def _update_context(self, content: str):
        """Update execution context"""
        timestamp = datetime.now().isoformat()
        context_entry = f"\\n**{timestamp}:** {content}\\n"
        
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
    
    parser = argparse.ArgumentParser(description='LLMunix LLM Interpreter')
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
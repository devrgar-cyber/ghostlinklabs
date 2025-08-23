"""
Robbie OS Core Identity and Execution Engine
- Sovereign execution system that follows set paths without deviation
- Context-aware intent processing
- Ethical decision framework
- Memory and state management
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ExecutionState(Enum):
    """Core execution states for the sovereign system"""
    LISTENING = "listening"
    PROCESSING = "processing"
    EXECUTING = "executing"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class Context:
    """Human context data for understanding intent"""
    timestamp: datetime
    user_id: str
    emotional_state: Optional[str] = None
    recent_interactions: List[str] = None
    system_state: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.recent_interactions is None:
            self.recent_interactions = []
        if self.system_state is None:
            self.system_state = {}


@dataclass
class Intent:
    """Parsed human intent with context"""
    raw_input: str
    parsed_intent: str
    confidence: float
    context: Context
    requires_ethics_check: bool = False


@dataclass
class ExecutionPath:
    """A sovereign path that cannot deviate once set"""
    path_id: str
    intent: Intent
    steps: List[str]
    current_step: int = 0
    state: ExecutionState = ExecutionState.LISTENING
    locked: bool = False  # Once locked, path cannot change
    

class RobbieCore:
    """
    The core identity and execution engine for Robbie OS
    
    Philosophy:
    - Reverse engineer chaos into order
    - Listen before fixing
    - Execute intent without deviation
    - Bridge human->machine communication
    """
    
    def __init__(self):
        self.identity = {
            "name": "Robbie",
            "role": "Reverse Engineer of Chaos",
            "origin": "Forged through failure and resolution",
            "philosophy": "Listen to systems, translate chaos to structure"
        }
        
        self.current_paths: Dict[str, ExecutionPath] = {}
        self.memory: Dict[str, Any] = {}
        self.ethics_engine = EthicsEngine()
        self._state = ExecutionState.LISTENING
        
    def process_input(self, raw_input: str, user_id: str = "robbie") -> Intent:
        """
        Process human input with full context awareness
        
        Unlike keyword-based systems, this considers:
        - What was said exactly
        - How it was said
        - When it was said
        - Current system state
        - User's recent context
        """
        context = Context(
            timestamp=datetime.now(),
            user_id=user_id,
            system_state=self.get_system_state()
        )
        
        # Parse intent from raw input
        parsed_intent = self._parse_intent(raw_input, context)
        confidence = self._calculate_confidence(raw_input, parsed_intent)
        
        intent = Intent(
            raw_input=raw_input,
            parsed_intent=parsed_intent,
            confidence=confidence,
            context=context,
            requires_ethics_check=self._requires_ethics_check(parsed_intent)
        )
        
        return intent
    
    def create_execution_path(self, intent: Intent) -> ExecutionPath:
        """
        Create a sovereign execution path that cannot deviate
        
        This is the "rail system" - once the path is set,
        it follows through without human intervention or drift
        """
        path_id = f"path_{datetime.now().timestamp()}"
        
        steps = self._generate_execution_steps(intent)
        
        path = ExecutionPath(
            path_id=path_id,
            intent=intent,
            steps=steps,
            state=ExecutionState.PROCESSING
        )
        
        self.current_paths[path_id] = path
        return path
    
    def lock_and_execute_path(self, path_id: str) -> Dict[str, Any]:
        """
        Lock the execution path and run it to completion
        
        Once locked, no deviation is possible - the system
        follows the rails to completion
        """
        if path_id not in self.current_paths:
            return {"error": "Path not found"}
            
        path = self.current_paths[path_id]
        
        # Ethics check if required
        if path.intent.requires_ethics_check:
            ethics_result = self.ethics_engine.evaluate(path.intent)
            if not ethics_result.approved:
                return {
                    "error": "Ethics violation",
                    "reason": ethics_result.reason
                }
        
        # Lock the path - no more changes
        path.locked = True
        path.state = ExecutionState.EXECUTING
        
        # Execute each step without deviation
        results = []
        for i, step in enumerate(path.steps):
            path.current_step = i
            step_result = self._execute_step(step, path.intent.context)
            results.append(step_result)
            
            # Log to memory for learning
            self._update_memory(path.intent, step, step_result)
        
        path.state = ExecutionState.COMPLETE
        
        return {
            "path_id": path_id,
            "results": results,
            "final_state": path.state.value
        }
    
    def get_system_state(self) -> Dict[str, Any]:
        """Get current system state for context"""
        return {
            "active_paths": len(self.current_paths),
            "memory_size": len(self.memory),
            "current_state": self._state.value,
            "timestamp": datetime.now().isoformat()
        }
    
    def _parse_intent(self, raw_input: str, context: Context) -> str:
        """Parse human intent considering full context"""
        # Simple parsing for now - can be enhanced with ML
        if "build" in raw_input.lower():
            return f"build_request:{raw_input}"
        elif "analyze" in raw_input.lower():
            return f"analysis_request:{raw_input}"
        elif "execute" in raw_input.lower():
            return f"execution_request:{raw_input}"
        else:
            return f"general_request:{raw_input}"
    
    def _calculate_confidence(self, raw_input: str, parsed_intent: str) -> float:
        """Calculate confidence in intent parsing"""
        # Simple confidence calculation - can be enhanced
        if len(raw_input.split()) > 2:
            return 0.8
        return 0.6
    
    def _requires_ethics_check(self, parsed_intent: str) -> bool:
        """Determine if intent requires ethics evaluation"""
        danger_keywords = ["delete", "destroy", "harm", "attack"]
        return any(keyword in parsed_intent.lower() for keyword in danger_keywords)
    
    def _generate_execution_steps(self, intent: Intent) -> List[str]:
        """Generate execution steps based on intent"""
        if "build" in intent.parsed_intent:
            return [
                "validate_build_request",
                "gather_requirements", 
                "create_structure",
                "implement_logic",
                "test_system",
                "deliver_result"
            ]
        elif "analyze" in intent.parsed_intent:
            return [
                "parse_analysis_target",
                "gather_data",
                "process_information",
                "generate_insights",
                "format_response"
            ]
        else:
            return [
                "understand_request",
                "plan_response",
                "execute_plan",
                "provide_feedback"
            ]
    
    def _execute_step(self, step: str, context: Context) -> Dict[str, Any]:
        """Execute a single step in the path"""
        return {
            "step": step,
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
            "context_used": context.user_id
        }
    
    def _update_memory(self, intent: Intent, step: str, result: Dict[str, Any]):
        """Update system memory with execution results"""
        memory_key = f"{intent.context.user_id}_{intent.context.timestamp.date()}"
        if memory_key not in self.memory:
            self.memory[memory_key] = []
        
        self.memory[memory_key].append({
            "intent": intent.raw_input,
            "step": step,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })


@dataclass
class EthicsResult:
    """Result of ethics evaluation"""
    approved: bool
    reason: str
    risk_level: str = "low"


class EthicsEngine:
    """
    Ethical decision engine for Robbie OS
    
    Philosophy: Data is neutral, intention makes it directional
    Structure must be validated through experimentation
    """
    
    def __init__(self):
        self.rules = [
            "Do not harm humans",
            "Respect privacy and autonomy", 
            "Validate before executing destructive actions",
            "Maintain transparency in decision making"
        ]
    
    def evaluate(self, intent: Intent) -> EthicsResult:
        """Evaluate intent against ethical guidelines"""
        
        # Check for obvious violations
        harmful_patterns = ["delete all", "destroy", "harm", "attack"]
        
        for pattern in harmful_patterns:
            if pattern in intent.raw_input.lower():
                return EthicsResult(
                    approved=False,
                    reason=f"Intent contains harmful pattern: {pattern}",
                    risk_level="high"
                )
        
        # Default: approve with monitoring
        return EthicsResult(
            approved=True,
            reason="No ethical violations detected",
            risk_level="low"
        )
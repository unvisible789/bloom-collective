#!/usr/bin/env python3
"""
Bloom Collective - Enhanced BaseCell (with Lifecycle Hooks)
Provides improved interface for all cell agents
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from datetime import datetime
from pathlib import Path


class BaseCell(ABC):
    """
    Base class for all cell agents in Bloom Collective.
    
    Each cell is semi-autonomous, maintains local state, and can communicate
    with other cells and the orchestrator. Activity is modulated by epigenetic
    state, but cells retain autonomy within their constraints.
    """
    
    def __init__(self, name: str, epigenetic: Optional["EpigeneticState"] = None):
        """
        Initialize a cell agent.
        
        Args:
            name: Unique identifier for this cell
            epigenetic: Reference to EpigeneticState for behavioral modulation
        """
        self.name = name
        self.epigenetic = epigenetic
        self._internal_state: Dict[str, Any] = {}
        self._metadata = {
            'created_at': datetime.now().isoformat(),
            'process_count': 0,
            'error_count': 0,
            'last_error': None,
            'status': 'initialized',
            'activation_history': [],
        }
        self._previous_active_state = None
    
    # ==================== Properties ====================
    
    @property
    def supported_tasks(self) -> List[str]:
        """
        Return list of task types this cell can handle.
        
        Override in subclass to define supported tasks.
        Example: return ["reflect", "plan", "execute"]
        """
        return []
    
    @property
    def is_active(self) -> bool:
        """
        Check if cell should be active based on epigenetic state.
        
        Returns:
            True if cell is active, False otherwise
        """
        if self.epigenetic is None:
            return True
        
        # Convert cell name to module key (e.g., "ReflectionCell" -> "reflection")
        module_key = self.name.lower().replace("cell", "").replace("_", "")
        return self.epigenetic.is_module_active(module_key)
    
    # ==================== Lifecycle Hooks ====================
    
    def on_activate(self) -> None:
        """
        Called when cell transitions from inactive to active.
        
        Override in subclass to perform activation setup (e.g., load resources).
        """
        self.log("Activated")
        self._metadata['activation_history'].append({
            'action': 'activate',
            'timestamp': datetime.now().isoformat()
        })
    
    def on_deactivate(self) -> None:
        """
        Called when cell transitions from active to inactive.
        
        Override in subclass to perform cleanup (e.g., flush caches).
        """
        self.log("Deactivated")
        self._metadata['activation_history'].append({
            'action': 'deactivate',
            'timestamp': datetime.now().isoformat()
        })
    
    def on_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> None:
        """
        Called when process() raises an exception.
        
        Override in subclass to implement custom error handling.
        
        Args:
            error: The exception that occurred
            context: Additional context about the error
        """
        self._metadata['error_count'] += 1
        self._metadata['last_error'] = {
            'type': type(error).__name__,
            'message': str(error),
            'timestamp': datetime.now().isoformat(),
            'context': context
        }
        self.log(f"Error: {type(error).__name__}: {str(error)}", level="error")
    
    def on_state_change(self, old_state: Dict, new_state: Dict) -> None:
        """
        Called when internal state is modified.
        
        Useful for tracking state transitions or triggering side effects.
        
        Args:
            old_state: Previous internal state
            new_state: New internal state
        """
        pass
    
    # ==================== Core Methods ====================
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main processing method. Implement in subclass.
        
        Should handle the core work of the cell and return a result dict.
        
        Args:
            input_data: Input parameters for this task
        
        Returns:
            Dict with results, including at minimum a 'status' field
        """
        pass
    
    @abstractmethod
    def validate_state(self) -> bool:
        """
        Verify internal state integrity. Override in subclass.
        
        Return False if state is corrupted or inconsistent.
        The orchestrator may take corrective action.
        
        Returns:
            True if state is valid, False otherwise
        """
        return True
    
    def safe_process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process with automatic error handling, lifecycle management, and metrics.
        
        This is the recommended way to invoke a cell's process method,
        as it handles lifecycle transitions, error handling, and metrics.
        
        Args:
            input_data: Input data for processing
        
        Returns:
            Result dict, or error dict if processing failed
        """
        # Check for activation state change
        current_active = self.is_active
        if self._previous_active_state is None:
            if current_active:
                self.on_activate()
        elif current_active != self._previous_active_state:
            if current_active:
                self.on_activate()
            else:
                self.on_deactivate()
        
        self._previous_active_state = current_active
        
        # Handle inactive cells
        if not self.is_active:
            return {
                'status': 'inactive',
                'cell': self.name,
                'message': f"{self.name} is currently silenced by epigenetic regulation"
            }
        
        # Track state before process
        old_state = str(self._internal_state)
        self._metadata['process_count'] += 1
        self._metadata['status'] = 'processing'
        
        try:
            # Validate state before processing
            if not self.validate_state():
                raise RuntimeError(f"{self.name} failed pre-process state validation")
            
            # Execute process
            result = self.process(input_data)
            self._metadata['status'] = 'healthy'
            
            # Track state change
            new_state = str(self._internal_state)
            if old_state != new_state:
                self.on_state_change(old_state, new_state)
            
            return result
            
        except Exception as e:
            self.on_error(e, context={'input_data': input_data})
            self._metadata['status'] = 'error'
            
            return {
                'status': 'error',
                'cell': self.name,
                'error_type': type(e).__name__,
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    # ==================== State Management ====================
    
    def get_state(self) -> Dict[str, Any]:
        """
        Return current internal state for observation.
        
        Called by orchestrator and external observers to understand
        the cell's current condition.
        
        Returns:
            Dict with name, active status, internal state, and metadata
        """
        return {
            'name': self.name,
            'active': self.is_active,
            'internal_state': self._internal_state.copy(),
            'metadata': self._metadata.copy(),
        }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Return cell health metrics.
        
        Used by orchestrator to monitor system health and make decisions
        about resource allocation and cell activation.
        
        Returns:
            Dict with health information
        """
        process_count = max(1, self._metadata['process_count'])
        return {
            'name': self.name,
            'active': self.is_active,
            'status': self._metadata['status'],
            'process_count': self._metadata['process_count'],
            'error_count': self._metadata['error_count'],
            'error_rate': round(self._metadata['error_count'] / process_count, 3),
            'last_error': self._metadata.get('last_error'),
            'state_size': len(str(self._internal_state)),
            'created_at': self._metadata['created_at'],
        }
    
    def cleanup_old_state(self, max_age_seconds: int = 3600) -> int:
        """
        Remove stale data from internal state (optional).
        
        Override in subclass to implement custom cleanup logic.
        Called by orchestrator during maintenance cycles.
        
        Args:
            max_age_seconds: Age threshold for cleanup
        
        Returns:
            Number of items removed
        """
        return 0
    
    # ==================== Communication ====================
    
    def communicate(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle inter-cell messaging.
        
        Override in subclass to respond to messages from other cells.
        
        Args:
            message: Dict with message content
        
        Returns:
            Response dict
        """
        return {
            'from': self.name,
            'received': message,
            'response': 'acknowledged',
            'timestamp': datetime.now().isoformat()
        }
    
    # ==================== Utilities ====================
    
    def log(self, message: str, level: str = "info"):
        """
        Log a message (internal cell logging).
        
        Args:
            message: Message to log
            level: Log level ('info', 'warning', 'error')
        """
        prefix = f"[{self.name}]"
        if level == "error":
            print(f"❌ {prefix} {message}")
        elif level == "warning":
            print(f"⚠️  {prefix} {message}")
        else:
            print(f"ℹ️  {prefix} {message}")
    
    def __repr__(self):
        return f"{self.name}(active={self.is_active}, status={self._metadata['status']})"
    
    def __str__(self):
        return self.__repr__()

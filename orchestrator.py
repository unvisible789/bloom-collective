#!/usr/bin/env python3
"""
Bloom Collective - Enhanced Orchestrator with Task Queue & Retry Logic
Provides robust task execution, queuing, and coordination
"""

from typing import Any, Dict, List, Optional, Callable
from collections import deque
from enum import Enum
from datetime import datetime

try:
    from epigenetic_state import EpigeneticState
    from base_cell import BaseCell
except ImportError:
    EpigeneticState = None
    BaseCell = None


class TaskStatus(str, Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRIED = "retried"
    CANCELLED = "cancelled"


class Task:
    """Represents a unit of work to be executed"""
    
    def __init__(self, task_id: str, task_type: str, input_data: Dict[str, Any],
                 required_cells: Optional[List[str]] = None, max_retries: int = 3,
                 timeout_seconds: Optional[int] = None, priority: int = 0):
        """
        Initialize a task.
        
        Args:
            task_id: Unique identifier for this task
            task_type: Type of task (e.g., "reflect", "plan")
            input_data: Input parameters for the task
            required_cells: List of required cells for execution
            max_retries: Maximum retry attempts on failure
            timeout_seconds: Task timeout in seconds
            priority: Task priority (higher = more important)
        """
        self.id = task_id
        self.type = task_type
        self.input = input_data
        self.required_cells = required_cells or []
        self.max_retries = max_retries
        self.retries = 0
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.timeout_seconds = timeout_seconds
        self.priority = priority
    
    def get_duration_ms(self) -> Optional[float]:
        """Get task execution duration in milliseconds"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds() * 1000
        return None
    
    def is_expired(self) -> bool:
        """Check if task has exceeded its timeout"""
        if not self.timeout_seconds or not self.started_at:
            return False
        elapsed = (datetime.now() - self.started_at).total_seconds()
        return elapsed > self.timeout_seconds
    
    def __repr__(self):
        return f"Task({self.id[:4]}, {self.type}, {self.status.value})"


class EnhancedOrchestrator:
    """
    Advanced orchestrator with task queuing, retry logic, and lifecycle management
    """
    
    def __init__(self, epigenetic: Optional[EpigeneticState] = None,
                 max_queue_size: int = 100):
        """
        Initialize enhanced orchestrator.
        
        Args:
            epigenetic: Reference to EpigeneticState
            max_queue_size: Maximum tasks in queue
        """
        self.epigenetic = epigenetic
        self.cells: Dict[str, BaseCell] = {}
        self.task_queue: deque = deque(maxlen=max_queue_size)
        self.task_history: List[Dict[str, Any]] = []
        self.log_entries: List[Dict[str, Any]] = []
        self.performance_metrics: Dict[str, List[float]] = {}
        self.callbacks: Dict[str, List[Callable]] = {
            'task_completed': [],
            'task_failed': [],
            'cell_activated': [],
            'cell_deactivated': [],
        }
    
    # ==================== Cell Management ====================
    
    def register_cell(self, cell: BaseCell):
        """Register a new cell agent"""
        self.cells[cell.name] = cell
        self._log(f"Registered cell: {cell.name}")
    
    def unregister_cell(self, cell_name: str):
        """Unregister a cell agent"""
        if cell_name in self.cells:
            del self.cells[cell_name]
            self._log(f"Unregistered cell: {cell_name}")
    
    def get_active_cells(self) -> List[BaseCell]:
        """Get currently active cells"""
        if self.epigenetic is None:
            return list(self.cells.values())
        return [cell for cell in self.cells.values() if cell.is_active]
    
    def get_cell_health(self) -> Dict[str, Dict[str, Any]]:
        """Get health status of all cells"""
        health = {}
        for cell_name, cell in self.cells.items():
            health[cell_name] = cell.health_check()
        return health
    
    # ==================== Task Queue Management ====================
    
    def enqueue_task(self, task_type: str, input_data: Dict[str, Any],
                     required_cells: Optional[List[str]] = None,
                     max_retries: int = 3, priority: int = 0) -> str:
        """
        Queue a task for execution.
        
        Args:
            task_type: Type of task
            input_data: Input parameters
            required_cells: Required cells for execution
            max_retries: Max retry attempts
            priority: Task priority
        
        Returns:
            Task ID
        """
        import uuid
        task_id = str(uuid.uuid4())[:8]
        task = Task(task_id, task_type, input_data, required_cells, max_retries, priority=priority)
        
        # Insert based on priority (higher priority first)
        self.task_queue.append(task)
        # Simple priority reordering (could use heapq for production)
        if priority > 0:
            queue_list = list(self.task_queue)
            queue_list.sort(key=lambda t: t.priority, reverse=True)
            self.task_queue.clear()
            self.task_queue.extend(queue_list)
        
        self._log(f"Task {task_id} enqueued (type: {task_type}, priority: {priority})")
        return task_id
    
    def process_queue(self, limit: Optional[int] = None):
        """
        Process queued tasks with retry logic.
        
        Args:
            limit: Max tasks to process in this cycle
        """
        processed = 0
        while self.task_queue and (limit is None or processed < limit):
            task = self.task_queue.popleft()
            self._execute_task_with_retry(task)
            processed += 1
        
        self._log(f"Processed {processed} tasks from queue")
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending task"""
        for task in self.task_queue:
            if task.id == task_id:
                task.status = TaskStatus.CANCELLED
                self._log(f"Cancelled task {task_id}")
                return True
        return False
    
    # ==================== Task Execution ====================
    
    def _execute_task_with_retry(self, task: Task):
        """Execute task with automatic retry on failure"""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()
        
        try:
            # Validate required cells are available
            if task.required_cells:
                available = {c.name for c in self.get_active_cells()}
                missing = set(task.required_cells) - available
                if missing:
                    raise RuntimeError(f"Missing required cells: {missing}")
            
            # Execute task
            task.result = self.run_task(task.type, task.input)
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            
            # Record performance
            duration = task.get_duration_ms()
            if duration:
                self._record_performance(task.type, duration)
            
            self._trigger_callbacks('task_completed', task)
            self._log(f"Task {task.id} completed in {duration:.1f}ms")
            
        except Exception as e:
            task.error = str(e)
            
            if task.retries < task.max_retries:
                task.retries += 1
                task.status = TaskStatus.RETRIED
                self.task_queue.append(task)
                self._log(f"Task {task.id} retried ({task.retries}/{task.max_retries}): {str(e)}")
            else:
                task.status = TaskStatus.FAILED
                task.completed_at = datetime.now()
                self._trigger_callbacks('task_failed', task)
                self._log(f"Task {task.id} failed after {task.max_retries} retries: {str(e)}")
        
        # Save to history
        self.task_history.append({
            'id': task.id,
            'type': task.type,
            'status': task.status.value,
            'retries': task.retries,
            'duration_ms': task.get_duration_ms(),
            'completed_at': datetime.now().isoformat()
        })
    
    # ==================== Task Execution (Direct) ====================
    
    def run_task(self, task_type: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a task across active cells.
        
        Args:
            task_type: Type of task
            input_data: Task input parameters
        
        Returns:
            Dict with results from all cells handling this task
        """
        results = {}
        active_cells = self.get_active_cells()
        
        cells_executed = []
        for cell in active_cells:
            if task_type in getattr(cell, 'supported_tasks', []):
                try:
                    result = cell.safe_process(input_data)
                    results[cell.name] = result
                    cells_executed.append(cell.name)
                except Exception as e:
                    results[cell.name] = {"status": "error", "message": str(e)}
        
        return {
            'task': task_type,
            'active_cells_used': cells_executed,
            'results': results,
            'timestamp': datetime.now().isoformat(),
        }
    
    # ==================== Performance Monitoring ====================
    
    def _record_performance(self, task_type: str, duration_ms: float):
        """Record task performance metric"""
        if task_type not in self.performance_metrics:
            self.performance_metrics[task_type] = []
        self.performance_metrics[task_type].append(duration_ms)
    
    def get_performance_report(self) -> Dict[str, Dict[str, float]]:
        """Get performance statistics"""
        report = {}
        for task_type, times in self.performance_metrics.items():
            if times:
                report[task_type] = {
                    'avg_ms': sum(times) / len(times),
                    'min_ms': min(times),
                    'max_ms': max(times),
                    'count': len(times),
                }
        return report
    
    # ==================== Callbacks ====================
    
    def on(self, event: str, callback: Callable):
        """Register event callback"""
        if event in self.callbacks:
            self.callbacks[event].append(callback)
    
    def _trigger_callbacks(self, event: str, *args):
        """Trigger registered callbacks for event"""
        if event in self.callbacks:
            for callback in self.callbacks[event]:
                try:
                    callback(*args)
                except Exception as e:
                    self._log(f"Callback error: {str(e)}", level="error")
    
    # ==================== Logging & Diagnostics ====================
    
    def _log(self, message: str, level: str = "info"):
        """Log orchestrator message"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message
        }
        self.log_entries.append(entry)
        if level == "error":
            print(f"❌ [Orchestrator] {message}")
        else:
            print(f"ℹ️  [Orchestrator] {message}")
    
    def get_diagnostics(self) -> Dict[str, Any]:
        """Get system diagnostics"""
        return {
            'cells_registered': len(self.cells),
            'cells_active': len(self.get_active_cells()),
            'queue_size': len(self.task_queue),
            'tasks_executed': len(self.task_history),
            'cell_health': self.get_cell_health(),
            'performance': self.get_performance_report(),
        }
    
    def __repr__(self):
        return f"EnhancedOrchestrator(cells={len(self.cells)}, queue={len(self.task_queue)})"


# Legacy compatibility wrapper
class SimpleOrchestrator(EnhancedOrchestrator):
    """Backward compatible SimpleOrchestrator"""
    pass

#!/usr/bin/env python3
"""
Bloom Collective - Enhanced Error Handler
Provides comprehensive error tracking, logging, and diagnostics
"""

import logging
import json
import traceback
from typing import Any, Dict, Optional, List
from datetime import datetime
from pathlib import Path


class BloomErrorHandler:
    """Enhanced error handling with context tracking and persistence"""
    
    def __init__(self, log_path: str = "memory/error_log.json"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.max_stored_errors = 100
        self.setup_logging()
        self._load_existing_logs()
    
    def setup_logging(self):
        """Configure Python logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_path.parent / "bloom.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('BloomCollective')
    
    def _load_existing_logs(self):
        """Load error history from disk"""
        if self.log_path.exists():
            try:
                with open(self.log_path, 'r') as f:
                    data = json.load(f)
                    self.errors = data.get('errors', [])[-self.max_stored_errors:]
                    self.warnings = data.get('warnings', [])[-50:]
            except Exception:
                pass
    
    def handle_cell_error(self, cell_name: str, error: Exception, 
                         context: Optional[Dict[str, Any]] = None,
                         severity: str = "error"):
        """
        Log cell-specific errors with full context
        
        Args:
            cell_name: Name of the cell where error occurred
            error: The exception object
            context: Additional context information
            severity: 'error', 'warning', or 'critical'
        """
        error_record = {
            'timestamp': datetime.now().isoformat(),
            'cell': cell_name,
            'error_type': type(error).__name__,
            'message': str(error),
            'context': context or {},
            'traceback': traceback.format_exc(),
            'severity': severity,
        }
        
        self.errors.append(error_record)
        self.logger.error(
            f"[{cell_name}] {severity.upper()}: {str(error)}",
            extra={'context': context},
            exc_info=True
        )
        
        self._persist_logs()
        
        return error_record
    
    def handle_task_error(self, task_id: str, task_type: str, error: Exception,
                         context: Optional[Dict[str, Any]] = None):
        """Log task execution errors"""
        error_record = {
            'timestamp': datetime.now().isoformat(),
            'task_id': task_id,
            'task_type': task_type,
            'error_type': type(error).__name__,
            'message': str(error),
            'context': context or {},
            'traceback': traceback.format_exc(),
            'severity': 'error',
        }
        
        self.errors.append(error_record)
        self.logger.error(f"[Task {task_id}] {str(error)}", exc_info=True)
        self._persist_logs()
        
        return error_record
    
    def log_warning(self, source: str, message: str, 
                   context: Optional[Dict[str, Any]] = None):
        """Log non-critical warnings"""
        warning_record = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'message': message,
            'context': context or {},
        }
        
        self.warnings.append(warning_record)
        self.logger.warning(f"[{source}] {message}")
        self._persist_logs()
        
        return warning_record
    
    def _persist_logs(self):
        """Save error and warning logs to disk"""
        try:
            data = {
                'version': '0.1.0',
                'timestamp': datetime.now().isoformat(),
                'errors': self.errors[-self.max_stored_errors:],
                'warnings': self.warnings[-50:],
            }
            with open(self.log_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to persist logs: {str(e)}")
    
    def get_error_summary(self, limit: int = 10) -> Dict[str, Any]:
        """Get summary of recent errors"""
        recent_errors = self.errors[-limit:]
        
        # Aggregate by error type
        error_types = {}
        for error in recent_errors:
            err_type = error['error_type']
            if err_type not in error_types:
                error_types[err_type] = 0
            error_types[err_type] += 1
        
        # Aggregate by source (cell or task)
        sources = {}
        for error in recent_errors:
            source = error.get('cell') or error.get('task_id') or 'unknown'
            if source not in sources:
                sources[source] = 0
            sources[source] += 1
        
        return {
            'total_errors': len(self.errors),
            'recent_count': len(recent_errors),
            'error_types': error_types,
            'sources': sources,
            'recent_errors': recent_errors,
        }
    
    def clear_old_errors(self, days: int = 7):
        """Remove errors older than specified days"""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)
        
        original_count = len(self.errors)
        self.errors = [
            e for e in self.errors
            if datetime.fromisoformat(e['timestamp']) > cutoff
        ]
        removed = original_count - len(self.errors)
        self.logger.info(f"Cleared {removed} errors older than {days} days")
        self._persist_logs()
    
    def __repr__(self):
        return f"BloomErrorHandler(errors={len(self.errors)}, warnings={len(self.warnings)})"


# Global error handler instance
_global_error_handler: Optional[BloomErrorHandler] = None

def get_error_handler() -> BloomErrorHandler:
    """Get or create global error handler instance"""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = BloomErrorHandler()
    return _global_error_handler

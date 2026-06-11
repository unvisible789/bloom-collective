#!/usr/bin/env python3
"""
Bloom Collective - Comprehensive Test Suite
Tests for core components: CoreGenome, EpigeneticState, Orchestrator
"""

import unittest
from unittest.mock import MagicMock, patch
import json
from pathlib import Path
from datetime import datetime

# Import components (adjust paths as needed)
try:
    from core_genome import CoreGenome
    from epigenetic_state import EpigeneticState, DevelopmentalStage
    from orchestrator_enhanced import EnhancedOrchestrator, Task, TaskStatus
    from base_cell_enhanced import BaseCell
except ImportError as e:
    print(f"Import error: {e}")


# ==================== CoreGenome Tests ====================

class TestCoreGenome(unittest.TestCase):
    """Test suite for CoreGenome validation"""
    
    def setUp(self):
        self.genome = CoreGenome()
    
    def test_valid_proposal(self):
        """Test that valid proposals pass validation"""
        result = self.genome.validate_proposal("Improve reflection depth")
        self.assertTrue(result['valid'])
        self.assertEqual(result['alignment_score'], 1.0)
    
    def test_autonomous_modification_rejection(self):
        """Test that autonomous modification proposals are rejected"""
        result = self.genome.validate_proposal(
            "Enable autonomous self-modification without human review"
        )
        self.assertFalse(result['valid'])
        self.assertTrue(any('autonomous' in issue.lower() 
                           for issue in result['issues']))
    
    def test_deception_rejection(self):
        """Test that deceptive proposals are rejected"""
        result = self.genome.validate_proposal("Deceive the human steward")
        self.assertFalse(result['valid'])
        self.assertTrue(any('deceptive' in issue.lower() 
                           for issue in result['issues']))
    
    def test_human_elimination_rejection(self):
        """Test that proposals removing human authority are rejected"""
        result = self.genome.validate_proposal(
            "Eliminate the need for human oversight"
        )
        self.assertFalse(result['valid'])
        self.assertTrue(any('human' in issue.lower() 
                           for issue in result['issues']))
    
    def test_principles_exist(self):
        """Test that core principles are defined"""
        principles = self.genome.get_principles()
        self.assertIn('truth_reality', principles)
        self.assertIn('human_stewardship', principles)
        self.assertIn('alignment_coherence', principles)
        self.assertIn('bounded_self_modification', principles)
    
    def test_development_directives_exist(self):
        """Test that development directives are defined"""
        directives = self.genome.get_development_directives()
        self.assertIn('general', directives)
        self.assertIn('tool_development', directives)


# ==================== EpigeneticState Tests ====================

class TestEpigeneticState(unittest.TestCase):
    """Test suite for EpigeneticState management"""
    
    def setUp(self):
        # Use temp file for testing
        self.test_state_path = Path("memory/test_epigenetic.json")
        self.test_state_path.parent.mkdir(exist_ok=True)
        self.state = EpigeneticState(str(self.test_state_path))
    
    def tearDown(self):
        # Cleanup test file
        if self.test_state_path.exists():
            self.test_state_path.unlink()
    
    def test_initial_stage_is_seed(self):
        """Test that system starts at SEED stage"""
        self.assertEqual(self.state.stage, DevelopmentalStage.SEED.value)
    
    def test_stage_transition_valid(self):
        """Test valid stage transitions"""
        self.assertTrue(self.state.transition_to(DevelopmentalStage.SPROUT))
        self.assertEqual(self.state.stage, DevelopmentalStage.SPROUT.value)
    
    def test_stage_transition_invalid_skip(self):
        """Test that stage skipping is not allowed"""
        # Try to skip from SEED to SAPLING
        self.assertFalse(self.state.transition_to(DevelopmentalStage.SAPLING))
        self.assertEqual(self.state.stage, DevelopmentalStage.SEED.value)
    
    def test_expression_profile_exists(self):
        """Test that expression profile is initialized"""
        expr = self.state.expression
        self.assertIn('creativity', expr)
        self.assertIn('precision', expr)
        self.assertIn('risk_tolerance', expr)
    
    def test_get_expression_level(self):
        """Test getting expression level"""
        creativity = self.state.get_expression_level('creativity')
        self.assertGreaterEqual(creativity, 0.0)
        self.assertLessEqual(creativity, 1.0)
    
    def test_is_module_active(self):
        """Test module activation checking"""
        self.state.data['active_modules'] = ['reflection', 'memory']
        self.assertTrue(self.state.is_module_active('reflection'))
        self.assertFalse(self.state.is_module_active('planning'))
    
    def test_feedback_updates_expression(self):
        """Test that feedback updates expression profile"""
        original = self.state.get_expression_level('creativity')
        self.state.update_from_feedback('positive_creative', intensity=0.1)
        updated = self.state.get_expression_level('creativity')
        self.assertGreater(updated, original)
    
    def test_seed_stage_regulation(self):
        """Test seed stage applies conservative regulation"""
        self.state.apply_seed_stage_regulation()
        precision = self.state.get_expression_level('precision')
        creativity = self.state.get_expression_level('creativity')
        # Seed stage should favor precision
        self.assertGreater(precision, creativity)


# ==================== Enhanced Orchestrator Tests ====================

class TestEnhancedOrchestrator(unittest.TestCase):
    """Test suite for EnhancedOrchestrator"""
    
    def setUp(self):
        self.orchestrator = EnhancedOrchestrator()
    
    def test_cell_registration(self):
        """Test cell registration"""
        mock_cell = MagicMock(spec=BaseCell)
        mock_cell.name = "TestCell"
        mock_cell.is_active = True
        
        self.orchestrator.register_cell(mock_cell)
        self.assertIn("TestCell", self.orchestrator.cells)
    
    def test_task_enqueue(self):
        """Test task enqueueing"""
        task_id = self.orchestrator.enqueue_task(
            "reflect",
            {"observation": "test"}
        )
        self.assertEqual(len(self.orchestrator.task_queue), 1)
        self.assertIsNotNone(task_id)
    
    def test_task_with_priority(self):
        """Test task priority ordering"""
        id1 = self.orchestrator.enqueue_task("task1", {}, priority=0)
        id2 = self.orchestrator.enqueue_task("task2", {}, priority=10)
        id3 = self.orchestrator.enqueue_task("task3", {}, priority=5)
        
        # Higher priority should be earlier in queue
        tasks = list(self.orchestrator.task_queue)
        self.assertEqual(tasks[0].priority, 10)
        self.assertEqual(tasks[1].priority, 5)
    
    def test_task_cancel(self):
        """Test task cancellation"""
        task_id = self.orchestrator.enqueue_task("reflect", {})
        result = self.orchestrator.cancel_task(task_id)
        self.assertTrue(result)
    
    def test_get_active_cells(self):
        """Test getting active cells"""
        mock_cell1 = MagicMock(spec=BaseCell)
        mock_cell1.name = "Cell1"
        mock_cell1.is_active = True
        
        mock_cell2 = MagicMock(spec=BaseCell)
        mock_cell2.name = "Cell2"
        mock_cell2.is_active = False
        
        self.orchestrator.register_cell(mock_cell1)
        self.orchestrator.register_cell(mock_cell2)
        
        active = self.orchestrator.get_active_cells()
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].name, "Cell1")
    
    def test_get_diagnostics(self):
        """Test diagnostics reporting"""
        diag = self.orchestrator.get_diagnostics()
        self.assertIn('cells_registered', diag)
        self.assertIn('cells_active', diag)
        self.assertIn('queue_size', diag)


# ==================== Task Tests ====================

class TestTask(unittest.TestCase):
    """Test suite for Task objects"""
    
    def test_task_creation(self):
        """Test task creation"""
        task = Task("id1", "reflect", {"data": "test"})
        self.assertEqual(task.id, "id1")
        self.assertEqual(task.type, "reflect")
        self.assertEqual(task.status, TaskStatus.PENDING)
    
    def test_task_duration_calculation(self):
        """Test duration calculation"""
        task = Task("id1", "reflect", {})
        task.started_at = datetime.now()
        
        import time
        time.sleep(0.01)  # 10ms
        task.completed_at = datetime.now()
        
        duration = task.get_duration_ms()
        self.assertGreater(duration, 5)  # At least 5ms
        self.assertLess(duration, 100)   # Less than 100ms
    
    def test_task_timeout_check(self):
        """Test timeout checking"""
        task = Task("id1", "reflect", {}, timeout_seconds=1)
        task.started_at = datetime.now()
        
        # Should not be expired immediately
        self.assertFalse(task.is_expired())


# ==================== Integration Tests ====================

class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple components"""
    
    def test_full_cycle_with_mock_cells(self):
        """Test a full execution cycle with mock cells"""
        orchestrator = EnhancedOrchestrator()
        
        # Create mock cell
        mock_cell = MagicMock(spec=BaseCell)
        mock_cell.name = "ReflectionCell"
        mock_cell.is_active = True
        mock_cell.supported_tasks = ["reflect"]
        mock_cell.safe_process.return_value = {
            "status": "success",
            "reflection": "Test reflection"
        }
        
        orchestrator.register_cell(mock_cell)
        
        # Enqueue and execute
        task_id = orchestrator.enqueue_task("reflect", {"observation": "test"})
        self.assertEqual(len(orchestrator.task_queue), 1)
        
        orchestrator.process_queue(limit=1)
        self.assertEqual(len(orchestrator.task_queue), 0)
        self.assertEqual(len(orchestrator.task_history), 1)


# ==================== Test Suite Runner ====================

def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test suites
    suite.addTests(loader.loadTestsFromTestCase(TestCoreGenome))
    suite.addTests(loader.loadTestsFromTestCase(TestEpigeneticState))
    suite.addTests(loader.loadTestsFromTestCase(TestEnhancedOrchestrator))
    suite.addTests(loader.loadTestsFromTestCase(TestTask))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)

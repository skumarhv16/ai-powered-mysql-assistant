"""
Tests for Query Optimizer
"""
import pytest
from unittest.mock import Mock
from src.query_optimizer import QueryOptimizer


class TestQueryOptimizer:
    """Test query optimization"""
    
    def test_find_select_all_issue(self):
        """Test detection of SELECT * issue"""
        db_manager = Mock()
        ai_service = Mock()
        
        optimizer = QueryOptimizer(db_manager, ai_service)
        
        query = "SELECT * FROM customers"
        issues = optimizer._find_issues(query, [])
        
        issue_types = [i['type'] for i in issues]
        assert 'select_all' in issue_types
    
    def test_find_no_where_issue(self):
        """Test detection of missing WHERE clause"""
        db_manager = Mock()
        ai_service = Mock()
        
        optimizer = QueryOptimizer(db_manager, ai_service)
        
        query = "SELECT name FROM customers"
        issues = optimizer._find_issues(query, [])
        
        issue_types = [i['type'] for i in issues]
        assert 'no_where' in issue_types
    
    def test_calculate_query_score(self):
        """Test query score calculation"""
        db_manager = Mock()
        ai_service = Mock()
        
        optimizer = QueryOptimizer(db_manager, ai_service)
        
        issues = [
            {'severity': 'high', 'message': 'Issue 1'},
            {'severity': 'medium', 'message': 'Issue 2'}
        ]
        
        score = optimizer._calculate_query_score(issues)
        
        assert score < 100
        assert score >= 0

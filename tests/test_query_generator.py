"""
Tests for Query Generator
"""
import pytest
from unittest.mock import Mock, patch
from src.query_generator import QueryGenerator


class TestQueryGenerator:
    """Test query generation"""
    
    def test_generate_simple_query(self):
        """Test simple query generation"""
        ai_service = Mock()
        ai_service.generate_sql.return_value = "SELECT * FROM customers LIMIT 10"
        
        db_manager = Mock()
        db_manager.explain_query.return_value = []
        
        generator = QueryGenerator(ai_service, db_manager)
        
        query = generator.generate(
            "Show me customers",
            {'tables': {'customers': {'columns': []}}}
        )
        
        assert 'SELECT' in query.upper()
        assert 'customers' in query.lower()
    
    def test_validate_query_success(self):
        """Test query validation success"""
        ai_service = Mock()
        db_manager = Mock()
        db_manager.explain_query.return_value = []
        
        generator = QueryGenerator(ai_service, db_manager)
        
        is_valid, error = generator._validate_query("SELECT * FROM customers")
        
        assert is_valid
        assert error is None
    
    def test_validate_query_failure(self):
        """Test query validation failure"""
        ai_service = Mock()
        db_manager = Mock()
        
        generator = QueryGenerator(ai_service, db_manager)
        
        is_valid, error = generator._validate_query("DROP TABLE customers")
        
        assert not is_valid
        assert error is not None

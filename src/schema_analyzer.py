"""
Database Schema Analyzer
Analyzes and provides schema context
"""
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class SchemaAnalyzer:
    """Analyzes database schema"""
    
    def __init__(self, db_manager):
        """
        Initialize schema analyzer
        
        Args:
            db_manager: Database manager instance
        """
        self.db_manager = db_manager
        self.schema_cache = None
    
    def get_schema_context(self) -> Dict:
        """
        Get schema context for AI
        
        Returns:
            Schema context dictionary
        """
        if self.schema_cache:
            return self.schema_cache
        
        self.schema_cache = self.analyze_schema()
        return self.schema_cache
    
    def analyze_schema(self) -> Dict:
        """
        Analyze complete database schema
        
        Returns:
            Complete schema information
        """
        logger.info("Analyzing database schema")
        
        tables = self.db_manager.get_tables()
        schema = {'tables': {}}
        
        for table in tables:
            table_schema = self.db_manager.get_table_schema(table)
            
            schema['tables'][table] = {
                'columns': [
                    {
                        'name': col['Field'],
                        'type': col['Type'],
                        'null': col['Null'],
                        'key': col['Key'],
                        'default': col['Default']
                    }
                    for col in table_schema
                ]
            }
        
        return schema
    
    def find_relationships(self) -> List[Dict]:
        """
        Find relationships between tables
        
        Returns:
            List of relationships
        """
        # In production, would query INFORMATION_SCHEMA
        return []
    
    def is_loaded(self) -> bool:
        """Check if schema is loaded"""
        return self.schema_cache is not None

"""
Natural Language to SQL Query Generator
Uses AI to convert natural language to SQL
"""
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class QueryGenerator:
    """Generates SQL queries from natural language"""
    
    def __init__(self, ai_service, db_manager):
        """
        Initialize query generator
        
        Args:
            ai_service: AI service instance
            db_manager: Database manager instance
        """
        self.ai_service = ai_service
        self.db_manager = db_manager
    
    def generate(self, description: str, schema_context: Dict) -> str:
        """
        Generate SQL query from natural language
        
        Args:
            description: Natural language description
            schema_context: Database schema information
            
        Returns:
            SQL query string
        """
        logger.info(f"Generating query for: {description}")
        
        # Create prompt for AI
        prompt = self._create_prompt(description, schema_context)
        
        # Get SQL from AI
        query = self.ai_service.generate_sql(prompt)
        
        # Validate query
        is_valid, error = self._validate_query(query)
        
        if not is_valid:
            logger.warning(f"Generated invalid query: {error}")
            # Try to fix query
            query = self._fix_query(query, error, schema_context)
        
        return query
    
    def _create_prompt(self, description: str, schema: Dict) -> str:
        """Create prompt for AI model"""
        schema_str = self._format_schema(schema)
        
        prompt = f"""You are an expert MySQL query generator.

Database Schema:
{schema_str}

User Request: {description}

Generate a MySQL query that:
1. Answers the user's request accurately
2. Uses proper MySQL syntax
3. Follows best practices (proper joins, WHERE clauses, etc.)
4. Includes appropriate LIMIT clauses if needed
5. Returns only the SQL query, no explanations

SQL Query:"""
        
        return prompt
    
    def _format_schema(self, schema: Dict) -> str:
        """Format schema for prompt"""
        formatted = []
        
        for table_name, table_info in schema.get('tables', {}).items():
            columns = ', '.join([
                f"{col['name']} ({col['type']})"
                for col in table_info.get('columns', [])
            ])
            formatted.append(f"Table: {table_name}\nColumns: {columns}\n")
        
        return '\n'.join(formatted)
    
    def _validate_query(self, query: str) -> tuple:
        """
        Validate generated SQL query
        
        Returns:
            (is_valid, error_message)
        """
        try:
            # Basic syntax check
            if not query.strip().upper().startswith('SELECT'):
                if any(word in query.upper() for word in ['DROP', 'DELETE', 'TRUNCATE', 'UPDATE', 'INSERT']):
                    return False, "Only SELECT queries are allowed"
            
            # Try to explain the query (validates syntax)
            self.db_manager.explain_query(query)
            
            return True, None
            
        except Exception as e:
            return False, str(e)
    
    def _fix_query(self, query: str, error: str, schema: Dict) -> str:
        """Attempt to fix invalid query"""
        logger.info(f"Attempting to fix query error: {error}")
        
        fix_prompt = f"""The following MySQL query has an error:

Query: {query}
Error: {error}

Database Schema:
{self._format_schema(schema)}

Please provide a corrected version of the query that fixes the error.
Return only the corrected SQL query, no explanations.

Corrected Query:"""
        
        fixed_query = self.ai_service.generate_sql(fix_prompt)
        return fixed_query

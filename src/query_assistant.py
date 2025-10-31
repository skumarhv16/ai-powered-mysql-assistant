"""
Main Query Assistant - Orchestrates AI and MySQL operations
"""
import logging
from typing import Dict, List, Optional
import pandas as pd

from .query_generator import QueryGenerator
from .query_optimizer import QueryOptimizer
from .database_manager import DatabaseManager
from .ai_service import AIService
from .schema_analyzer import SchemaAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueryAssistant:
    """
    AI-powered MySQL query assistant
    Combines AI capabilities with MySQL expertise
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize Query Assistant
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        
        # Initialize components
        self.db_manager = DatabaseManager(self.config)
        self.ai_service = AIService(self.config)
        self.query_generator = QueryGenerator(
            self.ai_service,
            self.db_manager
        )
        self.query_optimizer = QueryOptimizer(
            self.db_manager,
            self.ai_service
        )
        self.schema_analyzer = SchemaAnalyzer(self.db_manager)
        
        logger.info("Query Assistant initialized successfully")
    
    def ask(self, question: str) -> Dict:
        """
        Ask a question in natural language and get results
        
        Args:
            question: Natural language question
            
        Returns:
            Dictionary containing query, results, and explanation
        """
        logger.info(f"Processing question: {question}")
        
        try:
            # Get database schema context
            schema_context = self.schema_analyzer.get_schema_context()
            
            # Generate SQL query
            query = self.query_generator.generate(
                question,
                schema_context
            )
            
            logger.info(f"Generated query: {query}")
            
            # Execute query
            results = self.db_manager.execute_query(query)
            
            # Get AI explanation
            explanation = self.ai_service.explain_results(
                question,
                query,
                results
            )
            
            # Get optimization suggestions
            optimization = self.query_optimizer.analyze(query)
            
            return {
                'success': True,
                'question': question,
                'query': query,
                'results': results,
                'explanation': explanation,
                'optimization': optimization,
                'row_count': len(results) if results else 0
            }
            
        except Exception as e:
            logger.error(f"Error processing question: {e}")
            return {
                'success': False,
                'error': str(e),
                'question': question
            }
    
    def generate_query(self, description: str) -> str:
        """
        Generate SQL query from natural language description
        
        Args:
            description: Natural language description
            
        Returns:
            SQL query string
        """
        schema_context = self.schema_analyzer.get_schema_context()
        return self.query_generator.generate(description, schema_context)
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute SQL query and return results
        
        Args:
            query: SQL query string
            
        Returns:
            DataFrame with results
        """
        return self.db_manager.execute_query(query)
    
    def optimize_query(self, query: str) -> Dict:
        """
        Optimize existing SQL query
        
        Args:
            query: SQL query to optimize
            
        Returns:
            Optimization results and suggestions
        """
        return self.query_optimizer.optimize(query)
    
    def explain_query(self, query: str) -> str:
        """
        Explain SQL query in plain language
        
        Args:
            query: SQL query to explain
            
        Returns:
            Plain language explanation
        """
        return self.ai_service.explain_query(query)
    
    def explain_results(self, results: pd.DataFrame) -> str:
        """
        Generate AI explanation of query results
        
        Args:
            results: Query results DataFrame
            
        Returns:
            AI-generated explanation
        """
        return self.ai_service.explain_dataframe(results)
    
    def generate_documentation(self) -> Dict:
        """
        Generate comprehensive database documentation
        
        Returns:
            Dictionary containing documentation
        """
        logger.info("Generating database documentation")
        
        schema = self.schema_analyzer.analyze_schema()
        relationships = self.schema_analyzer.find_relationships()
        
        # Use AI to generate descriptions
        documentation = {
            'schema': schema,
            'relationships': relationships,
            'descriptions': {}
        }
        
        for table_name in schema['tables']:
            description = self.ai_service.generate_table_description(
                table_name,
                schema['tables'][table_name]
            )
            documentation['descriptions'][table_name] = description
        
        return documentation
    
    def get_insights(self, table_name: str) -> Dict:
        """
        Get AI-powered insights about a table
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary of insights
        """
        # Get table statistics
        stats = self.db_manager.get_table_statistics(table_name)
        
        # Get sample data
        sample_data = self.db_manager.execute_query(
            f"SELECT * FROM {table_name} LIMIT 100"
        )
        
        # Generate AI insights
        insights = self.ai_service.generate_insights(
            table_name,
            stats,
            sample_data
        )
        
        return insights
    
    def suggest_indexes(self, query: str) -> List[str]:
        """
        Suggest indexes to improve query performance
        
        Args:
            query: SQL query
            
        Returns:
            List of index suggestions
        """
        return self.query_optimizer.suggest_indexes(query)
    
    def health_check(self) -> Dict:
        """
        Check health of database and assistant
        
        Returns:
            Health check results
        """
        return {
            'database': self.db_manager.health_check(),
            'ai_service': self.ai_service.health_check(),
            'schema_loaded': self.schema_analyzer.is_loaded()
        }

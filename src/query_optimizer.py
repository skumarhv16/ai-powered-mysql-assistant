"""
SQL Query Optimizer
Analyzes and optimizes MySQL queries
"""
import logging
import re
from typing import Dict, List

logger = logging.getLogger(__name__)


class QueryOptimizer:
    """Optimizes MySQL queries for better performance"""
    
    def __init__(self, db_manager, ai_service):
        """
        Initialize query optimizer
        
        Args:
            db_manager: Database manager instance
            ai_service: AI service instance
        """
        self.db_manager = db_manager
        self.ai_service = ai_service
    
    def optimize(self, query: str) -> Dict:
        """
        Optimize SQL query
        
        Args:
            query: SQL query to optimize
            
        Returns:
            Optimization results
        """
        logger.info(f"Optimizing query: {query[:100]}...")
        
        # Analyze execution plan
        execution_plan = self.db_manager.explain_query(query)
        
        # Find optimization opportunities
        issues = self._find_issues(query, execution_plan)
        
        # Generate optimized query
        optimized_query = self._generate_optimized_query(query, issues)
        
        # Get index suggestions
        index_suggestions = self.suggest_indexes(query)
        
        # Get AI recommendations
        ai_recommendations = self.ai_service.get_optimization_advice(
            query,
            execution_plan,
            issues
        )
        
        return {
            'original_query': query,
            'optimized_query': optimized_query,
            'issues_found': issues,
            'index_suggestions': index_suggestions,
            'ai_recommendations': ai_recommendations,
            'execution_plan': execution_plan
        }
    
    def analyze(self, query: str) -> Dict:
        """
        Analyze query without optimization
        
        Args:
            query: SQL query to analyze
            
        Returns:
            Analysis results
        """
        execution_plan = self.db_manager.explain_query(query)
        issues = self._find_issues(query, execution_plan)
        
        return {
            'query': query,
            'issues': issues,
            'execution_plan': execution_plan,
            'score': self._calculate_query_score(issues)
        }
    
    def _find_issues(self, query: str, execution_plan: List[Dict]) -> List[Dict]:
        """Find performance issues in query"""
        issues = []
        
        # Check for SELECT *
        if re.search(r'SELECT\s+\*', query, re.IGNORECASE):
            issues.append({
                'type': 'select_all',
                'severity': 'medium',
                'message': 'Using SELECT * can retrieve unnecessary columns',
                'suggestion': 'Specify only the columns you need'
            })
        
        # Check for missing WHERE clause
        if not re.search(r'WHERE', query, re.IGNORECASE):
            if re.search(r'FROM\s+\w+', query, re.IGNORECASE):
                issues.append({
                    'type': 'no_where',
                    'severity': 'high',
                    'message': 'Query has no WHERE clause, may scan entire table',
                    'suggestion': 'Add WHERE clause to filter results'
                })
        
        # Check for table scans in execution plan
        for step in execution_plan:
            if step.get('type') == 'ALL':
                issues.append({
                    'type': 'table_scan',
                    'severity': 'high',
                    'table': step.get('table'),
                    'message': f"Full table scan on {step.get('table')}",
                    'suggestion': 'Consider adding an index'
                })
        
        # Check for filesort
        for step in execution_plan:
            if 'Using filesort' in step.get('Extra', ''):
                issues.append({
                    'type': 'filesort',
                    'severity': 'medium',
                    'message': 'Query requires filesort operation',
                    'suggestion': 'Add index on ORDER BY columns'
                })
        
        # Check for temporary table
        for step in execution_plan:
            if 'Using temporary' in step.get('Extra', ''):
                issues.append({
                    'type': 'temporary_table',
                    'severity': 'medium',
                    'message': 'Query creates temporary table',
                    'suggestion': 'Optimize joins or use covering index'
                })
        
        return issues
    
    def _generate_optimized_query(self, query: str, issues: List[Dict]) -> str:
        """Generate optimized version of query"""
        optimized = query
        
        # Replace SELECT *
        if any(i['type'] == 'select_all' for i in issues):
            # In production, would analyze actual columns needed
            optimized = re.sub(
                r'SELECT\s+\*',
                'SELECT id, name, created_at',  # Example
                optimized,
                flags=re.IGNORECASE
            )
        
        # Add LIMIT if missing and no WHERE
        if any(i['type'] == 'no_where' for i in issues):
            if not re.search(r'LIMIT', optimized, re.IGNORECASE):
                optimized += ' LIMIT 1000'
        
        return optimized
    
    def suggest_indexes(self, query: str) -> List[str]:
        """
        Suggest indexes for query
        
        Args:
            query: SQL query
            
        Returns:
            List of CREATE INDEX statements
        """
        suggestions = []
        
        # Extract table and WHERE columns
        tables = re.findall(r'FROM\s+(\w+)', query, re.IGNORECASE)
        where_columns = re.findall(
            r'WHERE\s+(\w+)\s*[=<>]',
            query,
            re.IGNORECASE
        )
        join_columns = re.findall(
            r'ON\s+\w+\.(\w+)\s*=',
            query,
            re.IGNORECASE
        )
        order_columns = re.findall(
            r'ORDER\s+BY\s+(\w+)',
            query,
            re.IGNORECASE
        )
        
        # Suggest indexes
        for table in tables:
            for column in set(where_columns + join_columns):
                suggestions.append(
                    f"CREATE INDEX idx_{table}_{column} ON {table}({column});"
                )
            
            if order_columns:
                order_cols = ', '.join(set(order_columns))
                suggestions.append(
                    f"CREATE INDEX idx_{table}_order ON {table}({order_cols});"
                )
        
        return suggestions
    
    def _calculate_query_score(self, issues: List[Dict]) -> int:
        """Calculate query performance score (0-100)"""
        score = 100
        
        severity_penalties = {
            'low': 5,
            'medium': 15,
            'high': 30
        }
        
        for issue in issues:
            penalty = severity_penalties.get(issue.get('severity', 'low'), 5)
            score -= penalty
        
        return max(0, score)

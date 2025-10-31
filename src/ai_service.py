"""
AI Service Integration
Handles communication with AI models (OpenAI/Gemini)
"""
import logging
import os
from typing import Dict, List
import pandas as pd

logger = logging.getLogger(__name__)


class AIService:
    """Integrates with AI models for natural language processing"""
    
    def __init__(self, config: Dict):
        """
        Initialize AI service
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = config.get('model', 'gpt-4')
        
        if not self.api_key:
            logger.warning("No API key found, using mock responses")
            self.mock_mode = True
        else:
            self.mock_mode = False
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialize AI client"""
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
            logger.info("OpenAI client initialized")
        except ImportError:
            logger.warning("OpenAI package not found, using mock mode")
            self.mock_mode = True
        except Exception as e:
            logger.error(f"Failed to initialize AI client: {e}")
            self.mock_mode = True
    
    def generate_sql(self, prompt: str) -> str:
        """
        Generate SQL query from prompt
        
        Args:
            prompt: Input prompt
            
        Returns:
            SQL query string
        """
        if self.mock_mode:
            return self._mock_sql_generation(prompt)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert MySQL query generator. Return only SQL queries without explanations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            query = response.choices[0].message.content.strip()
            
            # Clean up response
            query = query.replace('```sql', '').replace('```', '').strip()
            
            return query
            
        except Exception as e:
            logger.error(f"AI SQL generation failed: {e}")
            return self._mock_sql_generation(prompt)
    
    def explain_query(self, query: str) -> str:
        """
        Explain SQL query in plain language
        
        Args:
            query: SQL query
            
        Returns:
            Plain language explanation
        """
        if self.mock_mode:
            return f"This query retrieves data from the database with specific conditions."
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a database expert. Explain SQL queries in simple language."
                    },
                    {
                        "role": "user",
                        "content": f"Explain this SQL query:\n\n{query}"
                    }
                ],
                temperature=0.5,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Query explanation failed: {e}")
            return "Query explanation unavailable."
    
    def explain_results(
        self,
        question: str,
        query: str,
        results: pd.DataFrame
    ) -> str:
        """
        Generate explanation of query results
        
        Args:
            question: Original question
            query: SQL query executed
            results: Query results
            
        Returns:
            Natural language explanation
        """
        if self.mock_mode:
            return f"Found {len(results)} results matching your criteria."
        
        try:
            results_summary = self._summarize_results(results)
            
            prompt = f"""Question: {question}

Query Used: {query}

Results Summary:
{results_summary}

Provide a clear, concise explanation of these results in 2-3 sentences."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a data analyst. Explain query results clearly."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Results explanation failed: {e}")
            return f"Query returned {len(results)} rows."
    
    def explain_dataframe(self, df: pd.DataFrame) -> str:
        """
        Explain DataFrame contents
        
        Args:
            df: DataFrame to explain
            
        Returns:
            Explanation text
        """
        summary = self._summarize_results(df)
        return f"The data contains {len(df)} records with the following characteristics:\n{summary}"
    
    def get_optimization_advice(
        self,
        query: str,
        execution_plan: List[Dict],
        issues: List[Dict]
    ) -> str:
        """
        Get AI recommendations for query optimization
        
        Args:
            query: SQL query
            execution_plan: Query execution plan
            issues: Identified issues
            
        Returns:
            Optimization advice
        """
        if self.mock_mode:
            return "Consider adding indexes and avoiding table scans."
        
        try:
            issues_text = '\n'.join([
                f"- {issue['message']}" for issue in issues
            ])
            
            prompt = f"""Query: {query}

Issues Found:
{issues_text}

Provide 3 specific recommendations to optimize this query."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a database performance expert."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Optimization advice failed: {e}")
            return "Optimization advice unavailable."
    
    def generate_table_description(
        self,
        table_name: str,
        schema: List[Dict]
    ) -> str:
        """
        Generate description for a table
        
        Args:
            table_name: Name of table
            schema: Table schema
            
        Returns:
            Description text
        """
        if self.mock_mode:
            return f"Table {table_name} stores related data."
        
        columns = ', '.join([col['Field'] for col in schema])
        
        prompt = f"""Table Name: {table_name}
Columns: {columns}

Write a 1-2 sentence description of what this table likely stores."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Table description generation failed: {e}")
            return f"Table: {table_name}"
    
    def generate_insights(
        self,
        table_name: str,
        stats: Dict,
        sample_data: pd.DataFrame
    ) -> Dict:
        """
        Generate AI-powered insights about a table
        
        Args:
            table_name: Name of table
            stats: Table statistics
            sample_data: Sample data
            
        Returns:
            Dictionary of insights
        """
        return {
            'summary': f"Table {table_name} contains {stats.get('row_count', 0)} records",
            'size': f"Size: {stats.get('size_mb', 0)} MB",
            'columns': list(sample_data.columns),
            'sample_rows': len(sample_data)
        }
    
    def _summarize_results(self, df: pd.DataFrame) -> str:
        """Create summary of DataFrame"""
        summary = f"Rows: {len(df)}, Columns: {len(df.columns)}\n"
        summary += f"Columns: {', '.join(df.columns.tolist())}\n"
        
        if len(df) > 0:
            summary += f"First row preview: {df.iloc[0].to_dict()}"
        
        return summary
    
    def _mock_sql_generation(self, prompt: str) -> str:
        """Generate mock SQL for testing"""
        if 'customer' in prompt.lower():
            return "SELECT * FROM customers WHERE state = 'CA' LIMIT 10;"
        elif 'order' in prompt.lower():
            return "SELECT * FROM orders WHERE order_date > '2024-01-01' LIMIT 10;"
        else:
            return "SELECT * FROM table LIMIT 10;"
    
    def health_check(self) -> Dict:
        """Check AI service health"""
        return {
            'status': 'healthy' if not self.mock_mode else 'mock_mode',
            'model': self.model,
            'mock_mode': self.mock_mode
        }

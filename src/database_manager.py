"""
MySQL Database Manager
Handles all database operations
"""
import logging
import mysql.connector
from mysql.connector import pooling
from typing import Dict, List, Optional
import pandas as pd

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages MySQL database connections and operations"""
    
    def __init__(self, config: Dict):
        """
        Initialize database manager
        
        Args:
            config: Database configuration
        """
        self.config = config
        self.pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize connection pool"""
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name="mysql_pool",
                pool_size=5,
                host=self.config.get('host', 'localhost'),
                port=self.config.get('port', 3306),
                user=self.config.get('user', 'root'),
                password=self.config.get('password', ''),
                database=self.config.get('database', 'test')
            )
            logger.info("Database connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise
    
    def execute_query(self, query: str, params: tuple = None) -> pd.DataFrame:
        """
        Execute SQL query and return results as DataFrame
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            DataFrame with results
        """
        connection = None
        try:
            connection = self.pool.get_connection()
            
            # Execute query
            df = pd.read_sql_query(query, connection, params=params)
            
            logger.info(f"Query executed successfully, returned {len(df)} rows")
            return df
            
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
        finally:
            if connection:
                connection.close()
    
    def explain_query(self, query: str) -> List[Dict]:
        """
        Get query execution plan
        
        Args:
            query: SQL query
            
        Returns:
            List of execution plan steps
        """
        connection = None
        try:
            connection = self.pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            # Get execution plan
            cursor.execute(f"EXPLAIN {query}")
            plan = cursor.fetchall()
            
            cursor.close()
            return plan
            
        except Exception as e:
            logger.error(f"EXPLAIN failed: {e}")
            return []
        finally:
            if connection:
                connection.close()
    
    def get_tables(self) -> List[str]:
        """Get list of all tables"""
        connection = None
        try:
            connection = self.pool.get_connection()
            cursor = connection.cursor()
            
            cursor.execute("SHOW TABLES")
            tables = [row[0] for row in cursor.fetchall()]
            
            cursor.close()
            return tables
            
        except Exception as e:
            logger.error(f"Failed to get tables: {e}")
            return []
        finally:
            if connection:
                connection.close()
    
    def get_table_schema(self, table_name: str) -> List[Dict]:
        """
        Get schema information for a table
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of column information
        """
        connection = None
        try:
            connection = self.pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute(f"DESCRIBE {table_name}")
            schema = cursor.fetchall()
            
            cursor.close()
            return schema
            
        except Exception as e:
            logger.error(f"Failed to get schema for {table_name}: {e}")
            return []
        finally:
            if connection:
                connection.close()
    
    def get_table_statistics(self, table_name: str) -> Dict:
        """
        Get statistics for a table
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary of statistics
        """
        connection = None
        try:
            connection = self.pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            row_count = cursor.fetchone()['count']
            
            # Get table size
            cursor.execute(f"""
                SELECT 
                    table_name,
                    ROUND(((data_length + index_length) / 1024 / 1024), 2) as size_mb
                FROM information_schema.TABLES
                WHERE table_schema = DATABASE()
                AND table_name = '{table_name}'
            """)
            size_info = cursor.fetchone()
            
            cursor.close()
            
            return {
                'table_name': table_name,
                'row_count': row_count,
                'size_mb': size_info['size_mb'] if size_info else 0
            }
            
        except Exception as e:
            logger.error(f"Failed to get statistics for {table_name}: {e}")
            return {}
        finally:
            if connection:
                connection.close()
    
    def health_check(self) -> Dict:
        """
        Check database connection health
        
        Returns:
            Health check results
        """
        try:
            connection = self.pool.get_connection()
            cursor = connection.cursor()
            
            cursor.execute("SELECT 1")
            cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            return {
                'status': 'healthy',
                'connected': True
            }
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'connected': False,
                'error': str(e)
            }

"""
Streamlit Web Interface
Interactive UI for the MySQL AI Assistant
"""
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

from src.query_assistant import QueryAssistant

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI-Powered MySQL Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize assistant
@st.cache_resource
def get_assistant():
    """Initialize and cache assistant"""
    config = {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'port': int(os.getenv('MYSQL_PORT', 3306)),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'database': os.getenv('MYSQL_DATABASE', 'test'),
        'model': 'gpt-4'
    }
    return QueryAssistant(config)

# Main app
def main():
    """Main application"""
    st.title("🤖 AI-Powered MySQL Assistant")
    st.markdown("*Natural language database queries powered by AI*")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Mode selection
        mode = st.selectbox(
            "Select Mode",
            ["Ask Question", "Optimize Query", "Database Insights"]
        )
        
        st.markdown("---")
        
        # Health check
        if st.button("Health Check"):
            assistant = get_assistant()
            health = assistant.health_check()
            st.json(health)
    
    # Main content area
    if mode == "Ask Question":
        show_ask_interface()
    elif mode == "Optimize Query":
        show_optimize_interface()
    elif mode == "Database Insights":
        show_insights_interface()


def show_ask_interface():
    """Show question asking interface"""
    st.header("💬 Ask a Question")
    
    # Example questions
    with st.expander("📝 Example Questions"):
        st.markdown("""
        - Show me all customers from California
        - What's the average order value by month?
        - Find products that haven't sold in 30 days
        - List top 10 customers by lifetime value
        - Compare sales this year vs last year
        """)
    
    # Question input
    question = st.text_input(
        "Ask a question about your database:",
        placeholder="e.g., Show me top 10 customers by revenue"
    )
    
    if st.button("🚀 Generate & Execute", type="primary"):
        if question:
            with st.spinner("Processing your question..."):
                assistant = get_assistant()
                result = assistant.ask(question)
                
                if result['success']:
                    # Display generated query
                    st.subheader("📝 Generated SQL Query")
                    st.code(result['query'], language='sql')
                    
                    # Display results
                    st.subheader("📊 Results")
                    st.dataframe(result['results'], use_container_width=True)
                    
                    # Display AI explanation
                    st.subheader("💡 AI Explanation")
                    st.info(result['explanation'])
                    
                    # Display optimization suggestions
                    if result['optimization']['issues_found']:
                        st.subheader("⚡ Performance Notes")
                        for issue in result['optimization']['issues_found']:
                            st.warning(f"**{issue['type']}**: {issue['message']}")
                else:
                    st.error(f"Error: {result['error']}")
        else:
            st.warning("Please enter a question")


def show_optimize_interface():
    """Show query optimization interface"""
    st.header("⚡ Query Optimizer")
    
    query = st.text_area(
        "Enter SQL Query to Optimize:",
        height=150,
        placeholder="SELECT * FROM customers WHERE state = 'CA'"
    )
    
    if st.button("🔍 Analyze & Optimize", type="primary"):
        if query:
            with st.spinner("Analyzing query..."):
                assistant = get_assistant()
                result = assistant.optimize_query(query)
                
                # Original query
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Original Query")
                    st.code(result['original_query'], language='sql')
                
                with col2:
                    st.subheader("Optimized Query")
                    st.code(result['optimized_query'], language='sql')
                
                # Issues found
                if result['issues_found']:
                    st.subheader("⚠️ Issues Found")
                    for issue in result['issues_found']:
                        severity_color = {
                            'high': '🔴',
                            'medium': '🟡',
                            'low': '🟢'
                        }
                        st.write(
                            f"{severity_color.get(issue['severity'], '⚪')} "
                            f"**{issue['message']}**"
                        )
                        st.caption(f"💡 {issue['suggestion']}")
                
                # Index suggestions
                if result['index_suggestions']:
                    st.subheader("📌 Index Suggestions")
                    for suggestion in result['index_suggestions']:
                        st.code(suggestion, language='sql')
                
                # AI recommendations
                st.subheader("🤖 AI Recommendations")
                st.info(result['ai_recommendations'])
        else:
            st.warning("Please enter a query")


def show_insights_interface():
    """Show database insights interface"""
    st.header("📊 Database Insights")
    
    assistant = get_assistant()
    
    # Get tables
    tables = assistant.db_manager.get_tables()
    
    if tables:
        selected_table = st.selectbox("Select Table", tables)
        
        if st.button("🔍 Analyze Table", type="primary"):
            with st.spinner(f"Analyzing {selected_table}..."):
                # Get table info
                schema = assistant.db_manager.get_table_schema(selected_table)
                stats = assistant.db_manager.get_table_statistics(selected_table)
                insights = assistant.get_insights(selected_table)
                
                # Display schema
                st.subheader("📋 Schema")
                schema_df = pd.DataFrame(schema)
                st.dataframe(schema_df, use_container_width=True)
                
                # Display statistics
                st.subheader("📈 Statistics")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Rows", f"{stats['row_count']:,}")
                with col2:
                    st.metric("Size", f"{stats['size_mb']} MB")
                
                # Display insights
                st.subheader("💡 AI Insights")
                st.json(insights)
    else:
        st.warning("No tables found in database")


if __name__ == "__main__":
    main()

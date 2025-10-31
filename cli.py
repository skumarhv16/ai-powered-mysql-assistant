"""
Command Line Interface for MySQL AI Assistant
"""
import argparse
import sys
from dotenv import load_dotenv
from src.query_assistant import QueryAssistant
import json

load_dotenv()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='AI-Powered MySQL Assistant CLI'
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Generate query from natural language')
    query_parser.add_argument('question', help='Question in natural language')
    
    # Optimize command
    optimize_parser = subparsers.add_parser('optimize', help='Optimize SQL query')
    optimize_parser.add_argument('query', help='SQL query to optimize')
    
    # Explain command
    explain_parser = subparsers.add_parser('explain', help='Explain SQL query')
    explain_parser.add_argument('query', help='SQL query to explain')
    
    # Docs command
    docs_parser = subparsers.add_parser('docs', help='Generate database documentation')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize assistant
    assistant = QueryAssistant()
    
    # Execute command
    if args.command == 'query':
        result = assistant.ask(args.question)
        print_query_result(result)
    
    elif args.command == 'optimize':
        result = assistant.optimize_query(args.query)
        print_optimization_result(result)
    
    elif args.command == 'explain':
        explanation = assistant.explain_query(args.query)
        print(f"\n📝 Explanation:\n{explanation}\n")
    
    elif args.command == 'docs':
        docs = assistant.generate_documentation()
        print(json.dumps(docs, indent=2))


def print_query_result(result):
    """Print query result"""
    if result['success']:
        print(f"\n✅ Success!\n")
        print(f"📝 Generated Query:\n{result['query']}\n")
        print(f"📊 Results: {result['row_count']} rows\n")
        print(result['results'].to_string())
        print(f"\n💡 Explanation:\n{result['explanation']}\n")
    else:
        print(f"\n❌ Error: {result['error']}\n")


def print_optimization_result(result):
    """Print optimization result"""
    print(f"\n⚡ Query Optimization\n")
    print(f"Original Query:\n{result['original_query']}\n")
    print(f"Optimized Query:\n{result['optimized_query']}\n")
    
    if result['issues_found']:
        print("⚠️  Issues Found:")
        for issue in result['issues_found']:
            print(f"  - {issue['message']}")
        print()
    
    if result['index_suggestions']:
        print("📌 Index Suggestions:")
        for suggestion in result['index_suggestions']:
            print(f"  {suggestion}")
        print()


if __name__ == '__main__':
    main()

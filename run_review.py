import logging
from pipeline.store import PipelineStore

logging.basicConfig(level=logging.INFO)

def main():
    print("🔥 Firecrawl Eval - Human Review CLI")
    store = PipelineStore()
    runs = store.list_runs()
    
    if not runs:
        print("No runs found. Please run the pipeline first.")
        return
        
    latest_run = runs[0]
    print(f"Loading latest run: {latest_run}")
    
    data = store.get_run(latest_run)
    if not data:
        print("Failed to load run data.")
        return
        
    print(f"Found {len(data)} test cases.")
    print("Reviewing borderline cases is not fully implemented in this script yet, but the data is ready.")
    
    # In a full implementation, we would iterate through data,
    # find test cases where overall_score is between 0.4 and 0.6,
    # print Firecrawl results and Judge reasoning,
    # and prompt the user for input.

if __name__ == "__main__":
    main()

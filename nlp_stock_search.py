from google.cloud import aiplatform
from google.cloud import bigquery

# Initialize Gemini Model in Vertex AI
def get_gemini_response(query):
    model = aiplatform.generation.TextGenerationModel("gemini-pro")
    response = model.predict(query)
    return response.text.strip()  # Ensure clean output

# Query BigQuery for stocks in the identified industry
def get_stocks_from_bigquery(industry):
    client = bigquery.Client()
    # set industry to lowercase
    industry = industry.lower()
    
    # Check if industry is valid -> TBD
    if industry not in ["tech", "healthcare", "finance", "energy", "materials", "utilities"]:
        return []  # Return empty list if invalid industry
    
    # Construct BigQuery query with parameterized input
    # This will prevent SQL injection attacks
    # Also, it will optimize query performance by reducing the number of rows processed by BigQuery
    # Note: This is just an example, actual implementation may vary based on the actual schema and requirements of your BigQuery table
    
    query = """
    SELECT symbol, name 
    FROM `bigquery-public-data.financial_stock_data.stocks`
    WHERE industry = @industry
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("industry", "STRING", industry)
        ]
    )

    results = client.query(query, job_config=job_config).result()
    return [(row["symbol"], row["name"]) for row in results]

# Main Execution
search_term = input("Please specify what kind of stocks you are looking for: ")

# Use Gemini to determine the correct industry category
query = f"What is the industry classification for {search_term} stocks?"
industry_category = get_gemini_response(query)

print(f"Industry Identified: {industry_category}")

# Fetch stocks from BigQuery
stocks = get_stocks_from_bigquery(industry_category)

# Display results
if stocks:
    print(f"Stocks in {industry_category}:")
    for symbol, name in stocks:
        print(f"- {symbol}: {name}")
else:
    print(f"No stocks found for industry '{industry_category}'")

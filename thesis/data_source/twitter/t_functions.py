# Prepare a query to search on
def query_builder(ticker, company_name=None):
    if company_name:
        print(f"Name found: {company_name}")

        # Based on the query:
        # '(Microsoft OR $MSFT OR #Microsoft OR #MSFT OR @Microsoft)'
        query = f"({company_name} OR ${ticker} OR #{company_name} OR #{ticker})"

    else:
        query = f"(${ticker})"

    return query


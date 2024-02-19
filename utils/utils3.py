import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


def association_rules_pipeline(customers, basket, join_column='customer_id', list_column='list_of_goods',
                              min_support=0.2, metric='lift', min_threshold=1):
    """
    Perform the association rules pipeline on customer-basket data.

    Args:
        customers (pandas.DataFrame): The customer data.
        basket (pandas.DataFrame): The basket data.
        join_column (str, optional): The column name used for joining the customer and basket data. Defaults to 'customer_id'.
        list_column (str, optional): The column name containing the list of goods in the basket. Defaults to 'list_of_goods'.
        min_support (float, optional): The minimum support threshold for generating frequent itemsets. Defaults to 0.2.
        metric (str, optional): The metric used for evaluating association rules. Defaults to 'lift'.
        min_threshold (float, optional): The minimum threshold for the metric to consider a rule. Defaults to 1.

    Returns:
        pandas.DataFrame: The generated association rules.
    """
    # Merge customer and basket data on the specified join column
    data_merged = pd.merge(basket, customers, on=join_column, how='inner')

    # Extract transactions from the merged data
    transactions = data_merged[list_column].apply(lambda x: [item.strip() for item in x[1:-1].split(',')])

    # Convert transactions to transaction matrix using TransactionEncoder
    te = TransactionEncoder()
    te_fit = te.fit(transactions).transform(transactions)
    transactions_items = pd.DataFrame(te_fit, columns=te.columns_)

    # Generate frequent itemsets using Apriori algorithm
    frequent_itemsets = apriori(transactions_items, min_support=min_support, use_colnames=True)

    # Generate association rules from frequent itemsets
    rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)

    return rules

if (workflow.optimal_cashback === 'Category not found') {
    workflow.cashback_result= "Pay by Amazon Wallet to get a discount of 5% with a saving of Rs "+((workflow.product_price)*0.05).toFixed(2);
} else if (workflow.product_price <= 500 ) {
    workflow.cashback_result = "Sorry, no cashback is available at the moment.";
} else {
    workflow.cashback_result = "The best price for your products is " + workflow.optimal_cashback.best_price + 
                               ", with a cashback discount percentage of " + workflow.optimal_cashback.cashback_percentage + 
                               "%. If you pay with " + workflow.optimal_cashback.payment_method_name + 
                               ", your total savings will be " + workflow.optimal_cashback.savings + ".";
}

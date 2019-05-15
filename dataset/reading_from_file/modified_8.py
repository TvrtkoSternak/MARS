with open("customer/data", "w") as customer_data, open("manager/data", "w") as manager_data:
    manager_checkout = calculate_manager_checkout(manager, customer)
    customer_checkout = calculate_customer_checkout(customer, manager)
    customer_data.write(customer_checkout)
    manager_data.write(manager_checkout)
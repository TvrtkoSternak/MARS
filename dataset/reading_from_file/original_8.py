customer_data = open("customer/data", "w")
manager_data = open("manager/data", "w")

manager_checkout = calculate_manager_checkout(manager, customer)
customer_checkout = calculate_customer_checkout(customer, manager)
customer_data.write(customer_checkout)
manager_data.write(manager_checkout)

customer_data.close()
manager_data.close()
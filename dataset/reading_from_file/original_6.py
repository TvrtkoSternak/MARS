customer_records = open("customer/records", "a")

new_record = calculate_record(customer)
customer_records.write(new_record)

customer_records.close()
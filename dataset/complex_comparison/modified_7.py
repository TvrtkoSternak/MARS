list_sum_less_100 = sum(list_of_elements) < 100
is_list_short = len(list_of_elements) > 50

if list_sum_less_100 and is_list_short:
    print("list is short and sum is less than 100")
    self.do_work_with_list(list_of_elements)
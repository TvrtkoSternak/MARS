if self.check_connection() and self.check_internet_availability():
    msg = self.generate_mesage()
    self.send_message(msg)
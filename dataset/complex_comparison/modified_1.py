connection = self.check_connection()
internet_available = self.check_internet_availability()

if connection and internet_available:
    msg = self.generate_mesage()
    self.send_message(msg)
elif((username != "goran123" or password != "boboneco") and (username == "" and password != "")):
            self.label_5.setText("Username field can't be blank. ")

        elif((username != "goran123" or password != "boboneco") and (username != "" and password == "")):
            self.label_5.setText("Please enter Password. ")

        elif((username != "goran123" or password != "boboneco") and (username == "" and password == "")):
            self.label_5.setText("Please enter username and password. ")
            
        elif((username != "goran123" or password != "boboneco") and (username != "" and password != "")):
            self.label_5.setText("Wrong username or pasword")

 
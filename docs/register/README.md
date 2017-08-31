# Register

## Model

### OrderLog
The purpose of this model is to log each time an exhibitor updates their complete registration (each time save or submit is pressed), in order to be able to know what is going on. It saves contact, company, timestamp, fair, action and products (listed as plain text). The difference from SignupLog is that this saves the products, and creates a new log each time the info in the registration is updated. 

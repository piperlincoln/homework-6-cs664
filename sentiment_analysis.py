#!/usr/bin/env python3

"""
Piper Lincoln
Class: CS 664 - Fall 1
Date: 10/19/22
Assignment #6
"""

from monkeylearn import MonkeyLearn

class Product:
    
    def __init__(self, id, name, cost):
        self.id = id
        self.name = name
        self.cost = cost

class Customer:
    
    def __init__(self, name):
        self.name = name
        self.product = None
        
    def buy_product(self, product):
        self.product = product
        
class NatLang:
    
    products_sold = 0
    model_id = "cl_LKWiA7ej"
    cell_number = "612-875-8793"
    email_address = "prlcrochetcreations@gmail.com"
    
    def __init__(self):
        # Instantiate the MonkeyLearn model to use for sentiment analysis.
        self.nl_api = MonkeyLearn('e4e8d778bc4deee5932d11844fab81219cbda5e7')
        
    def sell_product(self, customer, name, cost):
        # Create the new product the customer bought.
        self.products_sold += 1
        product = Product(self.products_sold, name, cost)
        customer.buy_product(product)
        
    def analyze_message(self, message, customer):
        # Perform sentiment analysis by calling the MonkeyLearn model API.
        result = self.nl_api.classifiers.classify(self.model_id, [message])
        
        if result.body[0].get('error') == False:
            # Use the sentiment with the highest confidence value.
            self.produce_response(result.body[0].get(
                'classifications')[0].get('tag_name'), customer)
        else:
            # Warn the user if there was an error during the analysis.
            print("ERROR: Unable to analyze message.")
            
    def produce_response(self, sentiment, customer):
        if sentiment == 'Positive' and customer.product is not None:
            print("""
                  I am so glad that you are happy with the final result of the
                  {0}! If you have time, please consider leaving my shop a 
                  positive review. And in the future, please use the following 
                  code for a discount: {1}. I hope to work with you again!\n"""
                  .format(customer.product.name, 
                  "STRAWBERRY" + str(customer.product.id))) 
            
        elif sentiment == 'Negative' and customer.product is not None:
            print("""
                  I am so sorry that you are unhappy with the final
                  result of the {0}. We can either work together to refine your
                  product so I can have another chance to fulfill your
                  vision, or I can issue you a refund of ${1}. Please let
                  me know which option you’d like to pursue!\n""".format(
                  customer.product.name, customer.product.cost))  
       
        elif sentiment != 'Negative' and customer.product is None:
            print("""
                  Welcome to my Etsy shop, I look forward to working with you! 
                  Please reach out to me at {0} or {1} to setup a time to 
                  discuss your interests and vision for the product! In the 
                  meantime, feel free to browse the gallery of past products 
                  to pick out any characteristics you’d like to include.\n"""
                  .format(self.cell_number, self.email_address))           
        else:
            print("""
                  Please contact me at {0} for further clarification.
                  I am available 7-5 EST M-F.\n""".format(self.email_address))
            

if __name__ == "__main__":
    # Instantiate the application to perform sentiment analysis.
    nat_lang = NatLang()
    
    # The first customers to respond to are three iterations of an angry mom.
    customer_a = Customer("Angry Mom")
    
    # Use varying language to test the applicability of the model.
    nat_lang.sell_product(customer_a, "Backyardigan Plushie", 50)
    nat_lang.analyze_message("""
                              I really hate the penguin stuffed animal 
                              that you crocheted. I told you my son was 
                              interested in the Backyardigans, but I never said 
                              his favorite character was Pablo.""", customer_a)
    
    nat_lang.sell_product(customer_a, "Arctic Plushie", 150)
    nat_lang.analyze_message("""
                              My son did not like the penguin you created.
                              I am disappointed in the idea that we came up
                              with and hoping to start over.""", customer_a)
    
    nat_lang.sell_product(customer_a, "Happy Feet Plushie", 75)
    nat_lang.analyze_message("""
                              I have mixed feelings about this penguin, but 
                              my son thinks it is ridiculous.""", customer_a)
                             
    
    # The second customers to respond to are three iterations of a happy teen.
    customer_b = Customer("Happy Teen")
    
    # Use varying language to test the applicability of the model.
    nat_lang.sell_product(customer_b, "Strawberry Cow Plushie", 25)
    nat_lang.analyze_message("""
                              I think the strawberry cow stuffed animal that 
                              you crocheted is perfect. I like the different 
                              hues of red and pink, and the strawberry shaped 
                              patches were a good touch.""", customer_b)
    
    nat_lang.sell_product(customer_b, "Mocha Cow Plushie", 100)
    nat_lang.analyze_message("""
                              Cows are my favorite animal, so I thought this 
                              product was a good fit.""", customer_b)
    
    nat_lang.sell_product(customer_b, "Tangerine Cow Plushie", 60)
    nat_lang.analyze_message("""
                              I am a fan of your handiwork. You inspired me
                              to learn how to crochet myself!""", customer_b)
    
    # The third customer to respond to is a potential new customer.
    customer_c = Customer("New Customer")
    
    nat_lang.analyze_message("""
                             I love the work you've done for other customers! 
                             I hope to work with you to make my dream come
                             to life!""", customer_c)
        
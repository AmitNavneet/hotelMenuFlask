from flask import Flask,request,render_template

app=Flask(__name__)


class Menu:
    menuItems={}

    def addToMenu(self,menuItem,menuPrice):
        Menu.menuItems.update({menuItem:menuPrice})
        #return render_template(Menu.menuItems)
        

    def removeFromMenu(self,menuItem):
        #Menu.menuItems.pop(menuItem)
        del Menu.menuItems[menuItem]

    @staticmethod
    def printMenu():
        return Menu.menuItems


class Order:
    orderedItems={}
       
    def orderItem(self,food,qty):
       
        self.foodOrdered=food
        self.foodQuantity=qty

        #print(hotelMenu.menuItems.get(food))
        

        Order.orderedItems.update({self.foodOrdered:self.foodQuantity})

    def printBill(self):
        hotelMenu=Menu()
        
        billTotal=0
        billRow=''
        for foodItem,qty in Order.orderedItems.items():
            rowTotal=0            
            price=Menu.menuItems.get(foodItem)
            rowTotal=qty*price
            billTotal+=rowTotal
            billRow+=f"{foodItem}\tRs.{ price} x {qty} Nos. = Rs.{rowTotal}<br>"

        billRow+=f"<br><br>Total Amount={billTotal}<br><br>Please visit again!"
        
        return billRow 

@app.route('/cancelOrder')
def cancelOrder():
    Order.orderedItems.clear()
    return render_template('orderFood.html',order=Order.orderedItems)





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manageMenu')
def manageMenu():
    hotelMenu=Menu()
    return render_template('addRemoveItem.html')


@app.route('/orderFood')
def orderFood():
    if 'foodItem' in request.args and 'foodQuantity' in request.args:
        food=request.args.get('foodItem')
        qty=int(request.args['foodQuantity'])
        foodItem=Order()
        foodItem.orderItem(food,qty)
    return render_template('orderFood.html',order=Order.orderedItems)

@app.route('/removeItem')
def removeItem():
    foodItem=request.args.get('foodItem')
    hotelMenu=Menu()
    hotelMenu.removeFromMenu(foodItem)
    return Menu.menuItems

@app.route('/addItem')
def addItem():

    foodPrice=request.args['foodPrice']
    foodItem=request.args.get('foodItem')
    print("additem")
    if foodPrice=='':
        priceError="Please enter the price"
        return render_template('addRemoveItem.html',priceError=priceError)
    
    foodPrice=int(foodPrice)

    hotelMenu=Menu()
    hotelMenu.addToMenu(foodItem,foodPrice)
    return Menu.menuItems

@app.route('/printMenu')
def printMenu():
    
    
    return Menu.printMenu()

@app.route('/viewOrder')
def viewOrder():
    custOrder=Order()
    return custOrder.printBill()


    

if __name__=='__main__':
    app.run(debug=True)

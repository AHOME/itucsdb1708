class RestaurantController:
    def __init__(self):
        self.restaurants = {}
        self.last_restaurant_id = 0

    def add_restaurant(self, restaurant):
        self.last_restaurant_id += 1
        self.restaurants[self.last_restaurant_id] = restaurant
        restaurant._id = self.last_restaurant_id

    def delete_restaurant(self, restaurant_id):
        del self.restaurants[restaurant_id]

    def get_restaurant(self, restaurant_id):
        return self.restaurants[restaurant_id]

    def get_restaurants(self):
        return self.restaurants

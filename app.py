from api import app
from api.models import Client, FavouriteProducts, Product, ProductType, UserType
from api import routes

if __name__ == '__main__':

    app.run(debug=True)
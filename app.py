from api import app
from api.models import Client, FavouriteProducts, Product, ProductType, UserType
from api import routes
# from api.routes import it_college, ns_members, it_college_type, ns_members_type, main_type

if __name__ == '__main__':
    # app.register_blueprint(it_college.main, url_prefix='/api/student')
    # app.register_blueprint(ns_members.main, url_prefix='/api/ns_member')
    # app.register_blueprint(it_college_type.main, url_prefix='/api/college_type')
    # app.register_blueprint(ns_members_type.main, url_prefix='/api/ns_type')
    # app.register_blueprint(main_type.main, url_prefix='/api/main_type')
    app.run(debug=True)
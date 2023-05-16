from flask.views import MethodView
from flask_smorest import Blueprint,abort

from werkzeug.security import generate_password_hash

from email_validator import validate_email

from schemas import AdSchema

from models import AdModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from db import db

from flask_jwt_extended import jwt_required, current_user

blp = Blueprint("ad" , __name__ , description = "Ad blueprint")


@blp.route("/ad/<int:ad_id>")
class AdManager(MethodView):
    @blp.response(status_code=200, schema= AdSchema)
    def get(self, ad_id):
        ad = AdModel.query.filter_by(id = ad_id).first()
        print(ad)
        
        if not ad:
            abort(
                http_status_code=404,
                message="Ad with this id not found."
            )
        
        return ad

    @jwt_required()
    def delete(self, ad_id):
        ad = AdModel.query.filter_by(id = ad_id).first()

        if not ad:
            abort(
                http_status_code=404,
                message="Ad with this id not found."
            )
        
        if not ad.creator == current_user:
            abort(
                http_status_code=403,
                message="You can not remove other ads."
            )
        
        try:
            db.session.delete(ad)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                http_status_code=500,
                message = "An error accoured while deleting ad."
            )

        return {
            "message" : "Ad deleted successfully."
        }, 200
    
    @jwt_required()
    @blp.arguments(schema=AdSchema)
    @blp.response(status_code=200, schema=AdSchema)
    def put(self, ad_data, ad_id):
        ad = AdModel.query.filter_by(id = ad_id).first()

        if not ad:
            abort(
                http_status_code=404,
                message="Ad with this id not found."
            )
        
        if not ad.creator == current_user:
            abort(
                http_status_code=403,
                message="You can not modify other ads."
            )
        
        try:
            ad.title = ad_data["title"]
            ad.description = ad_data["description"]

            db.session.add(ad)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                http_status_code=500,
                message = "An error accoured while updating ad."
            )

        return ad

@blp.route("/ad")
class CreateAd(MethodView):
    @jwt_required()
    @blp.arguments(schema=AdSchema)
    @blp.response(status_code=200,schema=AdSchema)
    def post(self, ad_data):
        try:
            ad = AdModel(title = ad_data["title"], description = ad_data["description"])
            current_user.ads.append(ad)
            db.session.add(current_user)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                http_status_code=500,
                message = "An error accoured while inserting ad."
            )
        
        return ad
    
@blp.route("/ad")
class GetAllAds(MethodView):
    @blp.response(status_code=200, schema=AdSchema(many=True))
    def get(self):
        return AdModel.query.all()
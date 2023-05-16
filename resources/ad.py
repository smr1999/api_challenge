from flask.views import MethodView
from flask_smorest import Blueprint,abort

from schemas import AdSchema

from models import AdModel
from sqlalchemy.exc import SQLAlchemyError
from db import db

from flask_jwt_extended import jwt_required, current_user

blp = Blueprint("ad" , __name__ , description = "'Operations on Ads'")


@blp.route("/ad/<int:ad_id>")
class AdManager(MethodView):
    @blp.response(status_code=200, schema= AdSchema)
    @blp.alt_response(status_code=404, 
                      description="When ad with this id not found."
    )
    def get(self, ad_id):
        """Get specific Ad with it's ad_id."""
        ad = AdModel.query.filter_by(id = ad_id).first()
        
        if not ad:
            abort(
                http_status_code=404,
                message="Ad with this id not found."
            )
        
        return ad

    @jwt_required()
    @blp.response(status_code=200)
    @blp.alt_response(status_code=404,
                      description="When ad with this id not found."
    )
    @blp.alt_response(status_code=403,
                      description="When user wants to remove other ads."
    )
    @blp.alt_response(status_code=500,
                      description="An error occured when database problem."
    )
    def delete(self, ad_id):
        """Remove specific Ad with it's ad_id."""
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
        }
    

    @jwt_required()
    @blp.arguments(schema=AdSchema)
    @blp.response(status_code=200, schema=AdSchema)
    @blp.alt_response(status_code=404,
                      description="When ad with this id not found."
    )
    @blp.alt_response(status_code=403,
                      description="When user wants to update other ads."
    )
    @blp.alt_response(status_code=500,
                      description="An error occured when database problem."
    )
    def put(self, ad_data, ad_id):
        """Modify specific Ad with it's ad_id"""
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
    @blp.alt_response(status_code=500,
                      description="An error occured when database problem."
    )
    def post(self, ad_data):
        """Create an Ad with it's title and description"""
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
        """Retrive all the ads"""
        return AdModel.query.all()
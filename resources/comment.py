from flask.views import MethodView
from flask_smorest import Blueprint,abort

from schemas import CommentSchema

from models import CommentModel, AdModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from db import db

from flask_jwt_extended import jwt_required, current_user

blp = Blueprint("comment" , __name__ , description = "'Operations on Comments'")


@blp.route("/comment/<int:ad_id>")
class CommentManager(MethodView):
    @jwt_required()
    @blp.arguments(schema=CommentSchema)
    @blp.response(status_code=200, schema=CommentSchema)
    @blp.alt_response(status_code=404,
                      description="When entered 'ad_id' not found."
    )
    @blp.alt_response(status_code=409,
                      description="When user wants to submit more that one comment for each ad."
    )
    @blp.alt_response(status_code=500,
                      description="An error occured when database problem."
    )
    def post(self, comment_data ,ad_id):
        """Comment on a specific ad"""
        ad = AdModel.query.filter_by(id = ad_id).first()

        if not ad:
            abort(
                http_status_code=404,
                message="Ad with this id not found."
            )
        
        try:
            comment_ = CommentModel(comment = comment_data["comment"], ad_id = ad_id)
            current_user.comments.append(comment_)

            db.session.add(comment_)
            db.session.commit()
        
        except IntegrityError:
            abort(
                http_status_code=409,
                message = "You can comment once on each ad."
            )
        except SQLAlchemyError:
            abort(
                http_status_code=500,
                message = "An error occured while inserting comment in the database."
            )
        
        return comment_

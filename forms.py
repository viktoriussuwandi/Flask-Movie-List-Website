from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange, length
    
class UpdateForm(FlaskForm) :
  rating = DecimalField(  label = "Rating", validators = [ NumberRange(min=0,max=10) ] )
  review = TextAreaField( label = "Review", validators = [ DataRequired(), length(max=250) ] )
  submit = SubmitField(   label = "Done")

class AddForm(FlaskForm) :
  title  = StringField(   label = "Movie Title", validators = [ DataRequired() ])
  submit = SubmitField(   label = "Add Movie")
    
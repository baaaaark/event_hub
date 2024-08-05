from . import db

class Timer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    expired = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Timer {self.title}>"

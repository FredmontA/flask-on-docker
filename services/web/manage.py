from flask.cli import FlaskGroup

from project import app, db, Ticket


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    #db.session.add(Ticket(email="michael@mherman.org"))
    db.session.add(Ticket(ticket_id="76986496: 16391710",
                          order_id="1234",
                          status_raw="ok",
                          event_id=1,
                          date="2024-01-01T10:39:32+00:00",
                          organization_id=123))
    db.session.commit()


if __name__ == "__main__":
    cli()

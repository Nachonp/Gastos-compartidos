from flask_sqlalchemy import SQLAlchemy

# Esto es como en NotePoquet, si te acuerdas
# Inicializa el objeto SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """Función para inicializar la base de datos con la aplicación Flask."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    #Si comparas línea por línea NotePoquet con éste verás que este es distinto
    #Es porque la línea del with app.app_context() redundaba estando aquí, ya que hace falta fuera
    db.init_app(app)
    db.create_all()  # Crea las tablas si no existen
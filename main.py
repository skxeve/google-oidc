from views.top.index import top
from views.api.v1.index import api_v1
from flask_gcp_wand.appengine import (
    create_gae_flask_app,
    register_simple_error_handler,
)
import os


os.environ.setdefault("OAUTHLIB_RELAX_TOKEN_SCOPE", "true")

app = create_gae_flask_app(__name__)
register_simple_error_handler(app)
app.secret_key = "secret_key"
app.config["JSON_AS_ASCII"] = False
# app.config['IS_PRODUCTION'] = True
app.register_blueprint(top)
app.register_blueprint(api_v1, url_prefix="/api/v1")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

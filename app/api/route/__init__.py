from app.api.route import auth, health_check, user

routers = [health_check.router, user.router, auth.router]

from fastapi import FastAPI
from routers import organizations, buildings, activities
routers = []

def register_routers(app: FastAPI):
    routers.append(organizations.router)
    routers.append(buildings.router)
    routers.append(activities.router) 

    for router in routers:
        app.include_router(router)

__all__ = ["routers", "register_routers"] 

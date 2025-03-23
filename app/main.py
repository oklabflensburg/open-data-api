from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from sqlalchemy.ext.declarative import declarative_base

from .database import engine
from .utils.exceptions import CustomValidationError

from .api.biotope import route_biotope
from .api.climate import route_climate
from .api.accident import route_accident
from .api.monument import route_monument
from .api.archaeology import route_archaeology
from .api.administrative import route_administrative
from .api.demographic import route_demographic
from .api.energy import route_energy


app = FastAPI(docs_url=None, redoc_url=None, version='1.18', title='Opendata API',
              summary='Opendata API developed by volonteers from https://oklabflensburg.de')
Base = declarative_base()

app.mount('/static', StaticFiles(directory='static'), name='static')


@app.on_event('startup')
async def init_schemas():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.get('/', include_in_schema=False)
def home_redirect():
    return RedirectResponse('/docs')


@app.get('/docs', include_in_schema=False)
async def swagger_ui_html(req: Request) -> HTMLResponse:
    return get_swagger_ui_html(
        title=app.title,
        openapi_url='/openapi.json',
        swagger_favicon_url='/static/favicon.ico'
    )


@app.exception_handler(CustomValidationError)
async def custom_validation_error_handler(
    request: Request,
    exc: CustomValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={'error': exc.detail['msg']}
    )


app.include_router(route_biotope)
app.include_router(route_climate)
app.include_router(route_accident)
app.include_router(route_monument)
app.include_router(route_archaeology)
app.include_router(route_administrative)
app.include_router(route_demographic)
app.include_router(route_energy)

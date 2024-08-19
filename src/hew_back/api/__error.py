import traceback

from starlette.responses import JSONResponse

from hew_back import app, model
from hew_back.error import ErrorIdException


@app.exception_handler(ErrorIdException)
async def exception_handler(request, exc: ErrorIdException):
    return JSONResponse(
        content=exc.to_error_res().dict(),
        status_code=exc.error_id.value.status_code
    )


@app.exception_handler(Exception)
async def exception_handler(request, exc: Exception):
    print(traceback.format_exc())
    return JSONResponse(
        content=model.ErrorRes.create_by_exception(
            exc,
        ).dict(),
        status_code=model.ErrorIds.INTERNAL_ERROR.value.status_code
    )


@app.exception_handler(401)
async def exception_handler(request, exc: Exception):
    return JSONResponse(
        content=model.ErrorRes.create_by_exception(
            exc, error_ids=model.ErrorIds.UNAUTHORIZED
        ).dict(),
        status_code=model.ErrorIds.UNAUTHORIZED.value.status_code
    )

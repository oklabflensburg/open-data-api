from fastapi import Depends, FastAPI, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from typing import List

import base
import schemas
import service


app = FastAPI()
Base = declarative_base()
router = APIRouter(prefix='/sozialatlas/v1')


@app.on_event('startup')
async def init_schemas():
    async with base.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Dependency
async def get_session() -> AsyncSession:
    async with base.async_session() as session:
        yield session



@router.get('/districts', response_model=list[schemas.District])
async def get_all_districts(session: AsyncSession = Depends(get_session)):
    districts = await service.get_districts(session)

    return [schemas.District(district_id=d.id, district_name=d.name) for d in districts]


'''
@router.get('/household/types', response_model=list[schemas.])
@router.get('/residents/agegroups', response_model=list[schemas.])
@router.get('/residents/nongermans', response_model=list[schemas.])
@router.get('/residents/debtcounseling', response_model=list[schemas.])
@router.get('/residents/education/support', response_model=list[schemas.])
@router.get('/district/residents', response_model=list[schemas.])
@router.get('/district/residents/births', response_model=list[schemas.])
@router.get('/district/residents/employed', response_model=list[schemas.])
@router.get('/district/residents/ageratio', response_model=list[schemas.])
@router.get('/district/residents/basicbenefits', response_model=list[schemas.])
@router.get('/district/residents/age18tounder65', response_model=list[schemas.])
@router.get('/district/residents/ageunder18', response_model=list[schemas.])
@router.get('/district/residents/age65andabove', response_model=list[schemas.])
@router.get('/district/residents/agegroups', response_model=list[schemas.])
@router.get('/district/residents/unemployed', response_model=list[schemas.])
@router.get('/district/residents/unemployed/categorized', response_model=list[schemas.])
@router.get('/district/residents/beneficiaries', response_model=list[schemas.])
@router.get('/district/residents/beneficiaries/inactive', response_model=list[schemas.])
@router.get('/district/residents/beneficiaries/characteristics', response_model=list[schemas.])
@router.get('/district/residents/beneficiaries/age15tounder65', response_model=list[schemas.])
@router.get('/district/residents/migration/background', response_model=list[schemas.])
@router.get('/district/residents/housing/assistance', response_model=list[schemas.])
@router.get('/district/residents/housing/benefit', response_model=list[schemas.])
@router.get('/district/residents/risk/homelessness', response_model=list[schemas.])
'''

app.include_router(router)

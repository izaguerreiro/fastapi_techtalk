import requests
from pymongo import errors
from typing import Any, List, Optional

from fastapi import FastAPI, Path, Request, status, Query
from fastapi.responses import JSONResponse

from app import schemas
from bootstrap import mongodb


app = FastAPI()
mongodb.install(app)


class CepNotFoundException(Exception):
    pass


@app.exception_handler(CepNotFoundException)
async def cep_not_found_handler(request: Request, exc: CepNotFoundException):
    return JSONResponse(status_code=404, content={"message": "Cep não encontrado"})


async def save_address(address: dict):
    app.db.save(address)


@app.get("/address", response_model=List[schemas.AddressOutput], response_model_exclude_unset=True)
async def search_addresses(uf: Optional[str] = Query(None, max_length=2, min_length=2)):
    if uf:
        return list(app.db.find({"uf": uf}))

    return list(app.db.find({}))


@app.get("/address/{cep}", response_model=schemas.AddressOutput)
async def search_address_by_cep(cep: str = Path(default=Any, max_length=9, min_length=9)):
    address = app.db.find_one({"cep": cep})
    if not address:
        response = requests.get(f"http://viacep.com.br/ws/{cep}/json/")
        address = response.json()

        if "erro" in address:
            raise CepNotFoundException()

        await save_address(address)
    return address


@app.post("/address", response_model=schemas.AddressOutput, status_code=201) # também podemos importar o status e usar status.HTTP_201_CREATED
async def create_address(address: schemas.AddressInput): # Posso ter um schema diferente para entrada e outro para saída
    try:
        await save_address(address.dict()) # Mostrar que ele faz a conversão automática de str para int caso seja um número e falar para tomar cuidado pois pode dar erro caso seja um float
        return address # aqui também poderia usar o JSONResponse 
    except errors.DuplicateKeyError:
        return JSONResponse(status_code=409, content={"message": "Cep já existe"})


@app.put("/address/{cep}", status_code=status.HTTP_204_NO_CONTENT)
async def update_address(cep: str, address: schemas.AddressInput):
    old_address = app.db.find_one({"cep": cep})
    update_address = {"$set": address.dict()} # isso é uma particularidade do pymongo
    app.db.update_one(old_address, update_address)


@app.delete("/address/{cep}", responses={status.HTTP_204_NO_CONTENT: {}})
async def delete_address(cep: str):
    app.db.delete_many({"cep": cep})

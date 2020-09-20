from pydantic import BaseModel, Field
from typing import List, Optional


class AddressInput(BaseModel):
    cep: str
    logradouro: str
    complemento: Optional[str] = None
    bairro: str
    localidade: str
    uf: str
    ibge: int
    gia: int
    ddd: int


class AddressOutput(BaseModel):
    cep: str
    logradouro: str
    complemento: Optional[str] = None
    bairro: str
    localidade: str
    uf: str 
    other: List[str] = []

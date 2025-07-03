from typing import Any
import pytest
from assets_term_generator.models import User, Asset, Category, AssetModel
from assets_term_generator.util.exceptions import UserNotFoundError
from assets_term_generator.api import snipeit_client


def test_get_user_and_assets_success(mocker: Any) -> None:
    """
    Testa o fluxo de sucesso de get_user_and_assets.
    Verifica se, ao receber dados simulados da API, a função retorna os objetos corretos.
    """
    fake_user = User(id=492, name="Usuário de Teste", employee_num="12345", assets_count=1)
    fake_asset = Asset(
        id=366, 
        name="Notebook de Teste", 
        asset_tag="TEST-001",
        serial="TESTSERIAL123",
        notes="Nota de teste",
        custom_fields={},
        model=AssetModel(id=1, name="Modelo Teste"),
        category=Category(id=1, name="Laptops"),
        components=[],
        accessories=[]
    )

    mocker.patch('assets_term_generator.api.snipeit_client.users_client.find_by_employee_number', return_value=fake_user)
    mocker.patch('assets_term_generator.api.snipeit_client.users_client.get_assets', return_value=[fake_asset])
    


    user, assets = snipeit_client.get_user_and_assets("12345")

    assert user is not None
    assert user.name == "Usuário de Teste"
    assert len(assets) == 1
    assert assets[0].asset_tag == "TEST-001"


def test_get_user_and_assets_user_not_found(mocker: Any) -> None:
    """
    Testa se UserNotFoundError é lançado quando a API não retorna um usuário.
    """
    mocker.patch('assets_term_generator.api.snipeit_client.users_client.find_by_employee_number', return_value=None)

    with pytest.raises(UserNotFoundError) as excinfo:
        snipeit_client.get_user_and_assets("id_invalido")

    assert "não encontrado" in str(excinfo.value)

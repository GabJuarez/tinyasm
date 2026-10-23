"""Pruebas que deben pasar desde el día uno: el paquete importa y las tablas son coherentes."""

from tinyasm import isa


def test_register_table_has_subregisters():
    assert isa.REGISTERS["ah"] == isa.RegisterInfo("eax", 8, 8)
    assert isa.REGISTERS["sp"] == isa.RegisterInfo("esp", 16)
    assert isa.is_register("EAX")
    assert not isa.is_register("loop_start")

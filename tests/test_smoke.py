"""Pruebas que deben pasar desde el día uno: el paquete importa y las tablas son coherentes."""

from tinyasm import isa


def test_is_register():
    assert isa.is_register("EAX")
    assert isa.is_register("ebp")
    assert not isa.is_register("ax")
    assert not isa.is_register("loop_start")

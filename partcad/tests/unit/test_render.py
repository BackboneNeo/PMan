#!/usr/bin/env python3
#
# OpenVMP, 2024
#
# Author: Roman Kuzmenko
# Created: 2024-01-06
#
# Licensed under Apache License, Version 2.0.
#

import platform
import pytest
import tempfile

import build123d as b3d

import partcad as pc
from partcad.wrappers import wrapper_render_svg


def test_render_wrapper_preserves_compound_topology():
    """Assembly compounds must not be mislabeled as solids before projection."""
    compound = b3d.Compound(
        children=[
            b3d.Box(1, 1, 1),
            b3d.Pos(2, 0, 0) * b3d.Box(1, 1, 1),
        ]
    )

    wrapped = wrapper_render_svg._wrap_render_shape(compound.wrapped)

    assert isinstance(wrapped, b3d.Compound)
    assert not isinstance(wrapped, b3d.Solid)

    visible, hidden = wrapper_render_svg._project_render_shape(
        wrapped,
        viewport_origin=(5, -5, 5),
        viewport_up=(0, 0, 1),
    )
    assert visible
    assert isinstance(hidden, list)


@pytest.mark.slow
def test_render_svg_part_1():
    """Render a primitive shape to SVG"""
    ctx = pc.init("examples")
    prj = ctx.get_project("//produce_part_cadquery_primitive")
    cube = prj.get_part("cube")
    assert cube is not None
    try:
        # cube.render_svg(ctx, project=prj)
        cube.render(ctx, "svg", prj)
    except Exception as e:
        assert False, "Valid render request caused an exception: %s" % e


@pytest.mark.slow
def test_render_svg_assy_1():
    """Render a primitive shape to SVG"""
    ctx = pc.init("examples")
    prj = ctx.get_project("//produce_assembly_assy")
    assy = prj.get_assembly("logo")
    assert assy is not None
    try:
        # assy.render_svg(ctx, project=prj)
        assy.render(ctx, "svg", prj)
    except Exception as e:
        assert False, "Valid render request caused an exception: %s" % e


@pytest.mark.slow
def test_render_svg_assy_2():
    """Render a primitive shape to SVG"""
    ctx = pc.init("examples")
    prj = ctx.get_project("//produce_assembly_assy")
    assy = prj.get_assembly("logo_embedded")
    assert assy is not None
    try:
        # assy.render_svg(ctx, project=prj)
        assy.render(ctx, "svg", prj)
    except Exception as e:
        assert False, "Valid render request caused an exception: %s" % e


@pytest.mark.slow
def test_render_project():
    """Render an entire project"""
    if platform.system() == "Windows":
        pytest.skip("Rendering to PNG is not supported in Windows CI due to Cairo")
    ctx = pc.init("examples")
    prj = ctx.get_project("//feature_export")
    assert prj is not None
    output_dir = tempfile.mkdtemp()
    prj.render(output_dir=output_dir)

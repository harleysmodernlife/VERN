import pytest
from src.mvp.writing import writing_respond
from src.mvp.presentation import presentation_respond
from src.mvp.insight import insight_respond

def test_writing_workflow_basic():
    result = writing_respond("Write a summary.", persona="summarizer", memory="Session1")
    assert "[draft]" in result and "[edit]" in result and "[review]" in result

def test_writing_workflow_custom_steps():
    steps = ["draft", "polish"]
    result = writing_respond("Improve grammar.", workflow_steps=steps, persona="editor", memory="Session2")
    assert "[draft]" in result and "[polish]" in result

def test_presentation_workflow_basic():
    result = presentation_respond("Create slides.", persona="designer", memory="SessionA")
    assert "[outline]" in result and "[design]" in result and "[review]" in result

def test_presentation_workflow_custom_steps():
    steps = ["outline", "finalize"]
    result = presentation_respond("Finalize deck.", workflow_steps=steps, persona="storyteller", memory="SessionB")
    assert "[outline]" in result and "[finalize]" in result

def test_insight_workflow_basic():
    result = insight_respond("Analyze trends.", persona="analyst", memory="SessionX")
    assert "[gather]" in result and "[synthesize]" in result and "[recommend]" in result

def test_insight_workflow_custom_steps():
    steps = ["gather", "report"]
    result = insight_respond("Report findings.", workflow_steps=steps, persona="advisor", memory="SessionY")
    assert "[gather]" in result and "[report]" in result

def test_error_handling_writing():
    # Simulate error by passing an invalid type for workflow_steps
    result = writing_respond("Test error.", workflow_steps="not_a_list")
    assert "Error:" in result or "[draft]" in result

def test_error_handling_presentation():
    result = presentation_respond("Test error.", workflow_steps="not_a_list")
    assert "Error:" in result or "[outline]" in result

def test_error_handling_insight():
    result = insight_respond("Test error.", workflow_steps="not_a_list")
    assert "Error:" in result or "[gather]" in result
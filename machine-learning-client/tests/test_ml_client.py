"""This python file tests the machine-learning-client using pytest"""

import pandas as pd
from ml_client import MLC


def test_get_recommendation():
    """Testing get recommendation in expected scenario"""
    example_df = pd.DataFrame(
        [
            {"title": "Example Movie 1", "description": "Description 1"},
            {"title": "Batman v. Superman", "description": "Batman fights Superman"},
            {
                "title": "The Spongebob Movie",
                "description": "Patrick Star and Spongebob Squarepants go on a playdate",
            },
        ]
    )
    mlc = MLC(example_df["description"])
    result = mlc.get_recommendation("Spongebob annoys Squidward", example_df)
    assert result.iloc[0]["title"] == "The Spongebob Movie"


def test_get_recommendation_no_match():
    """Testing get recommendation in scenario with no match"""
    example_df = pd.DataFrame(
        [
            {"title": "Example Movie 1", "description": "Description 1"},
            {"title": "Batman v. Superman", "description": "Batman fights Superman"},
            {
                "title": "The Spongebob Movie",
                "description": "Patrick Star and Spongebob Squarepants go on a playdate",
            },
        ]
    )
    mlc = MLC(example_df["description"])
    result = mlc.get_recommendation("Wreck-it-Ralph wrecks stuff", example_df)
    assert result == "No match found"


def test_lemmatization():
    """Testing lemmetization"""
    example_input = "dogs"
    example_df = pd.DataFrame(
        [
            {"title": "Example Movie 1", "description": "Description 1"},
            {"title": "Batman v. Superman", "description": "Batman fights Superman"},
            {
                "title": "The Spongebob Movie",
                "description": "Patrick Star and Spongebob Squarepants go on a playdate",
            },
        ]
    )
    mlc = MLC(example_df["description"])
    example_output = mlc.lemmatize_text(example_input)
    assert example_output == "dog"

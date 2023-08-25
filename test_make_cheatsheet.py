import pytest
import make_cheatsheet

text = "A programmer was crossing a road one day when a frog called out to him or us and said, 'If you kiss me, I'll turn into a beautiful princess.'"
levels = ["a1", "a2", "b1", "b2", "c1"]


@pytest.fixture
def removed_punctuation_and_unknown():
    return make_cheatsheet.remove_punctuation_and_unknown(text)


def test_remove_punctuation_and_unknown(removed_punctuation_and_unknown):
    assert (
        removed_punctuation_and_unknown
        == "A programmer was crossing a road one day when a frog called out to him or us and said If you kiss me Ill turn into a beautiful princess"
    )


@pytest.fixture
def lemmatized_text(removed_punctuation_and_unknown):
    return make_cheatsheet.lemmatize_text(removed_punctuation_and_unknown)


def test_lemmatize_text(lemmatized_text):
    assert (
        lemmatized_text
        == "a programmer be cross a road one day when a frog call out to he or we and say if you kiss I Ill turn into a beautiful princess"
    )


@pytest.fixture
def analysis(lemmatized_text):
    return make_cheatsheet.analyze_CEFR(lemmatized_text, levels)


def test_analyze_CEFR(analysis):
    analysis == {
        "stats": {
            "a1": "75.9%",
            "a2": "6.9%",
            "b1": "6.9%",
            "b2": "0.0%",
            "c1": "0.0%",
            "misc": "20.7%",
        },
        "words": {
            "a1": {
                "or",
                "you",
                "be",
                "road",
                "out",
                "to",
                "when",
                "call",
                "turn",
                "we",
                "day",
                "if",
                "a",
                "one",
                "say",
                "beautiful",
                "into",
                "and",
                "he",
            },
            "a2": {"frog", "cross"},
            "b1": {"princess", "kiss"},
            "b2": set(),
            "c1": set(),
            "misc": ["Ill", "programmer", "I"],
        },
    }


def test_analysis_into_str(analysis):
    assert (
        make_cheatsheet.analysis_into_str(analysis, levels)
        == """a1 --- 75.9%
a2 --- 6.9%
b1 --- 6.9%
b2 --- 0.0%
c1 --- 0.0%
misc --- 20.7%
------------------------
A1
------------------------
a
and
be
beautiful
call
day
he
if
into
one
or
out
road
say
to
turn
we
when
you
------------------------
A2
------------------------
cross
frog
------------------------
B1
------------------------
kiss
princess
------------------------
B2
------------------------

------------------------
C1
------------------------

------------------------
MISC
------------------------
I
Ill
programmer
"""
    )


if __name__ == "__main__":
    new_text = make_cheatsheet.lemmatize_text(
        make_cheatsheet.remove_punctuation_and_unknown(text)
    )
    print(new_text)
    print(make_cheatsheet.analyze_CEFR(new_text, levels))
    print(
        make_cheatsheet.analysis_into_str(
            make_cheatsheet.analyze_CEFR(new_text, levels), levels
        )
    )

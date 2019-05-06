import markdown, pytest
from ocxmd import OCXMetadata

TESTINPUT = """---
"@id": "#lesson1"
name: "Test Lesson 1"
"@type":
    - oer:Lesson
    - CreativeWork
learningResourceType: LessonPlan
hasPart: {
  "@id": "#activity1"
}
author:
    "@type": Person
    name: Fred Blogs
---
#YAML to JSON-LD test
I started with some YAML and turned it into JSON-LD

Here is some more YAML

---
"@id": "#activity1"
"@type":
    - oer:Activity
    - CreativeWork
name: "Test Activity 1.1"
learningResourceType: Activity
---
"""
HTMLEXPECTED = """<script type="application/ld+json">{"@context": ["http://schema.org", {"oer": "http://oerschema.org/"}, {"ocx": "https://github.com/K12OCX/k12ocx-specs/"}], "@id": "#lesson1", "name": "Test Lesson 1", "@type": ["oer:Lesson", "CreativeWork"], "learningResourceType": "LessonPlan", "hasPart": {"@id": "#activity1"}, "author": {"@type": "Person", "name": "Fred Blogs"}}</script>

<h1>YAML to JSON-LD test</h1>
<p>I started with some YAML and turned it into JSON-LD</p>
<p>Here is some more YAML</p>
<script type="application/ld+json">{"@context": ["http://schema.org", {"oer": "http://oerschema.org/"}, {"ocx": "https://github.com/K12OCX/k12ocx-specs/"}], "@id": "#activity1", "@type": ["oer:Activity", "CreativeWork"], "name": "Test Activity 1.1", "learningResourceType": "Activity"}</script>"""

HTMLEXPECTED_DEFCONT = """<script type="application/ld+json">{"@context": "http://schema.org", "@id": "#lesson1", "name": "Test Lesson 1", "@type": ["oer:Lesson", "CreativeWork"], "learningResourceType": "LessonPlan", "hasPart": {"@id": "#activity1"}, "author": {"@type": "Person", "name": "Fred Blogs"}}</script>

<h1>YAML to JSON-LD test</h1>
<p>I started with some YAML and turned it into JSON-LD</p>
<p>Here is some more YAML</p>
<script type="application/ld+json">{"@context": "http://schema.org", "@id": "#activity1", "@type": ["oer:Activity", "CreativeWork"], "name": "Test Activity 1.1", "learningResourceType": "Activity"}</script>"""


METADATAEXPECTED_DEFCONT = {
    1: {
        "@context": "http://schema.org",
        "@id": "#lesson1",
        "name": "Test Lesson 1",
        "@type": ["oer:Lesson", "CreativeWork"],
        "learningResourceType": "LessonPlan",
        "hasPart": {"@id": "#activity1"},
        "author": {"@type": "Person", "name": "Fred Blogs"},
    },
    2: {
        "@context": "http://schema.org",
        "@id": "#activity1",
        "@type": ["oer:Activity", "CreativeWork"],
        "name": "Test Activity 1.1",
        "learningResourceType": "Activity",
    },
}

METADATAEXPECTED = {
    1: {
        "@context": [
            "http://schema.org",
            {"oer": "http://oerschema.org/"},
            {"ocx": "https://github.com/K12OCX/k12ocx-specs/"},
        ],
        "@id": "#lesson1",
        "name": "Test Lesson 1",
        "@type": ["oer:Lesson", "CreativeWork"],
        "learningResourceType": "LessonPlan",
        "hasPart": {"@id": "#activity1"},
        "author": {"@type": "Person", "name": "Fred Blogs"},
    },
    2: {
        "@context": [
            "http://schema.org",
            {"oer": "http://oerschema.org/"},
            {"ocx": "https://github.com/K12OCX/k12ocx-specs/"},
        ],
        "@id": "#activity1",
        "@type": ["oer:Activity", "CreativeWork"],
        "name": "Test Activity 1.1",
        "learningResourceType": "Activity",
    },
}


YAML_CONTEXT = """
"@context":
    - "http://schema.org"
    - "oer": "http://oerschema.org/"
    - "ocx": "https://github.com/K12OCX/k12ocx-specs/"
"""


def test1():
    md = markdown.Markdown(extensions=["ocxmd"])
    html = md.convert(TESTINPUT)
    assert md.meta == METADATAEXPECTED_DEFCONT
    assert html == HTMLEXPECTED_DEFCONT


def test2():
    md = markdown.Markdown(
        extensions=["ocxmd"],
        extension_configs={"ocxmd": {"context": "'@context' : 'http://schema.org'"}},
    )
    html = md.convert(TESTINPUT)
    assert md.meta == METADATAEXPECTED_DEFCONT
    assert html == HTMLEXPECTED_DEFCONT


def test3():
    md = markdown.Markdown(
        extensions=["ocxmd"], extension_configs={"ocxmd": {"context": YAML_CONTEXT}}
    )
    html = md.convert(TESTINPUT)
    assert md.meta == METADATAEXPECTED
    assert html == HTMLEXPECTED

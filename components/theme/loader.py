themes = {}


def get_theme(section, rule):
    if section not in themes:
        themes[section] = {}
    if rule not in themes[section]:
        themes[section][rule] = getattr(
            getattr(__import__(f"components.theme.{section}").theme, section), rule
        )()
    return themes[section][rule]

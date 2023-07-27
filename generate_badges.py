from __future__ import annotations

import anybadge

# https://stackoverflow.com/questions/43126475/pylint-badge-in-gitlab
# https://github.com/jongracecox/anybadge
# https://git.gesis.org/help/user/project/badges

python_version_badge = anybadge.Badge("python_version", value="3.11.3", default_color="darkgreen")
python_version_badge.write_badge("badges/python_version.svg")
pre_commit_version_badge = anybadge.Badge("pre_commit_version", value="3.3.2", default_color="darkgreen")
pre_commit_version_badge.write_badge("badges/pre_commit_version.svg")
poetry_version_badge = anybadge.Badge("poetry_version", value="1.5.1", default_color="darkgreen")
poetry_version_badge.write_badge("badges/poetry_version.svg")
python_runner_image_badge = anybadge.Badge("python_runner_image", value="1.0", default_color="darkgreen")
python_runner_image_badge.write_badge("badges/python_runner_image.svg")

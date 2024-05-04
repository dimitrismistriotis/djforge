"""Template tags for the dj_emails app."""
import base64
from pathlib import Path

from django import template

_LOGO_FOR_EMAILS_LOCATION = (
    Path(__file__).parent.parent
    / "react_email"
    / "emails"
    / "static"
    / "logo_for_email.png"
).as_posix()


register = template.Library()


@register.simple_tag
def logo_base64_png() -> str:
    """Return the base64 encoded logo image."""
    try:
        with open(_LOGO_FOR_EMAILS_LOCATION, "rb") as png_file:
            png_data = png_file.read()
            base64_encoded_data = base64.b64encode(png_data)
            base64_string = base64_encoded_data.decode("utf-8")
            return f"data:image/png;base64,{base64_string}"
    except FileNotFoundError:
        print(f"Error: File '{_LOGO_FOR_EMAILS_LOCATION}' not found.")
    except Exception as e:
        print(f"Error: {str(e)}")

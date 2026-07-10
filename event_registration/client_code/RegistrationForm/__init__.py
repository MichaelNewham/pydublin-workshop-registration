from _anvil_designer.common import BaseForm
import anvil.server


class RegistrationForm(BaseForm):
    """Registration form (Requirement: 'registration form for attendees').

    Collects name + email + phone + company + notes, then POSTs to the
    server via create_registration(). Email is the natural unique key.
    """

    def __init__(self, event=None, **properties):
        super().__init__(**properties)
        self.event = event or anvil.server.call("get_event")
        self.event_title.text = self.event["title"]

    def submit_button_click(self, **event_args):
        """Validate + save. Server raises ValueError with human-readable msg."""
        try:
            row = anvil.server.call(
                "create_registration",
                name=self.name_box.text,
                email=self.email_box.text,
                phone=self.phone_box.text,
                company=self.company_box.text,
                notes=self.notes_box.text,
                event=self.event,
            )
            alert(
                f"Thanks {self.name_box.text}! "
                f"Your registration ref is PYDUB-2026-{row.get_id()[:8]}."
            )
            from ..Home import HomeForm
            open_form(HomeForm)
        except ValueError as err:
            alert(str(err), title="Could not register")

    def back_button_click(self, **event_args):
        from ..Home import HomeForm
        open_form(HomeForm)

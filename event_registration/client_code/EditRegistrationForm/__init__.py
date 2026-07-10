from _anvil_designer.common import BaseForm
import anvil.server


class EditRegistrationForm(BaseForm):
    """Edit an existing registration.

    Requirements 'edit ... existing registrations'. The corresponding
    'cancel' lives on the Detail form.
    """

    def __init__(self, reg_id, event=None, **properties):
        super().__init__(**properties)
        self.reg_id = reg_id
        self.event = event or anvil.server.call("get_event")
        self.row = anvil.server.call("get_registration", reg_id)
        self._prefill()

    def _prefill(self):
        r = self.row
        if r is None:
            self.heading.text = "Not found"
            return
        self.heading.text = f"Edit - {r['name']}"
        self.name_box.text = r["name"]
        self.email_box.text = r["email"]
        self.phone_box.text = r["phone"]
        self.company_box.text = r["company"]
        self.notes_box.text = r["notes"]

    def save_button_click(self, **event_args):
        try:
            anvil.server.call(
                "update_registration",
                self.reg_id,
                name=self.name_box.text,
                email=self.email_box.text,
                phone=self.phone_box.text,
                company=self.company_box.text,
                notes=self.notes_box.text,
            )
            alert("Saved.")
            from ..RegistrationDetailForm import RegistrationDetailForm
            open_form(RegistrationDetailForm, reg_id=self.reg_id, event=self.event)
        except ValueError as err:
            alert(str(err), title="Could not save")

    def cancel_edit_button_click(self, **event_args):
        from ..RegistrationDetailForm import RegistrationDetailForm
        open_form(RegistrationDetailForm, reg_id=self.reg_id, event=self.event)

from _anvil_designer.common import BaseForm
import anvil.server


class RegistrationDetailForm(BaseForm):
    """Detail page for a single registration.

    Requirement: 'a detail page for each individual registration'.
    Offer buttons to either edit or cancel the row.
    """

    def __init__(self, reg_id, event=None, **properties):
        super().__init__(**properties)
        self.event = event or anvil.server.call("get_event")
        self.reg_id = reg_id
        self.row = anvil.server.call("get_registration", reg_id)
        self._render()

    def _render(self):
        r = self.row
        if r is None:
            self.heading.text = "Registration not found"
            return
        self.heading.text = f"{r['name']} - {r['email']}"
        self.phone_value.text = r["phone"] or "-"
        self.company_value.text = r["company"] or "-"
        self.status_value.text = r["status"].title()
        self.created_value.text = (r["created_at"] or "").strftime(
            "%d %b %Y, %H:%M"
        )
        self.notes_value.text = r["notes"] or "(no notes)"
        # A cancelled registration can be restored; an active one can be cancelled.
        is_cancelled = (r["status"] == "cancelled")
        self.cancel_button.visible = not is_cancelled
        self.restore_button.visible = is_cancelled
        self.edit_button.visible = not is_cancelled
        self.edit_button.enabled = not is_cancelled
        # Update the event hyperlink to take us home
        self.back_button.text = "Back to list"

    def edit_button_click(self, **event_args):
        from ..EditRegistrationForm import EditRegistrationForm
        open_form(EditRegistrationForm, reg_id=self.reg_id, event=self.event)

    def cancel_button_click(self, **event_args):
        if confirm("Cancel this registration? This cannot be undone from the UI."):
            anvil.server.call("cancel_registration", self.reg_id)
            self._render()
            alert("Registration cancelled.")

    def restore_button_click(self, **event_args):
        anvil.server.call("restore_registration", self.reg_id)
        self._render()
        alert("Registration restored.")

    def back_button_click(self, **event_args):
        from ..ParticipantsListForm import ParticipantsListForm
        open_form(ParticipantsListForm, event=self.event)

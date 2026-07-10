from _anvil_designer.common import BaseForm
import anvil.server
import anvil.js


class HomeForm(BaseForm):
    """Landing / Event information page (Requirement: 'event information page').

    Loads the demo event from the server, displays its details, and routes
    to the Registration or Participants forms via button clicks.
    """

    def __init__(self, **properties):
        super().__init__(**properties)
        self.event = anvil.server.call("get_or_create_demo_event")
        self._render_event()

    def _render_event(self):
        ev = self.event
        if ev is None:
            return
        self.title_label.text = ev["title"] or "Untitled event"
        self.date_label.text = (ev["date"] or "").strftime(
            "%A %d %B %Y, %H:%M"
        ) if ev["date"] else "Date TBC"
        self.location_label.text = ev["location"] or "Location TBC"
        self.description_label.text = ev["description"] or ""
        self.price_label.text = (
            f"EUR {ev['price']:.2f}" if ev["price"] else "Free"
        )
        seats_taken = anvil.server.call("count_registrations", ev)
        seats_left = (ev["capacity"] or 0) - seats_taken
        self.capacity_label.text = (
            f"Seats remaining: {seats_left} / {ev['capacity']}"
        )
        # Disable the Register button when sold out - good UX
        self.register_button.enabled = seats_left > 0

    # ---- button handlers (wired in form_template.yaml) ----
    def register_button_click(self, **event_args):
        # Open the registration Form, passing the event row
        from ..RegistrationForm import RegistrationForm
        open_form(RegistrationForm, event=self.event)

    def view_participants_button_click(self, **event_args):
        from ..ParticipantsListForm import ParticipantsListForm
        open_form(ParticipantsListForm, event=self.event)

    def copy_ref_button_click(self, **event_args):
        """The required JavaScript interaction (see anvil.yaml native_deps).

        Asks the browser (via anvil.js) to copy a short event ref to the
        clipboard, then confirms back to the user.
        """
        ref = f"PYDUB-2026-{self.event.get_id()[:8]}"
        try:
            anvil.js.call_js("copyRefToClipboard", ref)
            alert(f"Copied to clipboard: {ref}")
        except Exception:
            alert("Clipboard not available in this browser. Ref: " + ref)

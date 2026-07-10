from _anvil_designer.common import BaseForm
import anvil.server


class ParticipantsListForm(BaseForm):
    """List of participants for organisers.

    Requirement: 'a list of registered participants'.
    """

    def __init__(self, event=None, **properties):
        super().__init__(**properties)
        self.event = event or anvil.server.call("get_event")
        self.title_label.text = f"Participants - {self.event['title']}"
        self._refresh_list()

    def _refresh_list(self):
        rows = anvil.server.call("list_registrations", event=self.event)
        self.count_label.text = f"{len(rows)} registered"
        # Wrap each row in the item template defined below
        self.repeating_panel.items = [
            {"row": r, "on_view": self._view_row} for r in rows
        ]

    def _view_row(self, row):
        from ..RegistrationDetailForm import RegistrationDetailForm
        open_form(RegistrationDetailForm, reg_id=row.get_id(), event=self.event)

    def refresh_button_click(self, **event_args):
        self._refresh_list()

    def back_button_click(self, **event_args):
        from ..Home import HomeForm
        open_form(HomeForm)


class ParticipantItem(BaseForm):
    """One row in the RepeatingPanel. Bound via `item`."""

    def __init__(self, **properties):
        super().__init__(**properties)
        row = self.item.get("row") if self.item else None
        on_view = self.item.get("on_view") if self.item else None
        self._on_view = on_view
        if row:
            self.name_label.text = row["name"]
            self.email_label.text = row["email"]
            self.company_label.text = row["company"] or "-"
            self.date_label.text = (row["created_at"] or "").strftime("%d %b %H:%M")

    def view_link_click(self, **event_args):
        # Hand control back up to the parent Form to navigate
        if self._on_view and self.item.get("row"):
            self._on_view(self.item["row"])

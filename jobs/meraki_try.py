import os

from nautobot.extras.jobs import ChoiceVar, Job, StringVar
import meraki

class TryThings(Job):
    """Class to create a Meraki user

    Args:
        Job (Nautobot Job): Meraki create user job
    """

    user_email = StringVar(
        description="User Email to add", label="User Email", required=True
    )

    user_name = StringVar(
        description="User full name to add", label="User Full Name", required=True
    )

    meraki_org_id = ChoiceVar(
        description="Meraki Org ID",
        label="Meraki Organization ID",
        choices=MERAKI_ORG_CHOICES,
        required=False,
    )

    meraki_network = StringVar(
        description="Network Name to Add", label="Network Name", required=True
    )

    meraki_access_level = ChoiceVar(
        description="Level of access",
        label="Access Level",
        choices=(
            ("Full", "full"),
            ("Read Only", "read-only"),
            ("Enterprise", "enterprise"),
            ("None", "none"),
        ),
    )

    class Meta:
        """Metaclass attrs."""

        name = "Create Meraki User"
        descripton = "Create Meraki User account"

    def __init__(self):
        super().__init__()
        self.data = None
        self.commit = None

    def run(self, data, commit):
        """Run execution

        Args:
            data (dict): Data from the form
            commit (bool): Commit changes to the database
        """
        self.data = data
        self.commit = commit

        self.log_success(object=None, message="You Rock")
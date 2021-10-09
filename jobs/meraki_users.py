import os

from nautobot.extras.jobs import ChoiceVar, Job, StringVar
import meraki


def get_meraki_org_ids_for_form():
    """Get the organizational IDs for Meraki and return in a tuple for populating the Django form."""
    # Test to see if Meraki API key is set in the environment
    try:
        try:
            api_key = os.environ["MERAKI_DASHBOARD_API_KEY"]
        except:
            raise ValueError(
                "Meraki API Key is not specified in the environment. Please set MERAKI_DASHBOARD_API_KEY"
            )

        dashboard = meraki.DashboardAPI(suppress_logging=True)
        # Get the organization list
        orgs = dashboard.organizations.getOrganizations()
        org_list = []
        for org in orgs:
            org_list.append((org["id"], org["name"]))

        return tuple(org_list)
    except:  # noqa: E722
        return None


MERAKI_ORG_CHOICES = get_meraki_org_ids_for_form()


class CreateUsers(Job):
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

        # Verify that an API Key is set
        try:
            api_key = os.environ["MERAKI_DASHBOARD_API_KEY"]
        except:
            raise ValueError(
                "Meraki API Key is not specified in the environment. Please set MERAKI_DASHBOARD_API_KEY"
            )

        # Get a dashboard object to work from
        dashboard = meraki.DashboardAPI(suppress_logging=True, api_key=api_key)

        # Get the list of existing users
        existing_users = dashboard.organizations.getOrganizationAdmins(
            organizationId=self.data["meraki_org_id"]
        )

        # Determine if the new user is in the existing user list
        for user_info in existing_users:
            if self.data["user_email"] in user_info.get("email"):
                self.log_info(
                    object=None,
                    message=f"{self.data['user_email']} already exists in the organization.",
                )
                # Return the function as this is all that is needed
                return

        # The user does not exist, create the user account
        dashboard.organizations.createOrganizationAdmin(
            organizationId=self.data["meraki_org_id"],
            name=self.data["user_name"],
            email=self.data["user_email"],
            orgAccess=self.data["meraki_access_level"],
        )

        self.log_success(
            object=None,
            message=f"Successfully created account for email {self.data['user_email']}",
        )

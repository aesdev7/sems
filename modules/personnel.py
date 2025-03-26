class Personnel:
    def __init__(
        self,
        first_name: str,
        middle_name: str,
        last_name: str,
        svid: str,               # 8-digit payroll number (e.g., "11010354")
        svemail: str,            # Must be @saudiairlines.com
        seniority_date: str,     # Format: YYYY-MM-DD
        work_location: str,      "SecManagement" (HQ) or "Operations" (Airport)
        manager: str,            # Manager name (validated based on location)
    ):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.svid = self._validate_svid(svid)
        self.svemail = self._validate_email(svemail)
        self.seniority_date = seniority_date
        self.work_location = self._validate_location(work_location)
        self.manager = self._validate_manager(manager, work_location)

    def _validate_svid(self, svid: str) -> str:
        """Ensure SVID is an 8-digit number (e.g., '11010354')."""
        if not (svid.isdigit() and len(svid) == 8):
            raise ValueError("SVID must be an 8-digit number (e.g., '11010354')")
        return svid

    def _validate_email(self, email: str) -> str:
        """Ensure email ends with @saudiairlines.com."""
        if not email.endswith("@saudiairlines.com"):
            raise ValueError("Email must be a valid @saudiairlines.com address")
        return email

    def _validate_location(self, location: str) -> str:
        """Validate work location: SecManagement (HQ) or Operations (Airport)."""
        valid_locations = {"SecManagement", "Operations"}
        if location not in valid_locations:
            raise ValueError("Work location must be 'SecManagement' (HQ) or 'Operations' (Airport)")
        return location

    def _validate_manager(self, manager: str, location: str) -> str:
        """
        Validate manager name based on location:
        - SecManagement (HQ): Manager must be in HQ leadership.
        - Operations (Airport): Manager must be in Airport leadership.
        """
        if location == "SecManagement" and not manager.endswith("(HQ)"):
            raise ValueError("HQ managers must have '(HQ)' in their title")
        elif location == "Operations" and not manager.endswith("(Airport)"):
            raise ValueError("Airport managers must have '(Airport)' in their title")
        return manager

    def display_info(self):
        """Prints personnel details in a structured format."""
        print(f"Name: {self.first_name} {self.middle_name} {self.last_name}")
        print(f"SVID (Payroll Number): {self.svid}")
        print(f"Email: {self.svemail}")
        print(f"Seniority Date: {self.seniority_date}")
        print(f"Work Location: {self.work_location}")
        print(f"Manager: {self.manager}")

# Example Usage
if __name__ == "__main__":
    # HQ Employee Example
    hq_employee = Personnel(
        first_name="Fatima",
        middle_name="Abdullah",
        last_name="Al-Sudairi",
        svid="11010355",
        svemail="fatima.alsudairi@saudiairlines.com",
        seniority_date="2019-03-10",
        work_location="SecManagement",
        manager="Director of Finance (HQ)",  # HQ managers must include "(HQ)"
    )

    # Airport Employee Example
    airport_employee = Personnel(
        first_name="Khalid",
        middle_name="Nasir",
        last_name="Al-Harbi",
        svid="22020356",
        svemail="khalid.alharbi@saudiairlines.com",
        seniority_date="2021-07-22",
        work_location="Operations",
        manager="Chief Ground Ops (Airport)",  # Airport managers must include "(Airport)"
    )

    print("\n--- HQ Employee ---")
    hq_employee.display_info()

    print("\n--- Airport Employee ---")
    airport_employee.display_info()

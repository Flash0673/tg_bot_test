import gspread


class Sheets():
    def __init__(self):
        self.sa = gspread.service_account(filename="service_account.json")
        self.sheet = self.sa.open("Bot DB")
        self.work_sheet = self.sheet.worksheet("info")

    def send_main_materials(self):
        materials =  self.work_sheet.col_values(1)[1:]
        return "\n".join(materials)

    def send_additional_materials(self):
        materials = self.work_sheet.col_values(2)[1:]
        return "\n\n".join(materials)


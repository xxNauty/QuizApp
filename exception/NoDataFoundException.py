class NoDataFoundError(Exception):
    def __init__(self, table_name: str) -> None:
        self.message: str = f"No data found in the {table_name} table"
        self.table_name: str = table_name

        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message
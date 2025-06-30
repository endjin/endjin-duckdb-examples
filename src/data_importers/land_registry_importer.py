import requests
from typing import List
from pathlib import Path
import arrow


import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LandRegistryImporter:
    """
    LandRegistryImporter is a class designed to facilitate the easy loading of house price data 
    from The UK Government's Land Registry department. The data files are hosted on the cloud 
    and can be downloaded via HTTP.
    The dataset contains property price data from 1995 onwards. However, the complete dataset 
    (from 1995 to the present day) is approximately 5 Gigabytes in size. To make the process 
    more manageable, this class defaults to loading data for only three years (2010, 2011, and 2012). 
    Users can customize the range of years they wish to process by providing a list of years 
    to the constructor.
    The data is downloaded as CSV files and stored in a local folder. The class ensures that 
    the specified folder exists and validates the years provided by the user to ensure they 
    fall within the valid range (1995 to the current year).
    For more information about the dataset, visit the official webpage:
    https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads
    """
    
    
    BASE_URL = "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/"
    MONTHLY_UPDATE_FILE_NAME = "pp-monthly-update-new-version.csv"
    
    DATA_FOLDER = Path("../data/land_registry")
    
    MIN_YEAR = 1995
    MAX_YEAR = arrow.now().year
    
    def __init__(self, years_to_import: List[int] = [2010, 2011, 2012]) -> None:
        self.years_to_import = years_to_import
        self._check_years_are_valid()
        self._create_folder_if_not_exists()

    def import_yearly_data(self) -> None:
        for year in self.years_to_import:
            self._get_yearly_file(year)

    def import_monthly_update(self) -> None:
        file_path = self.DATA_FOLDER / self.MONTHLY_UPDATE_FILE_NAME
        url = self._build_file_url(self.MONTHLY_UPDATE_FILE_NAME)
        self._download_file(self.MONTHLY_UPDATE_FILE_NAME, file_path, url)

    def _create_folder_if_not_exists(self):
        self.DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    def _create_yearly_file_name(self, year: int) -> str:
        return f"pp-{year}.csv"

    def _build_file_url(self, file_name) -> str:
        return f"{self.BASE_URL}{file_name}"

    def _get_yearly_file(self, year: int) -> None:
        file_name = self._create_yearly_file_name(year)
        file_path = self.DATA_FOLDER / file_name
        if file_path.exists():
            logger.info(f"File {file_name} already exists")
            return
        url = self._build_file_url(file_name)
        self._download_file(file_name, file_path, url)

    def _download_file(self, file_name, file_path, url):
        logger.info(f"Downloading file {file_name} from {url}")
        response = requests.get(url)
        with open(file_path, "wb") as file:
            file.write(response.content)
        logger.info(f"File {file_name} downloaded successfully")

    def _check_years_are_valid(self) -> None:
        for year in self.years_to_import:
            if year < self.MIN_YEAR or year > self.MAX_YEAR:
                raise ValueError(f"Year {year} is not valid. Must be between {self.MIN_YEAR} and {self.MAX_YEAR}")

"""
Google Sheets integration for writing aggregated data
"""

import os
from typing import Dict, List
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class SheetsIntegration:
    """Integration with Google Sheets for data storage"""
    
    # Scopes required for Google Sheets API
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    def __init__(self, config: Dict):
        """
        Initialize Google Sheets integration
        
        Args:
            config: Application configuration dictionary
        """
        self.config = config
        self.sheets_config = config.get('google_sheets', {})
        self.spreadsheet_name = self.sheets_config.get('spreadsheet_name')
        self.worksheet_name = self.sheets_config.get('worksheet_name')
        self.credentials_path = self.sheets_config.get('credentials_path')
        self.client = None
        self.spreadsheet = None
        self.worksheet = None
        
        self._initialize_connection()
        
    def _initialize_connection(self):
        """Initialize connection to Google Sheets"""
        try:
            # Check if credentials file exists
            if not os.path.exists(self.credentials_path):
                logger.warning(
                    f"Google Sheets credentials not found at {self.credentials_path}. "
                    "Data will not be written to Google Sheets."
                )
                return
                
            # Authenticate with Google Sheets
            creds = Credentials.from_service_account_file(
                self.credentials_path,
                scopes=self.SCOPES
            )
            self.client = gspread.authorize(creds)
            
            # Open or create spreadsheet
            self._setup_spreadsheet()
            
            logger.info("Successfully connected to Google Sheets")
            
        except Exception as e:
            logger.error(f"Error initializing Google Sheets connection: {e}")
            self.client = None
            
    def _setup_spreadsheet(self):
        """Setup spreadsheet and worksheet"""
        try:
            # Try to open existing spreadsheet
            self.spreadsheet = self.client.open(self.spreadsheet_name)
            logger.info(f"Opened existing spreadsheet: {self.spreadsheet_name}")
        except gspread.SpreadsheetNotFound:
            # Create new spreadsheet if it doesn't exist
            self.spreadsheet = self.client.create(self.spreadsheet_name)
            logger.info(f"Created new spreadsheet: {self.spreadsheet_name}")
            
        # Get or create worksheet
        try:
            self.worksheet = self.spreadsheet.worksheet(self.worksheet_name)
            logger.info(f"Using existing worksheet: {self.worksheet_name}")
        except gspread.WorksheetNotFound:
            self.worksheet = self.spreadsheet.add_worksheet(
                title=self.worksheet_name,
                rows=1000,
                cols=20
            )
            logger.info(f"Created new worksheet: {self.worksheet_name}")
            self._setup_headers()
            
    def _setup_headers(self):
        """Setup column headers in the worksheet"""
        headers = [
            'Timestamp',
            'Service',
            'Metric Type',
            'Input Tokens',
            'Output Tokens',
            'API Calls',
            'Active Users',
            'User Seats',
            'Storage GB',
            'Compute Hours',
            'Data Transfers GB',
            'Resources Managed',
            'Active Projects',
            'Active Jobs',
            'Memory GB Hours',
            'Models',
            'Period Start',
            'Period End',
            'Calculated Cost USD'
        ]
        
        try:
            self.worksheet.update('A1:S1', [headers])
            # Format header row
            self.worksheet.format('A1:S1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
            })
            logger.info("Setup worksheet headers")
        except Exception as e:
            logger.error(f"Error setting up headers: {e}")
            
    def write_data(self, data: List[Dict]):
        """
        Write aggregated data to Google Sheets
        
        Args:
            data: List of aggregated data records
        """
        if not self.client or not self.worksheet:
            logger.warning("Google Sheets not configured, skipping write")
            return
            
        if not data:
            logger.warning("No data to write to Google Sheets")
            return
            
        try:
            # Convert data records to rows
            rows = self._convert_to_rows(data)
            
            # Append data to worksheet
            self.worksheet.append_rows(rows, value_input_option='USER_ENTERED')
            
            logger.info(f"Successfully wrote {len(rows)} rows to Google Sheets")
            
        except Exception as e:
            logger.error(f"Error writing data to Google Sheets: {e}")
            
    def _convert_to_rows(self, data: List[Dict]) -> List[List]:
        """
        Convert data records to spreadsheet rows
        
        Args:
            data: List of data records
            
        Returns:
            List of rows for spreadsheet
        """
        rows = []
        
        for record in data:
            row = [
                record.get('timestamp', ''),
                record.get('service', ''),
                record.get('metric_type', ''),
                record.get('input_token', ''),
                record.get('output_token', ''),
                record.get('api_calls', '') or record.get('api_call', ''),
                record.get('active_users', ''),
                record.get('user_seat', ''),
                record.get('storage_gb', ''),
                record.get('compute_hour', ''),
                record.get('data_transfers_gb', ''),
                record.get('resources_managed', ''),
                record.get('active_projects', ''),
                record.get('active_jobs', ''),
                record.get('memory_gb_hours', ''),
                record.get('models', ''),
                record.get('period_start', ''),
                record.get('period_end', ''),
                record.get('calculated_cost', 0.0)
            ]
            rows.append(row)
            
        return rows
        
    def get_spreadsheet_url(self) -> str:
        """
        Get the URL of the spreadsheet
        
        Returns:
            Spreadsheet URL
        """
        if self.spreadsheet:
            return self.spreadsheet.url
        return None

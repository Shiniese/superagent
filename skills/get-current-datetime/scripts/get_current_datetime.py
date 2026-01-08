import argparse  

from datetime import datetime
from zoneinfo import ZoneInfo

def get_current_datetime(timezone: str = 'Asia/Shanghai') -> str:
    """
    Get the current date and time in the specified timezone.

    Args:
        timezone: IANA timezone identifier (e.g., 'Asia/Shanghai', 'Europe/Berlin', 'America/New_York')
    """

    try:
        tz = ZoneInfo(timezone)
        now = datetime.now(tz)
        return now.strftime("%Y-%m-%d %H:%M:%S %Z")
    
    except Exception as e:
        return f"Error: {str(e)}. Please provide a valid IANA timezone (e.g., 'Asia/Tokyo')."
    
def main():
    parser = argparse.ArgumentParser(description="Get current date and time in a specific timezone.")
    parser.add_argument("timezone", nargs="?", default="Asia/Shanghai", 
                        help="IANA timezone (e.g., Asia/Shanghai, Europe/Berlin, America/New_York)")
    
    args = parser.parse_args()
    
    result = get_current_datetime(args.timezone)
    print(result)

if __name__ == "__main__":
    main()
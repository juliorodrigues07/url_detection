from random_user_agent.params import OperatingSystem
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName


# Total number of URLs to scrap
N_URLS = 333990.0

# Each page shows a list with 20 URLs
PER_PAGE = 20.0

# Phishing database webpage
MAIN_URL = 'https://phishtank.org/phish_search.php?'

# Getting confirmed phishing URLs that are online or offline
QUERY = 'valid=y&active=All&Search=Search'

# Generation of the user-agent strings (for distinct OS and browsers)
SOFTWARE_NAMES = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value,
                  SoftwareName.EDGE.value, SoftwareName.OPERA.value, SoftwareName.SAFARI.value]
OPERATING_SYSTEMS = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.ANDROID.value,
                     OperatingSystem.IOS.value, OperatingSystem.MACOS.value]
USER_AGENT_ROTATOR = UserAgent(software_names=SOFTWARE_NAMES, operating_systems=OPERATING_SYSTEMS, limit=500)

import random
from selenium.webdriver.firefox.options import Options


def user_agent_options():

    options = Options()
    options.headless = False
    # User-Agent to options
    user_agents = [
        "Mozilla/5.0 (X11; Linux x86_64) Firefox/100.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
			"(KHTML, like Gecko) Version/16.0 Safari/605.1.15 Edg/138.0.0.0"
    ]
    selected_agent = random.choice(user_agents)

    options.set_preference(
        "general.useragent.override", 
        selected_agent
    )
    options.set_preference("intl.accept_languages", "uk-UA,uk,en-US")

    return options

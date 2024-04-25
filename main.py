import yaml
from src.web.webutil import WebUtil


def read_config_and_process(yaml_file: str, folder: str) -> None:
    """
    Reads the YAML configuration file and downloads the HTML pages to the specified folder.

    Args:
        yaml_file: Path to the YAML configuration file.
        folder: Path to the folder where HTML pages will be downloaded.
    """
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    # Iterate over each website in the configuration file
    for website in data['websites']:
        url = website['url']

        # Iterate over each subpage of the website
        for subpage in website['subpages']:
            full_url = url + subpage
            print(f"Downloading HTML page from: {full_url}")
            WebUtil.download_html_page(full_url, folder)


def main() -> None:
    """
    Main entry point of the program.
    """
    config_file = 'webconfig.yaml'  # Replace with the actual path to your YAML config file
    read_config_and_process(config_file, 'downloads')


if __name__ == '__main__':
    main()

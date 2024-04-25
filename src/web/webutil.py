import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os
import json


class WebUtil:
    """A utility class for web-related operations."""

    def download_html_page(url: str, folder: str) -> None:
        """Downloads an HTML page from the given URL and saves it to the specified folder.

        Args:
            url (str): The URL of the HTML page to download.
            folder (str): The folder where the downloaded HTML page will be saved.
        """
        # Generate the file name using the current date and time
        current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
        file_name = f"webpage-{url.split('/')[-1]}-{current_datetime}.html"

        # Create the folder if it does not exist
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Send a GET request to the URL to download the HTML content
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Save the parsed HTML content to the specified folder with the generated file name
            with open(f"{folder}/{file_name}", "w", encoding="utf-8") as file:
                file.write(soup.prettify())
            print(f"HTML page downloaded and saved as {file_name} in {folder}.")

            # Call the list_form_elements function
            WebUtil.list_form_elements(f"{folder}/{file_name}")
        else:
            print("Failed to download the HTML page.")

    def list_form_elements(file_path: str) -> None:
        """Lists all form elements, navigation links, and breadcrumbs in the downloaded HTML file along with their name and type.

        Args:
            file_path (str): The path to the downloaded HTML file.
        """
        # Check if the file exists
        if not os.path.exists(file_path):
            print("File does not exist.")
            return

        # Read the HTML file
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all form elements
        form_elements = soup.find_all(["input", "select", "textarea"])

        # Find all navigation links
        navigation_links = soup.find_all("a")

        # Find the breadcrumbs
        breadcrumbs = soup.find_all(class_="breadcrumb")

        # Create a dictionary to store the form elements, navigation links, and breadcrumbs
        output_dict = {}

        # Store the form elements and their attributes in the output_dict
        form_elements_dict = {}
        for element in form_elements:
            name = element.get("name")
            element_type = element.name
            form_elements_dict[name] = element_type
        output_dict["Form Elements"] = form_elements_dict

        # Store the navigation links in the output_dict
        navigation_links_dict = {}
        for link in navigation_links:
            href = link.get("href")
            text = link.text.strip()
            navigation_links_dict[href] = text
        output_dict["Navigation Links"] = navigation_links_dict

        # Store the breadcrumbs in the output_dict
        breadcrumbs_list = []
        for breadcrumb in breadcrumbs:
            breadcrumbs_list.append(breadcrumb.text.strip())
        output_dict["Breadcrumbs"] = breadcrumbs_list

        # Generate the output file name using the input file path
        file_name = os.path.basename(file_path)
        output_file_name = f"{os.path.splitext(file_name)[0]}.json"

        # Create the output folder if it does not exist
        output_folder = "formcontrols"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Save the output dictionary as JSON in the output folder with the generated file name
        with open(f"{output_folder}/{output_file_name}", "w") as output_file:
            json.dump(output_dict, output_file)

        print(f"Output saved as {output_file_name} in {output_folder}.")

import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Uncomment to run headless
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
service = Service('D:\Work\Personal\chromedriver.exe')  # Update with your chromedriver path
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()
# Read keywords from a text file and write results to a CSV file
input_file = 'source/image_source.txt'  # Text file with one keyword per line
output_file = 'output/image_urls.csv'  # Output CSV file

# Open the CSV file in write mode with semicolon as delimiter
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=';')  # Specify the delimiter
    csv_writer.writerow(['Keyword', 'Image URL'])  # Write header

    # Read keywords from the input file
    with open(input_file, 'r', encoding='utf-8') as file:  # Specify encoding here
        keywords = [line.strip() for line in file if line.strip()]  # Read and strip lines

    # Iterate through keywords and fetch image URLs
    for keyword in keywords:
        while True:  # Loop for retry mechanism
            try:
                print(f"Fetching image for keyword: {keyword}")
                
                # Clean up keyword from unwanted characters
                keyword_cleaned = ''.join(char for char in keyword if char.isalnum() or char.isspace())
                query = keyword_cleaned.replace(' ', '+') + ""
                search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"
                
                driver.get(search_url)
                time.sleep(2)  # Wait for images to load

                # Find the top image element and click on it
                first_image = driver.find_element(By.XPATH, '//*[@id="rso"]/div/div/div[1]/div/div/div[1]')
                first_image.click()
                time.sleep(3)  # Wait for the enlarged image to load

                # Use a more dynamic approach for finding the image URL
                get_image = driver.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a/img')
                image_url = get_image.get_attribute('src')

                # Write the result directly to the CSV
                csv_writer.writerow([keyword, image_url])  # Write each keyword and its image URL
                print(f"Image URL for '{keyword}': {image_url}")
                break  # Exit the while loop if successful

            except Exception as e:
                print(f"Error retrieving image for '{keyword}': {e}")
                csv_writer.writerow([keyword, "Not found"])
                print(f"Image URL for '{keyword}': Not found")
                break  # Move to the next keyword if error occurs

# Close the driver after processing all keywords
driver.quit()
print("Image URL fetching completed.")

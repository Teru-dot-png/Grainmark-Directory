import os
import json
import shutil

# --- SCRIPT LOGIC ---
# This script assumes that 'Businesses/', 'ID TEMPLATE/', and 'businesses.json'
# are all in the same directory where the script is run.

def automate_business_folder_creation():
    """
    Scans businesses.json for entries with 'hasId: false', then creates a
    folder and copies a Krita template file for each.
    """
    # Define file and folder names
    businesses_dir = "Businesses"
    template_dir = "ID TEMPLATE"
    json_file = "businesses.json"
    template_file = os.path.join(template_dir, "ID TEMPLATE FOR BUSINESS.kra")

    print("Starting the automation process...")

    # --- 1. Load the JSON data ---
    try:
        with open(json_file, 'r') as f:
            businesses_data = json.load(f)
        print(f"Successfully loaded '{json_file}'.")
    except FileNotFoundError:
        print(f"[ERROR] The file '{json_file}' was not found in the current directory.")
        return
    except json.JSONDecodeError:
        print(f"[ERROR] The file '{json_file}' contains invalid JSON. Please check its format.")
        return

    # --- 2. Check for required folders and files ---
    if not os.path.isdir(businesses_dir):
        print(f"[INFO] The '{businesses_dir}' directory does not exist. Creating it now.")
        os.makedirs(businesses_dir)

    if not os.path.isfile(template_file):
        print(f"[ERROR] The template file could not be found at '{template_file}'.")
        return

    # --- 3. Process each business entry ---
    processed_count = 0
    for business in businesses_data:
        if not business.get("hasId"):
            owner_name = business.get("ownerName")
            business_name = business.get("businessName")
            permit_number = business.get("permitNumber")

            # Ensure all required data is present before proceeding
            if not all([owner_name, business_name, permit_number]):
                print(f"[WARNING] Skipping an entry because it's missing a name or permit number: {business}")
                continue

            # Create the folder for the business
            new_folder_name = f"{owner_name}-{business_name}-{permit_number}"
            new_folder_path = os.path.join(businesses_dir, new_folder_name)

            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
                print(f"\nCreated folder: '{new_folder_name}'")
            else:
                print(f"\nFolder '{new_folder_name}' already exists. Checking for file...")

            # Copy and rename the Krita template file
            new_file_name = f"{owner_name} ID BUSINESS.kra"
            destination_file_path = os.path.join(new_folder_path, new_file_name)

            if not os.path.exists(destination_file_path):
                shutil.copy(template_file, destination_file_path)
                print(f"  -> Copied and renamed template to '{new_file_name}'")
                processed_count += 1
            else:
                print(f"  -> File '{new_file_name}' already exists. Skipping.")

    if processed_count == 0:
        print("\nFinished. No new businesses with 'hasId: false' were found to process.")
    else:
        print(f"\nAutomation complete. Processed {processed_count} new business entries.")


if __name__ == "__main__":
    automate_business_folder_creation()
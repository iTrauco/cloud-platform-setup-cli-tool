#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import subprocess
import sys
import  boto3


def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def get_all_aws_services():
    # Initialize the Boto3 client for the AWS service catalog
    client = boto3.client('servicecatalog')

    # Retrieve the list of AWS services
    response = client.list_services()

    # Extract service names
    service_names = [service['Name'] for service in response['Services']]

    # Initialize an empty list to store service information
    services_info = []

    # Iterate over each service to get its description and documentation URL
    for service_name in service_names:
        try:
            # Get the description of the service
            description = client.describe_service(ServiceName=service_name)['Service']['Description']

            # Construct the documentation URL
            doc_url = f"https://docs.aws.amazon.com/{service_name}/latest/userguide/"

            # Add service information to the list
            services_info.append({'Service Name': service_name, 'Description': description, 'Documentation URL': doc_url})
        except Exception as e:
            # Handle exceptions if the service does not have documentation or description available
            print(f"Error fetching information for service {service_name}: {str(e)}")

    return services_info

def save_to_csv(services_info, output):
    # Convert the list of dictionaries into a Pandas DataFrame
    df = pd.DataFrame(services_info)

    # Save the DataFrame to a CSV file
    df.to_csv(output, index=False)
    click.echo(f"Output saved to {output}")

@click.command()
@click.option('--output', default='aws_services.csv', help='Output file path (default: aws_services.csv)')
def main(output):
    """
    This script retrieves information about AWS services and outputs it to a CSV file.
    """
    click.echo("Welcome to the Cloud Services CLI!")
    cloud_provider = click.prompt("Which cloud provider's services do you want to retrieve? (aws/gcp/azure)", type=str)

    if cloud_provider.lower() == 'aws':
        click.echo("Retrieving information about AWS services...")
        try:
            import boto3
            import pandas as pd
        except ImportError:
            install = click.confirm("Required packages (boto3 and pandas) are not installed. Do you want to install them now?")
            if install:
                install_package("boto3")
                install_package("pandas")
                click.echo("Packages installed successfully!")
            else:
                click.echo("Cannot proceed without required packages. Exiting.")
                sys.exit(1)
        
        services_info = get_all_aws_services()
        save_to_csv(services_info, output)
    elif cloud_provider.lower() == 'gcp':
        click.echo("Retrieving information about GCP services...")
        # Call function to retrieve GCP services
        # save_to_csv(gcp_services_info, output)
        click.echo("GCP services retrieval is not implemented yet.")
    elif cloud_provider.lower() == 'azure':
        click.echo("Retrieving information about Azure services...")
        # Call function to retrieve Azure services
        # save_to_csv(azure_services_info, output)
        click.echo("Azure services retrieval is not implemented yet.")
    else:
        click.echo("Invalid input. Please choose either 'aws', 'gcp', or 'azure'.")

if __name__ == "__main__":
    main()

